"""
WRDS extraction for the External Hire Premium study.

Pulls the three pass-two financial layers for the classified panel:
  1. ExecuComp anncomp  -> predecessor and successor total compensation (TDC1)
  2. Compustat funda    -> ROA inputs (net income, total assets) for event windows
  3. CRSP monthly       -> returns for the -2yr / +3yr TSR windows

Run inside WRDS JupyterHub, or anywhere the `wrds` Python module can authenticate.
No data is redistributed: this script reads WRDS and writes derived outputs locally.

Inputs : wrds_panel_gvkeys.csv  (the 611-transition panel, keyed on gvkey)
Outputs: execucomp_ceo_years.csv, compustat_funda.csv, crsp_monthly.csv,
         and the merged enrichment file enrichment_from_wrds.csv

Author: External Hire Premium project. Field choices follow the methods commitments:
TDC1 is the headline compensation measure (academic standard), not the proxy "Total" line.
"""

import wrds
import pandas as pd
import numpy as np

# ----------------------------------------------------------------------
# 0. Connect and load the panel
# ----------------------------------------------------------------------
conn = wrds.Connection()                       # prompts for WRDS credentials once
panel = pd.read_csv("wrds_panel_gvkeys.csv")
panel = panel.dropna(subset=["gvkey"]).copy()
panel["gvkey"] = panel["gvkey"].astype(int).astype(str).str.zfill(6)
gvkeys = sorted(panel["gvkey"].unique())
gvkey_sql = "(" + ",".join("'%s'" % g for g in gvkeys) + ")"

# Wide year band: -2 before the earliest transition (2010) through tenure of the
# latest (2022). Pulling a band per firm is more robust than exact-year pulls;
# the selection step below picks the right predecessor / successor fiscal years.
YR_MIN, YR_MAX = 2007, 2024

# ----------------------------------------------------------------------
# 1. ExecuComp: every CEO-year for the panel firms (TDC1 = headline comp)
# ----------------------------------------------------------------------
execucomp = conn.raw_sql(f"""
    SELECT gvkey, year, execid, exec_fullname, coname, title,
           ceoann, becameceo, leftofc,
           salary, bonus, stock_awards, option_awards,
           noneq_incent, othcomp, tdc1, tdc2
    FROM   comp_execucomp.anncomp
    WHERE  gvkey IN {gvkey_sql}
      AND  year BETWEEN {YR_MIN} AND {YR_MAX}
""", date_cols=["becameceo", "leftofc"])
execucomp.to_csv("execucomp_ceo_years.csv", index=False)
print(f"ExecuComp: {len(execucomp):,} executive-years for {execucomp.gvkey.nunique()} firms")

# ----------------------------------------------------------------------
# 2. Compustat funda: ROA inputs and basic controls over the event windows
#    ROA = ni / at (net income over total assets), the conventional measure.
# ----------------------------------------------------------------------
funda = conn.raw_sql(f"""
    SELECT gvkey, datadate, fyear, conm,
           ni, at, oiadp, revt, sale
    FROM   comp.funda
    WHERE  gvkey IN {gvkey_sql}
      AND  fyear BETWEEN {YR_MIN} AND {YR_MAX}
      AND  indfmt='INDL' AND datafmt='STD'
      AND  popsrc='D' AND consol='C'
""", date_cols=["datadate"])
funda["roa"] = funda["ni"] / funda["at"]
funda["roa_oper"] = funda["oiadp"] / funda["at"]      # operating ROA, robustness
funda.to_csv("compustat_funda.csv", index=False)
print(f"Compustat: {len(funda):,} firm-years")

# ----------------------------------------------------------------------
# 3. CRSP monthly returns for TSR windows, via the CCM gvkey<->permno link
# ----------------------------------------------------------------------
link = conn.raw_sql(f"""
    SELECT gvkey, lpermno AS permno, linkdt, linkenddt, linktype, linkprim
    FROM   crsp.ccmxpf_linktable
    WHERE  gvkey IN {gvkey_sql}
      AND  linktype IN ('LU','LC') AND linkprim IN ('P','C')
""", date_cols=["linkdt", "linkenddt"])
link["linkenddt"] = link["linkenddt"].fillna(pd.Timestamp("2025-12-31"))
permnos = sorted(link["permno"].dropna().astype(int).unique())
permno_sql = "(" + ",".join(str(p) for p in permnos) + ")"

crsp = conn.raw_sql(f"""
    SELECT permno, date, ret, retx, prc, shrout
    FROM   crsp.msf
    WHERE  permno IN {permno_sql}
      AND  date BETWEEN '{YR_MIN}-01-01' AND '{YR_MAX}-12-31'
""", date_cols=["date"])

# value-weighted market return for index adjustment
mkt = conn.raw_sql(f"""
    SELECT date, vwretd
    FROM   crsp.msi
    WHERE  date BETWEEN '{YR_MIN}-01-01' AND '{YR_MAX}-12-31'
""", date_cols=["date"])
crsp = crsp.merge(mkt, on="date", how="left")
crsp.to_csv("crsp_monthly.csv", index=False)
print(f"CRSP: {len(crsp):,} security-months for {crsp.permno.nunique()} permnos")

conn.close()

# ----------------------------------------------------------------------
# 4. Selection / merge: build the per-transition enrichment record
# ----------------------------------------------------------------------
def ceo_year_comp(gvkey, fy):
    """TDC1 of the CEO-flagged executive for a given firm-year, if present."""
    rows = execucomp[(execucomp.gvkey == gvkey) & (execucomp.year == fy)
                     & (execucomp.ceoann == "CEO")]
    if len(rows) == 0:
        return (np.nan, None)
    r = rows.sort_values("tdc1", ascending=False).iloc[0]   # primary CEO row
    return (r["tdc1"], r["exec_fullname"])

def roa_for(gvkey, fy):
    rows = funda[(funda.gvkey == gvkey) & (funda.fyear == fy)]
    return rows["roa"].iloc[0] if len(rows) else np.nan

def tsr_window(gvkey, appt_date, yrs_before=2, yrs_after=3):
    """Compounded raw and market-adjusted return over the event window."""
    lk = link[link.gvkey == gvkey]
    if len(lk) == 0:
        return (np.nan, np.nan)
    appt = pd.Timestamp(appt_date)
    start, end = appt - pd.DateOffset(years=yrs_before), appt + pd.DateOffset(years=yrs_after)
    pn = lk["permno"].astype(int).tolist()
    win = crsp[(crsp.permno.isin(pn)) & (crsp.date >= start) & (crsp.date <= end)].copy()
    if len(win) == 0:
        return (np.nan, np.nan)
    raw = (1 + win["ret"].fillna(0)).prod() - 1
    mkt_cum = (1 + win["vwretd"].fillna(0)).prod() - 1
    return (raw, raw - mkt_cum)         # raw TSR, market-adjusted TSR

records = []
for _, p in panel.iterrows():
    g = p["gvkey"]
    succ_comp, succ_name = ceo_year_comp(g, p["succ_first_full_fy"])
    pred_comp, pred_name = ceo_year_comp(g, p["pred_last_full_fy"])
    tsr_raw, tsr_adj = tsr_window(g, p["appt_date"])
    records.append({
        "transition_id": p["transition_id"], "gvkey": g, "coname": p["coname"],
        "classification": p["classification"],
        "predecessor": p["predecessor"], "successor": p["successor"],
        "pred_last_full_fy": p["pred_last_full_fy"], "pred_tdc1": pred_comp,
        "pred_tdc1_execucomp_name": pred_name,
        "succ_first_full_fy": p["succ_first_full_fy"], "succ_tdc1": succ_comp,
        "succ_tdc1_execucomp_name": succ_name,
        "comp_ratio_succ_over_pred": (succ_comp / pred_comp) if (pred_comp and pred_comp == pred_comp and pred_comp != 0) else np.nan,
        "roa_pre": roa_for(g, p["pred_last_full_fy"]),
        "roa_post": roa_for(g, p["succ_first_full_fy"]),
        "tsr_raw_2y_3y": tsr_raw, "tsr_mktadj_2y_3y": tsr_adj,
    })

enr = pd.DataFrame(records)
enr.to_csv("enrichment_from_wrds.csv", index=False)
print(f"\nMerged enrichment written: {len(enr)} transitions")
print(f"  predecessor TDC1 matched: {enr.pred_tdc1.notna().sum()}")
print(f"  successor   TDC1 matched: {enr.succ_tdc1.notna().sum()}")
print(f"  TSR window computed:      {enr.tsr_raw_2y_3y.notna().sum()}")
print("\nNOTE: rows where ExecuComp has no CEO flag for the target year need a manual")
print("name->execid check (small-cap gaps, mid-year fiscal ends). These are flagged by NaN.")
