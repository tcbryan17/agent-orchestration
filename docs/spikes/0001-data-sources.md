# Spike 0001: data sources for "football finance analyst"

- **Date:** 2026-11-14
- **Question:** Can the agents get reliable, gradeable financial data for Premier League clubs and betting operators?
- **Method:** three research subagents (Sonnet ×2, Haiku ×1) working from public web pages, with no API keys. Every finding below carries a confidence level; anything not checked against a primary source is marked **unverified**.

## 1. Betting operators and Manchester United: SEC EDGAR

| Company | CIK | Latest annual report | FYE | Standard |
|---|---|---|---|---|
| DraftKings | 1883685 | 10-K FY2025, filed 2026-02-13 | Dec 31 | US GAAP |
| Flutter Entertainment | 1635327 | 10-K FY2025, filed Feb 2026 (26th vs 27th **unverified**) | Dec 31 | US GAAP (10-K filer since FY2023) |
| Rush Street Interactive | 1793659 | 10-K FY2025 (filing date **unverified**) | Dec 31 | US GAAP |
| Manchester United plc | 1549107 | 20-F FY ended 30 Jun 2026 (**unverified**); FY2025 20-F confirmed | Jun 30 | IFRS (IASB) |

- **Free XBRL API.** `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` (CIK zero-padded to 10 digits).
- **Access requirements.** Requests need a User-Agent of the form `Name contact@domain`, and the limit is 10 requests/s.
- **Verdict: structured, machine-readable and gradeable.** The `companyfacts` endpoint covers both US GAAP and IFRS (`ifrs-full`) filers.

## 2. Other Premier League clubs: Companies House

| Club | Reporting entity (number) | Latest accounts (period end, filed) | Format |
|---|---|---|---|
| Arsenal | Arsenal Holdings Ltd (04250459) | 31 May 2025, filed 27 Feb 2026 | **Image-only scanned PDF** |
| Liverpool | The Liverpool FC and Athletic Grounds Ltd (00035668) | 31 May 2025, filed 4 Mar 2026 | **Image-only scanned PDF** |
| Manchester City | Manchester City FC Ltd (00040946) | 30 Jun 2025, filed 6 Mar 2026 | **Image-only scanned PDF** |
| Chelsea | Chelsea FC Ltd (01965149) | 30 Jun 2025, filed 12 Apr 2026 | **Image-only scanned PDF** |
| Tottenham | Tottenham Hotspur Football & Athletic Co. Ltd (00057186) | 30 Jun 2025, filed 9 Apr 2026 | **Image-only scanned PDF** |
| Newcastle | Newcastle United Football Company Ltd (00031014) | 30 Jun 2025, filed 13 Apr 2026 | **Image-only scanned PDF** |

- **All six PDFs are images with no text layer** (produced by `tiff2pdf`). Requests for the iXBRL version returned errors. So the free bulk "Accounts Data Product", which holds only electronically filed accounts, almost certainly doesn't contain them.
- **The data arrives up to about 10 months after year end.** For example, Arsenal's accounts for May 2025 were filed in February 2026.
- **The accounting framework is probably FRS 102 (UK GAAP)**, but that's **unverified**; nobody has read the accounting-policy notes yet.
- **Companies House API.** The key is free and sent as the HTTP Basic auth username. The limit is 600 requests per 5 minutes. The endpoints are `filing-history`, then `document/{id}/content`.
- **Verdict:** clubs need a **vision-extraction step plus human verification**. They can't be live tool calls against structured data.

## 3. Premier League rules context (2026/27)

- **Spending rules.** PSR (£105m loss limit over 3 years) applied through 2025/26. From **2026/27 the Squad Cost Ratio (SCR)** replaces it: squad costs may be at most **85% of football revenue plus net profit on player sales**, with a multi-year 30% allowance subject to a levy. *Source: Premier League statement; high confidence.* The levy's size and when it starts are **unverified**.
- **What squad costs include.** Reportedly wages, amortisation of player registrations, and agent fees (medium confidence). All three are computable from accounts, so the Analyst has a real calculation to do.
- **UEFA.** UEFA's separate rule caps squad costs at 70% for clubs playing in European competition.
- **Gambling sponsors.** From **2026/27, gambling sponsors are banned from the front of shirts**; sleeves and partnership deals are still allowed. Several deals have moved to sleeves (medium confidence). The list of clubs with gambling shirt sponsors in 2025/26 is **unverified**.
- **Reference sources.** The Deloitte Football Money League and UEFA's finance landscape report are copyrighted. Cite individual figures with attribution; don't bulk-copy them.

## 4. Implications for design and governance

1. **Two kinds of data path.** Operators and Man Utd are fetched by live tool calls against structured XBRL. Clubs come from an *offline, human-verified dataset* extracted from scans. Specialist agents exist because the data sources genuinely differ, not for show.
2. **Three accounting standards** (US GAAP, IFRS, likely FRS 102). Comparing across them is a finance control the Reviewer should enforce.
3. **Fiscal years don't line up** (Dec, Jun, May). Periods have to be aligned before any comparison.
4. **The scanned-PDF extraction is itself an AI step with a governance story.** It needs data lineage (page number for each figure), human verification before use, and a measured extraction-accuracy rate. Those fit ISO 42001's data and lifecycle topics and NIST AI RMF's MEASURE function.

## Still to verify (once keys are in `.env`)
- Flutter's and Rush Street's filing dates, and whether Man Utd's FY2026 20-F is on the `companyfacts` API.
- Each club's accounting framework, read from the accounting-policy note.
- Document metadata for each club through the Companies House Document API, to confirm only a PDF exists.
