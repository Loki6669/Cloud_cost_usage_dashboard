# Data Files

The dashboard **automatically discovers and loads every `.json` file** in this folder. No code changes needed.

## How to Add a New Month

1. Copy any existing month file (e.g., `2026-01.json`)
2. Rename it to the new month: `2026-02.json`
3. Update the numbers inside
4. Commit and push — dashboard updates on next page load

## Monthly File Format

Filename must be `YYYY-MM.json` (e.g., `2026-02.json`).

```json
{
  "month": "Feb 2026",
  "azure": { "cost": 1740906.54, "budget": 1850000 },
  "aws": { "cost": 86200, "budget": 100000 },
  "gcp": { "cost": 41200, "budget": 65000 },
  "top20": [
    { "name": "Data Services Production", "cost": 322681.04, "pct": 18.5 },
    { "name": "CRM Personalization Prod", "cost": 147294.61, "pct": 8.5 }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `month` | Yes | Display label, e.g. `"Feb 2026"` |
| `azure.cost` | Yes | Azure total cost for the month |
| `azure.budget` | Yes | Azure budget for the month |
| `aws.cost` | Yes | AWS total cost for the month |
| `aws.budget` | Yes | AWS budget for the month |
| `gcp.cost` | Yes | GCP total cost for the month |
| `gcp.budget` | Yes | GCP budget for the month |
| `top20` | Optional | Array of top subscription objects (shown in Accounts tab). Only needed in the latest month — dashboard uses the most recent one it finds. |

## Config File (`config.json`)

Static data that doesn't change monthly lives in `config.json`:

```json
{
  "mca": { "total": 17000000, "current": 14079000, "balance": 2921000, "note": "..." },
  "aiGrowth": [{ "m": "Jul", "c": 910.36 }, ...],
  "additional": [{ "metric": "Cost to Produce", "value": "$480,523", "nov": "27.0%", "may": "27.5%" }, ...]
}
```

Update `config.json` when MCA numbers change or AI growth data is refreshed.

## File Naming

Files are sorted alphabetically, so `YYYY-MM.json` format ensures correct chronological order:
- `2025-08.json` (Aug 2025)
- `2025-09.json` (Sep 2025)
- `2026-01.json` (Jan 2026)
- `2026-02.json` (Feb 2026) — add this next!
