"""
SEC XBRL ROA fetcher: the free, structured ROA layer for the External Hire Premium study.

Pulls net income and total assets straight from the SEC's XBRL company-facts API
(data.sec.gov), no login and no key, and computes ROA = NetIncomeLoss / Assets for each
transition's predecessor-last-full-fiscal-year and successor-first-full-fiscal-year.

This is the same financial data Compustat repackages, taken from the issuer's own tagged
filings, so it is not a degraded fallback; it is the authoritative source. ROA here uses
year-end total assets (the conventional ni/at). An operating variant (OperatingIncomeLoss
/ Assets) is also computed where the tag is present, as a robustness measure.

Inputs : wrds_panel_gvkeys.csv  (uses cik, appt years; 561 of 611 rows carry CIK)
Output : roa_from_xbrl.csv       (pred ROA, succ ROA, source years, match status)

SEC fair-access: a descriptive User-Agent with contact email is REQUIRED; edit CONTACT.
Requests are throttled under SEC's 10/sec limit.
"""

import requests, time, sys
import pandas as pd

# ---- SEC fair-access: EDIT before running ----------------------------
CONTACT = "External Hire Premium research <ross@themallorygroup.ai>"
HEADERS = {"User-Agent": CONTACT, "Accept-Encoding": "gzip, deflate"}
THROTTLE = 0.12
# ----------------------------------------------------------------------

FACTS = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"

def get_facts(cik):
    time.sleep(THROTTLE)
    r = requests.get(FACTS.format(cik=int(cik)), headers=HEADERS, timeout=30)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def annual_value(facts, tag, fy, instant=False):
    """
    Return the annual value of a us-gaap tag for fiscal year `fy`.
    instant=True for balance-sheet items (Assets): match the fiscal-year-end snapshot.
    instant=False for flow items (NetIncomeLoss): match the full-year duration.
    Strategy: prefer 10-K, fp='FY', fy match; among matches take the latest filed.
    """
    try:
        units = facts["facts"]["us-gaap"][tag]["units"]["USD"]
    except KeyError:
        return None
    cand = []
    for u in units:
        if u.get("fy") != fy or u.get("fp") != "FY":
            continue
        if u.get("form") not in ("10-K", "10-K/A"):
            continue
        if not instant:
            # flow: require a ~annual period (>= ~350 days)
            if "start" not in u or "end" not in u:
                continue
            d = (pd.Timestamp(u["end"]) - pd.Timestamp(u["start"])).days
            if d < 350:
                continue
        cand.append(u)
    if not cand:
        # relax: any form, fy match
        for u in units:
            if u.get("fy") == fy and u.get("fp") == "FY":
                cand.append(u)
    if not cand:
        return None
    cand.sort(key=lambda u: u.get("filed", ""), reverse=True)
    return cand[0]["val"]

def roa_for(facts, fy):
    if facts is None or fy is None or pd.isna(fy):
        return (None, None, None, None)
    fy = int(fy)
    ni = annual_value(facts, "NetIncomeLoss", fy, instant=False)
    at = annual_value(facts, "Assets", fy, instant=True)
    oi = annual_value(facts, "OperatingIncomeLoss", fy, instant=False)
    roa = (ni / at) if (ni is not None and at not in (None, 0)) else None
    roa_oper = (oi / at) if (oi is not None and at not in (None, 0)) else None
    return (roa, roa_oper, ni, at)

def run(panel_path="wrds_panel_gvkeys.csv"):
    panel = pd.read_csv(panel_path)
    panel = panel.dropna(subset=["cik"]).copy()
    panel["cik"] = panel["cik"].astype(int)
    cache, rows = {}, []
    for _, p in panel.iterrows():
        cik = p["cik"]
        try:
            if cik not in cache:
                cache[cik] = get_facts(cik)
            facts = cache[cik]
        except Exception as ex:
            rows.append({"transition_id": p["transition_id"], "cik": cik,
                         "coname": p["coname"], "status": f"facts-error:{ex}"})
            continue
        pre_roa, pre_oper, pre_ni, pre_at = roa_for(facts, p["pred_last_full_fy"])
        post_roa, post_oper, post_ni, post_at = roa_for(facts, p["succ_first_full_fy"])
        rows.append({
            "transition_id": p["transition_id"], "cik": cik, "coname": p["coname"],
            "classification": p["classification"],
            "pred_last_full_fy": p["pred_last_full_fy"], "roa_pre": pre_roa,
            "roa_oper_pre": pre_oper, "ni_pre": pre_ni, "at_pre": pre_at,
            "succ_first_full_fy": p["succ_first_full_fy"], "roa_post": post_roa,
            "roa_oper_post": post_oper, "ni_post": post_ni, "at_post": post_at,
            "roa_delta": (post_roa - pre_roa) if (pre_roa is not None and post_roa is not None) else None,
            "status": "ok" if (pre_roa is not None and post_roa is not None)
                      else "partial-or-missing (check tags/fiscal-year)",
        })
    out = pd.DataFrame(rows)
    out.to_csv("roa_from_xbrl.csv", index=False)
    ok = (out["status"] == "ok").sum()
    print(f"ROA from XBRL: {len(out)} transitions, {ok} with both pre and post ROA.")
    print("Missing rows are typically pre-XBRL years (XBRL mandatory ~FY2009+) or non-")
    print("calendar fiscal ends; flagged for a manual companyconcept check or EDGAR 10-K.")

if __name__ == "__main__":
    if CONTACT.startswith("External Hire Premium research <your-email"):
        sys.exit("EDIT the CONTACT variable with your real email before running (SEC requires it).")
    run()
