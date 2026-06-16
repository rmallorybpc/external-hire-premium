# Run Locally: collecting the financial data

A plain, step-by-step guide. No prior Python needed. The goal: run three scripts on your
own computer that pull the financial data (compensation, ROA, stock returns) and save it
as CSV files. Everything is free; nothing needs a login or an API key.

Estimated time: 30 minutes of setup, then the scripts run mostly on their own (the
compensation one runs for a few hours in the background).

---

## Step 1 — Install Python (once)

1. Go to https://www.python.org/downloads/ and install Python 3.11 or newer.
2. On the installer's first screen, **check the box "Add Python to PATH"** before clicking
   Install. (This one checkbox saves a lot of trouble later.)

To confirm it worked, open a terminal and type `python --version` (Windows) or
`python3 --version` (Mac). You should see a version number.

## Step 2 — Get the repository onto your computer

Easiest path with VS Code:
1. Open VS Code.
2. `View → Command Palette`, type "Git: Clone", paste your repo URL
   (`https://github.com/YOURNAME/external-hire-premium`), pick a folder.
3. VS Code opens the project. Use its built-in terminal: `Terminal → New Terminal`.

(If you prefer the browser: on the repo page, `Code → Download ZIP`, unzip it, then in
VS Code do `File → Open Folder` on the unzipped folder.)

## Step 3 — Install the packages the scripts need (once)

In the VS Code terminal, type this and press Enter:

```
pip install -r requirements.txt
```

If you get a message about an "externally managed environment," use this instead:

```
pip install --break-system-packages -r requirements.txt
```

That installs five free packages. It takes a minute. You only do this once.

## Step 4 — Run the three scripts, in this order

The contact email is already set in the scripts, so they will run as-is. Run them from the
`scripts` folder. In the terminal:

```
cd scripts
```

**4a. ROA (fast, ~10 minutes).** Financial performance from the SEC.
```
python sec_xbrl_roa.py
```
Produces `roa_from_xbrl.csv`. Watch for the summary line at the end telling you how many
firms matched.

**4b. Stock returns (medium, ~20 minutes).**
```
python price_tsr.py
```
Produces `tsr_from_prices.csv` and `tsr_unresolved_tickers.csv`. The "unresolved" file
lists companies that were acquired or changed their ticker symbol — those need a manual
ticker. Send me that file and I will give you the overrides to fill in, then you rerun
this one step.

**4c. Compensation (slow, runs for a few hours).** This one fetches ~1,000 proxy
documents, so start it and let it run in the background.
```
python edgar_comp_extraction.py
```
Produces `edgar_comp_matched.csv`. It is normal for some rows to be flagged for review;
the script tells you how many parsed cleanly.

## Step 5 — Send the results back

When the three CSV files exist (`roa_from_xbrl.csv`, `tsr_from_prices.csv`,
`edgar_comp_matched.csv`), commit them to the repo (VS Code: Source Control panel → type a
message → Commit → Sync) or just send them to me. I merge them, run quality checks, and we
start the analysis.

---

## If something goes wrong

- **"python: command not found"** — Python isn't on your PATH. Reinstall (Step 1) and check
  the "Add to PATH" box, or use `python3` instead of `python`.
- **"No module named ..."** — the packages didn't install. Rerun Step 3.
- **The stock script returns very little** — Yahoo sometimes rate-limits. Wait an hour and
  rerun; it picks up where it can. (This is the one step that is more reliable from a home
  internet connection than from a corporate VPN.)
- **The compensation script is slow** — that's expected. It is polite to the SEC's servers
  on purpose (a small pause between requests). Let it run.
- **Anything else** — copy the error text and send it to me; the fix is usually one line.

## What you do NOT need to do

- No GitHub Actions, no servers, no API keys, no WRDS or Bloomberg login.
- You do not need to understand the Python. You are running it, not writing it.
