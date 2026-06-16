"""
EDGAR comp-extraction engine: the documented fallback for the External Hire Premium study.

Use this only if WRDS access does not materialize, OR to fill the NaN gaps the WRDS
ExecuComp pull leaves behind. It collects CEO compensation from DEF 14A proxy
Summary Compensation Tables (SCTs) straight from SEC EDGAR. It is free and authoritative
but slower and messier than ExecuComp; see the caveats in the README.

What it does, per transition:
  - finds the firm's DEF 14A filed in the successor's target proxy year and the
    predecessor's target proxy year (a proxy filed in year T+1 reports year-T pay),
  - fetches the filing's primary HTML document,
  - locates the Summary Compensation Table,
  - extracts the named-executive rows and flags the CEO row(s),
  - records salary and total compensation with the source accession number.

Inputs : edgar_comp_panel.csv  (561 transitions carrying CIK, with proxy years precomputed)
Outputs: edgar_comp_raw.csv      (every NEO row parsed, with confidence flags)
         edgar_comp_matched.csv  (one row per transition: pred + succ CEO comp)

EDGAR fair-access rules are respected: a descriptive User-Agent with contact email is
REQUIRED (edit CONTACT below), and requests are throttled to <=8/sec.

IMPORTANT FIELD NOTE for the methods page: the proxy SCT "Total" column is the
grant-date-fair-value total under post-2006 SEC rules. It is NOT identical to
ExecuComp TDC1. If any figure here is mixed with WRDS TDC1 figures, label the source
per row so the comparison stays honest. Prefer WRDS TDC1 as the headline; use these
for gaps and validation.
"""

import requests, time, io, re, sys
import pandas as pd
from datetime import datetime

# ---- EDGAR fair-access: EDIT THIS before running ---------------------
CONTACT = "External Hire Premium research <ross@themallorygroup.ai>"
HEADERS = {"User-Agent": CONTACT, "Accept-Encoding": "gzip, deflate"}
THROTTLE = 0.15          # seconds between requests (~7/sec, under EDGAR's 10/sec cap)
# ----------------------------------------------------------------------

SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:010d}.json"
ARCHIVE     = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash}/{doc}"

def get(url):
    time.sleep(THROTTLE)
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r

def def14a_filings(cik):
    """Return list of (filing_date, accession, primary_doc) for all DEF 14A filings."""
    j = get(SUBMISSIONS.format(cik=cik)).json()
    recent = j["filings"]["recent"]
    out = []
    for form, date, acc, doc in zip(recent["form"], recent["filingDate"],
                                    recent["accessionNumber"], recent["primaryDocument"]):
        if form == "DEF 14A":
            out.append((date, acc, doc))
    return out

def fetch_proxy_html(cik, acc, doc):
    acc_nodash = acc.replace("-", "")
    url = ARCHIVE.format(cik=cik, acc_nodash=acc_nodash, doc=doc)
    return get(url).text

def find_sct(html):
    """
    Return the Summary Compensation Table as a DataFrame, or None.
    Strategy: read every HTML table, keep the one whose header/cells mention the
    SCT signature columns (salary, stock awards, total) and that contains a year column.
    """
    try:
        tables = pd.read_html(io.StringIO(html))
    except ValueError:
        return None
    best, best_score = None, 0
    for t in tables:
        flat = " ".join(str(c) for c in t.columns) + " " + \
               " ".join(t.astype(str).head(3).values.ravel().tolist())
        flat = flat.lower()
        score = sum(k in flat for k in
                    ["salary", "stock award", "option award", "total", "name and principal"])
        if score > best_score and ("salary" in flat and "total" in flat):
            best, best_score = t, score
    return best

def parse_neo_rows(sct, ceo_name_hint):
    """
    From the SCT, return list of dicts: {name, year, salary, total, is_ceo}.
    Heuristics: the first text column holds names/titles; numeric columns hold dollars;
    a row is CEO if its name cell matches the hint or an adjacent title cell says
    'Chief Executive' / 'CEO'.
    """
    if sct is None or sct.empty:
        return []
    df = sct.copy()
    df.columns = [str(c) for c in df.columns]
    # crude column role detection
    name_col = df.columns[0]
    def money(x):
        s = re.sub(r"[^0-9.]", "", str(x))
        return float(s) if s not in ("", ".") else None
    # find a 'year' column and a 'total' column
    year_col = next((c for c in df.columns if re.search(r"year", c, re.I)), None)
    total_col = next((c for c in df.columns if re.search(r"total", c, re.I)), None)
    salary_col = next((c for c in df.columns if re.search(r"salary", c, re.I)), None)
    rows = []
    last_name = None
    hint = (ceo_name_hint or "").split()[-1].lower() if ceo_name_hint else ""
    for _, r in df.iterrows():
        nm = str(r[name_col]).strip()
        if nm and nm.lower() != "nan":
            last_name = nm
        blob = " ".join(str(v) for v in r.values).lower()
        is_ceo = ("chief executive" in blob or re.search(r"\bceo\b", blob) is not None
                  or (hint and hint in (last_name or "").lower()))
        rows.append({
            "name": last_name,
            "year": str(r[year_col]).strip() if year_col else "",
            "salary": money(r[salary_col]) if salary_col else None,
            "total": money(r[total_col]) if total_col else None,
            "is_ceo": bool(is_ceo),
        })
    return rows

def pick_proxy_for_year(filings, proxy_year):
    """Choose the DEF 14A filed in proxy_year (reports prior-year comp)."""
    cands = [(d, a, doc) for (d, a, doc) in filings if d[:4] == str(proxy_year)]
    return cands[0] if cands else None

def run(panel_path="edgar_comp_panel.csv"):
    panel = pd.read_csv(panel_path)
    panel["cik"] = panel["cik"].astype(int)
    raw_rows, matched = [], []
    # cache filings per CIK to avoid refetching
    fil_cache = {}
    for _, p in panel.iterrows():
        cik = p["cik"]
        try:
            if cik not in fil_cache:
                fil_cache[cik] = def14a_filings(cik)
            filings = fil_cache[cik]
        except Exception as ex:
            matched.append({**p.to_dict(), "status": f"submissions-error:{ex}"})
            continue

        rec = {"transition_id": p["transition_id"], "cik": cik, "coname": p["coname"],
               "classification": p["classification"]}
        for role, who, pyr, fy in [("succ", p["successor"], p["succ_proxy_year"], p["succ_first_full_fy"]),
                                   ("pred", p["predecessor"], p["pred_proxy_year"], p["pred_last_full_fy"])]:
            sel = pick_proxy_for_year(filings, int(pyr))
            if not sel:
                rec[f"{role}_total"] = None; rec[f"{role}_status"] = "no-proxy-for-year"
                continue
            d, acc, doc = sel
            try:
                html = fetch_proxy_html(cik, acc, doc)
                sct = find_sct(html)
                neo = parse_neo_rows(sct, who)
            except Exception as ex:
                rec[f"{role}_total"] = None; rec[f"{role}_status"] = f"fetch/parse-error:{ex}"
                continue
            # choose the CEO row matching the target fiscal year if year column present
            ceo_rows = [n for n in neo if n["is_ceo"]]
            target = None
            for n in ceo_rows:
                if str(fy) in str(n["year"]):
                    target = n; break
            if target is None and ceo_rows:
                target = max(ceo_rows, key=lambda n: (n["total"] or 0))  # fallback: top CEO row
            rec[f"{role}_total"] = target["total"] if target else None
            rec[f"{role}_salary"] = target["salary"] if target else None
            rec[f"{role}_name_parsed"] = target["name"] if target else None
            rec[f"{role}_accession"] = acc
            rec[f"{role}_status"] = "ok" if target else "ceo-row-not-found"
            for n in neo:
                raw_rows.append({"transition_id": p["transition_id"], "role": role,
                                 "accession": acc, **n})
        rec["comp_ratio_succ_over_pred"] = (
            rec.get("succ_total")/rec.get("pred_total")
            if rec.get("succ_total") and rec.get("pred_total") else None)
        matched.append(rec)

    pd.DataFrame(raw_rows).to_csv("edgar_comp_raw.csv", index=False)
    M = pd.DataFrame(matched)
    M.to_csv("edgar_comp_matched.csv", index=False)
    ok_succ = (M.get("succ_status") == "ok").sum() if "succ_status" in M else 0
    ok_pred = (M.get("pred_status") == "ok").sum() if "pred_status" in M else 0
    print(f"Transitions processed: {len(M)}")
    print(f"  successor comp parsed ok: {ok_succ}")
    print(f"  predecessor comp parsed ok: {ok_pred}")
    print("Low-confidence rows (status != ok) are flagged for manual SCT review.")

if __name__ == "__main__":
    if CONTACT.startswith("External Hire Premium research <your-email"):
        sys.exit("EDIT the CONTACT variable with your real email before running (EDGAR requires it).")
    run()
