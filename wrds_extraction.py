"""
SEC SIC fetcher: the industry-control layer for the External Hire Premium study.

Pulls each firm's SIC code and description from the SEC submissions API (data.sec.gov),
no login, no key. Gives a 2-digit SIC industry for fixed effects in the regressions,
the one control that was missing from the first controlled pass.

Inputs : wrds_panel_gvkeys.csv  (uses cik)
Output : sic_from_sec.csv        (transition_id, cik, sic, sic2, sic_desc)

Edit CONTACT before running. Throttled under SEC's 10/sec limit. Fast (~400 firms).
"""
import requests, time, sys
import pandas as pd

CONTACT = "External Hire Premium research <ross@themallorygroup.ai>"
HEADERS = {"User-Agent": CONTACT, "Accept-Encoding": "gzip, deflate"}
THROTTLE = 0.12
SUB = "https://data.sec.gov/submissions/CIK{cik:010d}.json"

def run(panel_path="wrds_panel_gvkeys.csv"):
    panel = pd.read_csv(panel_path).dropna(subset=["cik"]).copy()
    panel["cik"] = panel["cik"].astype(int)
    cache, rows = {}, []
    for i, (_, p) in enumerate(panel.iterrows(), 1):
        if i % 25 == 0: print(f"  ...{i} of {len(panel)}")
        cik = int(p["cik"])
        if cik not in cache:
            try:
                time.sleep(THROTTLE)
                j = requests.get(SUB.format(cik=cik), headers=HEADERS, timeout=30).json()
                cache[cik] = (str(j.get("sic", "")), j.get("sicDescription", ""))
            except Exception:
                cache[cik] = ("", "")
        sic, desc = cache[cik]
        rows.append({"transition_id": p["transition_id"], "cik": cik,
                     "sic": sic, "sic2": sic[:2] if sic else "",
                     "sic_desc": desc})
    out = pd.DataFrame(rows)
    out.to_csv("sic_from_sec.csv", index=False)
    print(f"SIC fetched: {len(out)} transitions, {(out['sic']!='').sum()} with a code, "
          f"{out['sic2'].nunique()} distinct 2-digit industries.")

if __name__ == "__main__":
    if "your-email" in CONTACT:
        sys.exit("EDIT the CONTACT variable with your real email before running.")
    run()
