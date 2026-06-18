"""
Refined regressions for the External Hire Premium study.
Runs the moment the rerun outputs are in: wider TSR coverage, post-hire-only returns,
and 2-digit-SIC industry fixed effects. Staged ahead so the analysis is one command.

Expects in the working dir:
  edgar_comp_raw.csv      (comp, parsed)        roa_from_xbrl.csv   (ROA + assets)
  tsr_from_prices.csv     (NEW: post-hire cols) sic_from_sec.csv    (industry)
  wrds_panel_gvkeys.csv   (panel + appt dates)
"""
import pandas as pd, numpy as np, statsmodels.formula.api as smf

panel = pd.read_csv("wrds_panel_gvkeys.csv")
raw   = pd.read_csv("edgar_comp_raw.csv")
roa   = pd.read_csv("roa_from_xbrl.csv")
tsr   = pd.read_csv("tsr_from_prices.csv")
sic   = pd.read_csv("sic_from_sec.csv")

# --- rebuild comp from raw (outlier screen + nearest-year match) ---
ceo = raw[(raw["is_ceo"]==True) & raw["total"].notna()].copy()
ceo["yr"] = pd.to_numeric(ceo["year"], errors="coerce")
ceo = ceo[(ceo["total"]>=100_000) & (ceo["total"]<=200_000_000)]
def pick(tid, role, fy):
    if pd.isna(fy): return np.nan
    sub = ceo[(ceo["transition_id"]==tid) & (ceo["role"]==role)]
    if not len(sub): return np.nan
    ex = sub[sub["yr"]==int(fy)]
    if len(ex): return ex["total"].max()
    s2 = sub.dropna(subset=["yr"])
    if len(s2):
        s2 = s2.assign(d=(s2["yr"]-int(fy)).abs())
        return s2.sort_values(["d","total"],ascending=[True,False]).iloc[0]["total"]
    return sub["total"].max()
comp = pd.DataFrame([{"transition_id":p.transition_id,
                      "succ_total":pick(p.transition_id,"succ",p.succ_first_full_fy),
                      "pred_total":pick(p.transition_id,"pred",p.pred_last_full_fy)}
                     for p in panel.itertuples()])

d = panel[["transition_id","coname","classification","appt_date"]].merge(comp,on="transition_id",how="left")
d = d.merge(roa[["transition_id","roa_pre","roa_post","at_pre"]],on="transition_id",how="left")
# TSR: take post-hire-only if present, plus full for comparison
tcols = ["transition_id","tsr_mktadj"] + [c for c in ["tsr_post_mktadj","tsr_pre_mktadj"] if c in tsr.columns]
d = d.merge(tsr[tcols],on="transition_id",how="left")
d = d.merge(sic[["transition_id","sic2"]],on="transition_id",how="left")

d["year"]=pd.to_datetime(d["appt_date"],errors="coerce").dt.year
d["ext"]=(d["classification"]=="external").astype(int)
d["log_succ"]=np.log(d["succ_total"]); d["log_pred"]=np.log(d["pred_total"])
d["log_assets"]=np.log(d["at_pre"].where(d["at_pre"]>0))
d["log_ratio"]=np.log(d["succ_total"]/d["pred_total"])
d["roa_chg"]=d["roa_post"]-d["roa_pre"]
d["ind"]=d["sic2"].astype("Int64").astype(str)

def show(title, formula, key="ext"):
    try:
        r=smf.ols(formula,data=d).fit(cov_type="HC1")
        coef,p,n=r.params.get(key,np.nan),r.pvalues.get(key,np.nan),int(r.nobs)
        print(f"{title}\n   {key}: {coef:+.4f}  p={p:.4f}  n={n}  R2={r.rsquared:.3f}")
    except Exception as ex:
        print(f"{title}\n   (failed: {ex})")

print("="*72)
print("PREMIUM with industry FE")
show("  log(succ/pred ratio) ~ external + size + year + industry",
     "log_ratio ~ ext + log_assets + C(year) + C(ind)")
print("="*72)
print("RETURN, POST-HIRE-ONLY (breaks the selection confound) with industry FE")
if "tsr_post_mktadj" in d.columns:
    show("  post-hire market-adj TSR ~ external + size + year + industry",
         "tsr_post_mktadj ~ ext + log_assets + C(year) + C(ind)")
    show("  [compare] FULL-window market-adj TSR ~ external + ...",
         "tsr_mktadj ~ ext + log_assets + C(year) + C(ind)")
else:
    print("  tsr_post_mktadj not found - rerun price_tsr.py (upgraded) first.")
show("  ROA change ~ external + size + year + industry",
     "roa_chg ~ ext + log_assets + C(year) + C(ind)")
print("="*72)
print("HEADLINE: does premium predict POST-HIRE return? (industry FE)")
if "tsr_post_mktadj" in d.columns:
    show("  post-hire TSR ~ premium + size + year + industry","tsr_post_mktadj ~ log_ratio + log_assets + C(year) + C(ind)","log_ratio")
show("  ROA change ~ premium + size + year + industry","roa_chg ~ log_ratio + log_assets + C(year) + C(ind)","log_ratio")
d.to_csv("merged-enrichment-refined.csv",index=False)
print("\nwrote merged-enrichment-refined.csv")
