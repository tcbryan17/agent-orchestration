# Data card

*Describes each data source: where it came from, how it was processed, what is missing. Fill in as sources are built. Facts below come from `docs/spikes/0001-data-sources.md`; those marked "unverified" there are marked "to verify" here.*

## Source 1: SEC EDGAR XBRL (Stage 1)
| Item | Detail |
|---|---|
| What | `companyfacts` JSON from `data.sec.gov` for DraftKings, Flutter, Rush Street, Manchester United |
| Standards | US GAAP for the first three; IFRS (`ifrs-full`) for Manchester United (20-F) |
| Access | Free API. The request must send a `User-Agent` with a name and contact. Limit 10 requests per second |
| Licence and attribution | SEC filings are public. Licence and reuse terms to verify; cite the filing in outputs |
| Fiscal years | Dec year end for the first three; Manchester United is 30 June |
| Processing | Fetched live by the `edgar` tool; no copy kept except test fixtures |
| Known gaps | Filing dates for Flutter and Rush Street, and whether Manchester United's latest 20-F is in `companyfacts`: to verify |

## Source 2: Companies House club dataset (Stage 2)
| Item | Detail |
|---|---|
| What | Figures for about six Premier League clubs (Arsenal, Liverpool, Manchester City, Chelsea, Tottenham, Newcastle) |
| Origin | Scanned PDFs from Companies House (image-only, no text layer) |
| Method | Extracted once by a vision model, then checked line by line by the owner; each figure has a source page reference |
| Access | Companies House API key; limit 600 requests per 5 minutes |
| Licence and attribution | Companies House data terms (Open Government Licence or similar) to verify |
| Accuracy | Extraction accuracy rate to record here after verification |
| Known gaps | Accounts lag year end by up to about 10 months; period ends in May and June, not December; accounting framework probably FRS 102, to verify; the scanned PDFs are not committed |

## Other material
The Deloitte Football Money League and UEFA reports are copyrighted. Cite individual figures with attribution. Never copy text in bulk.

## Personal data present
Filings can name directors and report their pay (for example remuneration tables and signatures). This is personal data under GDPR. See `gdpr.md` and C4/C5 for minimisation. *Record which fields you keep, which you drop, and why.*

## Known gaps summary
| Gap | Effect | Mitigation |
|---|---|---|
| (example) Fiscal year ends differ | Periods do not line up | Analyst aligns periods; Reviewer checks |
