import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from adsmetrics.metrics import compute


def _df():
    return pd.DataFrame([
        {"sku": "A", "units": 100, "total_sales": 1000, "ad_spend": 100, "ad_sales": 400,
         "impressions": 10000, "clicks": 200, "ad_orders": 20, "unit_cost": 3,
         "referral_pct": 0.15, "fba_fee": 2},
        {"sku": "B", "units": 50, "total_sales": 200, "ad_spend": 150, "ad_sales": 100,
         "impressions": 5000, "clicks": 100, "ad_orders": 5, "unit_cost": 2,
         "referral_pct": 0.15, "fba_fee": 3},
    ])


def test_advertising_metrics():
    s = compute(_df())["summary"]
    assert s["acos_pct"] == 50.0        # spend 250 / ad_sales 500
    assert s["roas"] == 2.0             # 500 / 250
    assert s["tacos_pct"] == 20.8       # 250 / 1200
    assert s["ctr_pct"] == 2.0          # 300 / 15000
    assert s["cpc"] == 0.83             # 250 / 300
    assert s["ad_conversion_pct"] == round(25 / 300 * 100, 2)


def test_profitability_metrics():
    s = compute(_df())["summary"]
    assert s["cogs"] == 400.0           # 100*3 + 50*2
    assert s["referral_fees"] == 180.0  # 15% of 1200
    assert s["fba_fees"] == 350.0       # 100*2 + 50*3
    assert s["net_profit"] == 20.0      # 250 + (-230)
    assert s["net_margin_pct"] == 1.7   # 20 / 1200
    assert s["unprofitable_skus"] == 1


def test_per_sku_sorted_worst_first():
    skus = compute(_df())["skus"]
    assert skus[0]["sku"] == "B" and skus[0]["unprofitable"] is True
    assert skus[0]["contribution"] == -230.0
    assert skus[1]["sku"] == "A"
    assert skus[1]["contribution"] == 250.0
    assert skus[1]["acos"] == 25.0 and skus[1]["roas"] == 4.0 and skus[1]["net_margin"] == 25.0
