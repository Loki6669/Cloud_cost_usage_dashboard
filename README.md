# Cloud Cost & Usage Dashboard

A free, serverless executive dashboard for tracking multi-cloud costs (Azure, AWS, GCP). Hosted on **GitHub Pages** — no domain or hosting needed.

## Live Dashboard

```
https://Loki6669.github.io/Cloud_cost_usage_dashboard/
```

## How It Works

- Dashboard is a single `index.html` served by GitHub Pages
- Cost data lives as JSON files in the `data/` folder
- On page load, the dashboard **auto-discovers** all data files via the GitHub API
- **To add a new month**: drop a `YYYY-MM.json` file into `data/`, commit and push — that's it

## Adding New Data

1. Copy an existing file like `data/2026-01.json`
2. Rename to the new month: `data/2026-02.json`
3. Update the numbers:

```json
{
  "month": "Feb 2026",
  "azure": { "cost": 1800000, "budget": 1850000 },
  "aws": { "cost": 88000, "budget": 100000 },
  "gcp": { "cost": 42000, "budget": 65000 }
}
```

4. Commit and push to `main`

See [`data/README.md`](data/README.md) for the full data format.

## Enable GitHub Pages

1. Go to **Settings > Pages**
2. Source: Deploy from branch
3. Branch: `main` / `/ (root)`
4. Save — live in ~1 minute

## Features

- KPI summary cards (total spend, per-cloud, budget variance)
- Spend trend bar chart across all months
- Year-to-date spend with percentage breakdown
- MCA commitment progress bar
- AI growth tracking
- Top 20 account subscription breakdown
- Monthly detail comparison table
- Cloud toggle filters (show/hide AWS, Azure, GCP)
- Interactive month selector
- Fully responsive, print-friendly
