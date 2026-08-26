"""
Precompute dashboard insights for fast cold-start serving.

Runs the (expensive) model evaluation ONCE on a full-power machine and
stores everything the Insights dashboard needs as a compact JSON file at
ui/insights.json. The deployed app then renders the dashboard instantly
without touching pandas/sklearn at runtime.

If ui/insights.json already exists it is refreshed with a fresh computation.

Usage:
    python scripts/export_insights.py
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ui.app import _compute_insights, INSIGHTS_JSON  # noqa: E402


def main():
    payload = _compute_insights()
    INSIGHTS_JSON.write_text(json.dumps(payload), encoding="utf-8")

    size_kb = INSIGHTS_JSON.stat().st_size / 1024
    print("[OK] insights.json written ({:.1f} KB)".format(size_kb))
    print("     metrics: {}".format(payload["metrics"]))


if __name__ == "__main__":
    main()
