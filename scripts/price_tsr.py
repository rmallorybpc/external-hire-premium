"""
Free-price TSR fetcher: the no-subscription return layer for the External Hire Premium study.

Computes total shareholder return over the event window (default -2yr to +3yr around the
appointment date), raw and market-adjusted, from free public price data. No WRDS, no paid
feed.

Price source priority (configurable):
  1. yfinance  -> 'Close' with auto_adjust=True is split- AND dividend-adjusted, which is
     true TSR (price appreciation + reinvested dividends). Best choice. (pip install yfinance)
  2. Stooq     -> no key, direct CSV; split-adjusted close. Use as fallback; note that
     Stooq's adjustment of dividends is less complete, so a Stooq-only figure is closer to
     price return than full TSR. Flag the source per row.

Market benchmark: S&P 500 (^GSPC via yfinance, or ^spx via Stooq) over the same window,
for the market-adjusted (abnormal) return.

Ticker resolution: the panel carries CIK, not ticker. This maps current CIK->ticker via
SEC company_tickers.json. Firms that were acquired or changed ticker before/after the
window will not resolve to a current ticker and are written out to a manual-ticker queue;
supply a `ticker` column in the panel (or a ticker_overrides.csv) for those.

Inputs : wrds_panel_gvkeys.csv  (cik, appt_date, target years)
Output : tsr_from_prices.csv     (raw and market-adjusted window returns, source, status)
         tsr_unresolved_tickers.csv (rows needing a manual ticker)
"""

import sys, time, io
import pandas as pd
import requests

CONTACT = "External Hire Premium research <ross@themallorygroup.ai>"
HEADERS = {"User-Agent": CONTACT}
SOURCE = "yfinance"          # "yfinance" or "stooq"
YRS_BEFORE, YRS_AFTER = 2, 3

CT_URL = "https://www.sec.gov/files/company_tickers.json"

def cik_to_ticker_map():
    r = requests.get(CT_URL, headers=HEADERS, timeout=30); r.raise_for_status()
    j = r.json()
    return {int(v["cik_str"]): v["ticker"] for v in j.values()}

# ---- price backends --------------------------------------------------
def prices_yf(ticker, start, end):
    import yfinance as yf
    df = yf.download(ticker, start=start, end=end, auto_adjust=True,
                     progress=False, threads=False)
    if df is None or len(df) == 0:
        return None
    s = df["Close"].dropna()
    return s

def prices_stooq(ticker, start, end):
    url = (f"https://stooq.com/q/d/l/?s={ticker.lower()}.us"
           f"&d1={start.strftime('%Y%m%d')}&d2={end.strftime('%Y%m%d')}&i=d")
    time.sleep(0.2)
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code != 200 or "Date" not in r.text[:50]:
        return None
    df = pd.read_csv(io.StringIO(r.text))
    if "Close" not in df or len(df) == 0:
        return None
    df["Date"] = pd.to_datetime(df["Date"])
    return df.set_index("Date")["Close"].dropna()

def get_prices(ticker, start, end):
    return prices_yf(ticker, start, end) if SOURCE == "yfinance" else prices_stooq(ticker, start, end)

def window_return(series):
    if series is None or len(series) < 2:
        return None
    return float(series.iloc[-1] / series.iloc[0] - 1.0)

# ---- main ------------------------------------------------------------
def run(panel_path="wrds_panel_gvkeys.csv", overrides_path=None):
    panel = pd.read_csv(panel_path)
    panel = panel.dropna(subset=["cik"]).copy()
    panel["cik"] = panel["cik"].astype(int)
    ctmap = cik_to_ticker_map()
    overrides = {}
    if overrides_path:
        ov = pd.read_csv(overrides_path)
        overrides = dict(zip(ov["transition_id"], ov["ticker"]))

    # market benchmark over full span (pull once, slice per window)
    span_start = pd.Timestamp(panel["appt_date"].min()) - pd.DateOffset(years=YRS_BEFORE+1)
    span_end   = pd.Timestamp(panel["appt_date"].max()) + pd.DateOffset(years=YRS_AFTER+1)
    mkt_ticker = "^GSPC" if SOURCE == "yfinance" else "^spx"
    mkt = get_prices(mkt_ticker, span_start, span_end)

    rows, unresolved = [], []
    for _, p in panel.iterrows():
        tid = p["transition_id"]
        ticker = overrides.get(tid) or ctmap.get(int(p["cik"]))
        if not ticker:
            unresolved.append({"transition_id": tid, "cik": p["cik"], "coname": p["coname"]})
            rows.append({"transition_id": tid, "coname": p["coname"], "status": "no-ticker"})
            continue
        appt = pd.Timestamp(p["appt_date"])
        start, end = appt - pd.DateOffset(years=YRS_BEFORE), appt + pd.DateOffset(years=YRS_AFTER)
        try:
            s = get_prices(ticker, start, end)
        except Exception as ex:
            rows.append({"transition_id": tid, "coname": p["coname"], "ticker": ticker,
                         "status": f"price-error:{ex}"}); continue
        raw = window_return(s)
        mkt_win = window_return(mkt.loc[start:end]) if mkt is not None else None
        rows.append({
            "transition_id": tid, "coname": p["coname"], "ticker": ticker,
            "classification": p["classification"],
            "window_start": start.date(), "window_end": end.date(),
            "tsr_raw": raw, "mkt_return": mkt_win,
            "tsr_mktadj": (raw - mkt_win) if (raw is not None and mkt_win is not None) else None,
            "price_source": SOURCE,
            "status": "ok" if raw is not None else "no-price-data",
        })
    pd.DataFrame(rows).to_csv("tsr_from_prices.csv", index=False)
    pd.DataFrame(unresolved).to_csv("tsr_unresolved_tickers.csv", index=False)
    ok = sum(r.get("status") == "ok" for r in rows)
    print(f"TSR from prices ({SOURCE}): {len(rows)} transitions, {ok} computed.")
    print(f"Unresolved tickers (acquired/renamed firms): {len(unresolved)} "
          f"-> tsr_unresolved_tickers.csv; supply a ticker_overrides.csv and rerun.")
    if SOURCE == "stooq":
        print("NOTE: Stooq close is split-adjusted; dividend adjustment is partial, so these")
        print("are closer to price return than full TSR. Use yfinance for dividend-inclusive TSR.")

if __name__ == "__main__":
    if CONTACT.startswith("External Hire Premium research <your-email"):
        sys.exit("EDIT the CONTACT variable with your real email before running.")
    run()
