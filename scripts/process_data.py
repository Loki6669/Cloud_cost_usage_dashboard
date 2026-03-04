#!/usr/bin/env python3
"""
process_data.py — Cloud Cost CSV → JSON converter
==================================================
Run this script whenever you upload new CSV files. It automatically
reads every CSV in data/aws/, data/azure/, and data/gcp/ and writes
one JSON file per month into data/.

Usage (from repo root):
    python3 scripts/process_data.py

CSV naming convention expected:
    data/aws/cost_aws_monthly_MMYYYY.csv
    data/azure/cost_azure_monthly_MMYYYY.csv
    data/gcp/cost_gcp_monthly_MMYYYY.csv

Example: cost_azure_monthly_022026.csv  → data/2026-02.json

config.json is created only if it doesn't already exist — edit it
manually to update MCA commitment, AI growth, and additional metrics.
"""

import csv
import io
import json
import os
import re
from collections import defaultdict

# ── Paths ──────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

# ── Budget targets — update these when targets change ─────────────────
# Add a new entry for each month if the budget differs from the default.
AZURE_BUDGETS = {
    '2025-08': 1500000,
    '2025-09': 1500000,
    '2025-10': 1500000,
    '2025-11': 1500000,
    '2025-12': 1850000,
    '2026-01': 1850000,
    # '2026-02': 1850000,   ← add new months here
}
AZURE_BUDGET_DEFAULT = 1850000  # fallback for months not listed above

AWS_BUDGETS = {}               # per-month overrides (empty = all use default)
AWS_BUDGET_DEFAULT = 100000

GCP_BUDGETS = {}
GCP_BUDGET_DEFAULT = 65000

# ── Month display labels ────────────────────────────────────────────────
_LABELS = {
    '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec',
}

def _key_to_label(key):
    """'2026-02' → 'Feb 2026'"""
    yyyy, mm = key.split('-')
    return f"{_LABELS[mm]} {yyyy}"


def _parse_key(fname):
    """Extract YYYY-MM key from filename like cost_aws_monthly_022026.csv"""
    m = re.search(r'(\d{2})(\d{4})', fname)
    return f"{m.group(2)}-{m.group(1)}" if m else None


# ── Cloud parsers ──────────────────────────────────────────────────────

def parse_aws(folder):
    """
    AWS Cost Explorer export format:
      Row 0: "Linked account" header with account IDs
      Row 1: Account names
      Row 2: "Linked account total" with per-account totals (last column = grand total)
      Row 3+: Daily breakdown rows

    Returns: {key: total_cost}
    """
    totals = {}
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith('.csv'):
            continue
        key = _parse_key(fname)
        if not key:
            print(f"  SKIP (no date in filename): {fname}")
            continue
        path = os.path.join(folder, fname)
        with open(path, encoding='utf-8-sig') as f:
            lines = f.readlines()
        if len(lines) < 3:
            print(f"  SKIP (too few rows): {fname}")
            continue
        cols = next(csv.reader(io.StringIO(lines[2])))
        try:
            totals[key] = round(float(cols[-1]), 2)
        except (ValueError, IndexError):
            print(f"  WARNING: Could not parse AWS total from {fname}")
    return totals


def parse_azure(folder):
    """
    Azure Cost Management export format:
      CSV with header row containing: UsageDate, SubscriptionName, CostUSD, Cost, Currency

    Groups by SubscriptionName, sums CostUSD, derives top 20.
    Returns: {key: (total_cost, top20_list)}
    """
    results = {}
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith('.csv'):
            continue
        key = _parse_key(fname)
        if not key:
            print(f"  SKIP (no date in filename): {fname}")
            continue
        path = os.path.join(folder, fname)
        subs = defaultdict(float)
        with open(path, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = (row.get('SubscriptionName') or '').strip()
                try:
                    cost = float(row.get('CostUSD') or 0)
                except (ValueError, TypeError):
                    cost = 0.0
                if name and cost > 0:
                    subs[name] += cost
        total = sum(subs.values())
        sorted_subs = sorted(subs.items(), key=lambda x: x[1], reverse=True)[:20]
        top20 = [
            {"name": n, "cost": round(c, 2), "pct": round(c / total * 100, 1)}
            for n, c in sorted_subs
        ] if total > 0 else []
        results[key] = (round(total, 2), top20)
    return results


def parse_gcp(folder):
    """
    GCP Billing export format:
      CSV with header row containing: Project name, Project ID, ..., Cost ($), ...

    Returns: {key: total_cost}
    """
    totals = {}
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith('.csv'):
            continue
        key = _parse_key(fname)
        if not key:
            print(f"  SKIP (no date in filename): {fname}")
            continue
        path = os.path.join(folder, fname)
        total = 0.0
        with open(path, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    total += float(row.get('Cost ($)') or 0)
                except (ValueError, TypeError):
                    pass
        totals[key] = round(total, 2)
    return totals


# ── Main ───────────────────────────────────────────────────────────────

def main():
    aws_dir   = os.path.join(DATA, 'aws')
    azure_dir = os.path.join(DATA, 'azure')
    gcp_dir   = os.path.join(DATA, 'gcp')

    print("=" * 60)
    print("Cloud Cost CSV → JSON Processor")
    print("=" * 60)

    print("\nParsing CSVs…")
    aws   = parse_aws(aws_dir)   if os.path.isdir(aws_dir)   else {}
    azure = parse_azure(azure_dir) if os.path.isdir(azure_dir) else {}
    gcp   = parse_gcp(gcp_dir)  if os.path.isdir(gcp_dir)  else {}

    all_keys = sorted(set(aws) | set(azure) | set(gcp))
    if not all_keys:
        print("\nNo CSV files found.")
        print("Place CSVs in data/aws/, data/azure/, data/gcp/")
        print("Naming: cost_aws_monthly_MMYYYY.csv (e.g. cost_aws_monthly_022026.csv)")
        return

    print(f"\nFound {len(all_keys)} month(s): {', '.join(all_keys)}")
    print("\nGenerating JSON files…")

    for key in all_keys:
        az_cost, az_top20 = azure.get(key, (0, []))
        aw_cost = aws.get(key, 0)
        gc_cost = gcp.get(key, 0)

        az_bud = AZURE_BUDGETS.get(key, AZURE_BUDGET_DEFAULT)
        aw_bud = AWS_BUDGETS.get(key, AWS_BUDGET_DEFAULT)
        gc_bud = GCP_BUDGETS.get(key, GCP_BUDGET_DEFAULT)

        data = {
            "month": _key_to_label(key),
            "azure": {"cost": az_cost, "budget": az_bud},
            "aws":   {"cost": aw_cost, "budget": aw_bud},
            "gcp":   {"cost": gc_cost, "budget": gc_bud},
            "top20": az_top20,
        }

        out_path = os.path.join(DATA, f"{key}.json")
        with open(out_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"  ✓ {key}.json  "
              f"Azure=${az_cost:>14,.2f}  "
              f"AWS=${aw_cost:>10,.2f}  "
              f"GCP=${gc_cost:>8,.2f}  "
              f"Top20={len(az_top20)}")

    # Write config.json only if missing
    config_path = os.path.join(DATA, 'config.json')
    if not os.path.exists(config_path):
        config = {
            "mca": {
                "total": 17000000,
                "current": 14079000,
                "balance": 2921000,
                "note": "*Brings us to end of March; MCA ends in May"
            },
            "aiGrowth": [
                {"m": "Jul", "c": 910.36},
                {"m": "Aug", "c": 2249.17},
                {"m": "Sep", "c": 5763.19},
                {"m": "Oct", "c": 10513.91}
            ],
            "additional": [
                {"metric": "Cost to Produce",       "value": "$480,523",        "nov": "27.0%", "may": "27.5%"},
                {"metric": "Cost to Serve",         "value": "$1,299,857",      "nov": "73.0%", "may": "72.5%"},
                {"metric": "Reservation Coverage",  "value": "20 Reservations", "nov": "72.4%", "may": "43.2%"},
                {"metric": "Top 20 Accts (of 215)", "value": "% of overall",    "nov": "71.0%", "may": "71.8%"}
            ]
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n  ✓ config.json created (edit to update MCA/AI growth data)")
    else:
        print(f"\n  ↷ config.json already exists — not overwritten")

    # Always rewrite manifest.json so the dashboard can discover files
    # without hitting the GitHub API (avoids rate limits & works on private repos)
    manifest_files = [f"{k}.json" for k in all_keys] + ["config.json"]
    manifest_path = os.path.join(DATA, 'manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump({"files": manifest_files}, f, indent=2)
    print(f"  ✓ manifest.json updated ({len(manifest_files)} entries)")

    print(f"\nDone! {len(all_keys)} JSON file(s) written to data/")
    print("Commit and push to update the live dashboard.\n")


if __name__ == '__main__':
    main()
