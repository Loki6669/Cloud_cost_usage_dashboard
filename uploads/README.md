# Uploads Folder

Drop your raw AWS and GCP cost export files here (CSV, Excel, or JSON).

## What to upload

| File | Description |
|---|---|
| AWS cost exports | Monthly billing CSVs or Cost Explorer exports |
| GCP cost exports | BigQuery billing exports or console CSVs |
| Any other cloud cost files | Azure detail exports, etc. |

## Format (any of these work)

- AWS Cost Explorer CSV export
- GCP Billing export CSV
- Any spreadsheet with columns: Month, Cost, Budget
- Screenshots are also fine — paste them in the chat

## After uploading

Once your files are here, Claude will read them and update the
`data/YYYY-MM.json` files with your real cost and budget numbers.

---

> This folder is for **raw source data only** — the actual dashboard
> reads from `data/*.json` files, not from here.
