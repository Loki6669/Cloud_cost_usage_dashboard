# CLAUDE.md — Cloud Cost Usage Dashboard

Context for AI assistants working in this repository.

---

## Project Overview

**MGM Resorts Platform Economics** — a static, serverless executive dashboard for multi-cloud cost tracking (Azure, AWS, GCP), hosted on **GitHub Pages** with zero backend.

Data lives as JSON files in the `data/` folder. The dashboard **auto-discovers** and loads them at runtime via the GitHub Contents API. To add a new month, just drop a JSON file — no code changes needed.

### Live URL

```
https://Loki6669.github.io/Cloud_cost_usage_dashboard/
```

---

## Repository Structure

```
Cloud_cost_usage_dashboard/
├── index.html                      # Dashboard (HTML + CSS + JS, no build step)
├── cloud-executive-summary.html    # Original version (hardcoded data, kept for reference)
├── data/                           # Auto-discovered JSON data files
│   ├── 2025-08.json                # Monthly: Aug 2025
│   ├── 2025-09.json                # Monthly: Sep 2025
│   ├── 2025-10.json                # Monthly: Oct 2025
│   ├── 2025-11.json                # Monthly: Nov 2025
│   ├── 2025-12.json                # Monthly: Dec 2025
│   ├── 2026-01.json                # Monthly: Jan 2026 (includes top20)
│   ├── config.json                 # Static data: MCA, AI Growth, Additional Metrics
│   └── README.md                   # Data format documentation
├── HOW-TO-HOST.md                  # Hosting instructions
├── CLAUDE.md                       # This file
└── README.md                       # Project README
```

---

## How It Works

1. `index.html` is served by GitHub Pages
2. On page load, JS calls `api.github.com/repos/.../contents/data` to list all files
3. Files matching `YYYY-MM.json` are fetched as monthly cost data
4. `config.json` is fetched for static data (MCA, AI growth, etc.)
5. The `DATA` object is assembled and the dashboard renders — same UI as the original

---

## Data Format

### Monthly Files (`data/YYYY-MM.json`)

```json
{
  "month": "Feb 2026",
  "azure": { "cost": 1740906.54, "budget": 1850000 },
  "aws": { "cost": 86200, "budget": 100000 },
  "gcp": { "cost": 41200, "budget": 65000 },
  "top20": [
    { "name": "Data Services Production", "cost": 322681.04, "pct": 18.5 }
  ]
}
```

- `month`: Display label (e.g. `"Feb 2026"`)
- `azure/aws/gcp`: Each has `cost` and `budget` (numbers)
- `top20`: Optional array of top subscriptions. Dashboard uses the latest month that has it.

### Config File (`data/config.json`)

Static data updated less frequently:
- `mca`: MCA commitment (total, current, balance, note)
- `aiGrowth`: AI cost growth data points
- `additional`: Additional metrics table rows

---

## Technology Stack

| Layer | Tech |
|---|---|
| Hosting | GitHub Pages (free) |
| Frontend | Single `index.html` — vanilla HTML/CSS/JS |
| Fonts | Inter + JetBrains Mono (Google Fonts CDN) |
| Data discovery | GitHub Contents API |
| Data format | JSON files in `data/` |
| Build step | None |

---

## GitHub Pages Setup

1. Go to repo **Settings > Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, folder: `/ (root)`
4. Save — live at `https://Loki6669.github.io/Cloud_cost_usage_dashboard/`

---

## Dashboard Views

| View | Description |
|---|---|
| **Overview** | KPI cards, spend/budget table, trend bars, YTD summary, MCA progress, AI growth, additional metrics, top 10 accounts |
| **Monthly Detail** | Full month-by-month comparison table, per-cloud mini charts |
| **Accounts** | Top 20 Azure subscription bar chart + detail table + additional measurements |

### Interactive Controls
- **Month pills**: Click any month to select it
- **Cloud toggles**: Toggle AWS/Azure/GCP visibility on/off

---

## Adding a New Month (Workflow)

1. Copy `data/2026-01.json` to `data/2026-02.json`
2. Change `"month"` to `"Feb 2026"`
3. Update the cost and budget numbers
4. Optionally add/update `top20` array
5. Commit and push — done

---

## Key Code Sections in `index.html`

| Section | What It Does |
|---|---|
| `<style>` | All CSS — light theme, responsive, print-friendly |
| `detectConfig()` | Auto-detects GitHub owner/repo from Pages URL |
| `discoverFiles()` | Calls GitHub API to list `data/` contents |
| `fetchJSON()` | Fetches individual JSON files from raw.githubusercontent |
| `loadAllData()` | Orchestrates discovery + fetch + assembles DATA object |
| `buildToolbar()` | Renders month pills and cloud toggles |
| `getVisible()` | Filters DATA based on active cloud toggles |
| `render()` | Main render function — builds all views |
| `init()` | Entry point — loads data, then renders |

---

## For AI Assistants

1. **Read `index.html` before editing** — all code is in one file
2. **Data is in `data/*.json`** — never hardcode data into the HTML
3. **Keep it static** — no backend, no npm, no build tools
4. **Don't change the JSON schema** without updating the loader in JS
5. **The `detectConfig()` fallback** must match the actual GitHub owner/repo
6. **Test locally** — open `index.html` in a browser, check console for errors
7. **GitHub API rate limit** — 60 req/hour unauthenticated; don't add unnecessary API calls
8. **Update this file** if you change data format, add views, or modify architecture
