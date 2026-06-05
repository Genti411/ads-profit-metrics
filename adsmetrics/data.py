"""Deterministic synthetic advertising + cost data per SKU. Swap for your
Amazon Advertising reports + COGS/fee data."""
from __future__ import annotations

import numpy as np
import pandas as pd


def generate(seed: int = 13, n_sku: int = 20):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_sku):
        price = round(float(rng.uniform(10, 90)), 2)
        units = int(rng.integers(20, 600))
        total_sales = round(units * price, 2)
        # a portion of sales is ad-attributed
        ad_sales = round(total_sales * float(rng.uniform(0.1, 0.6)), 2)
        impressions = int(rng.integers(2000, 80000))
        clicks = int(impressions * float(rng.uniform(0.002, 0.02)))
        cpc = float(rng.uniform(0.3, 2.5))
        ad_spend = round(clicks * cpc, 2)
        ad_orders = int(clicks * float(rng.uniform(0.03, 0.15)))
        rows.append({
            "sku": f"SKU-{3000 + i}",
            "units": units,
            "total_sales": total_sales,
            "ad_spend": ad_spend,
            "ad_sales": ad_sales,
            "impressions": impressions,
            "clicks": clicks,
            "ad_orders": ad_orders,
            "unit_cost": round(price * float(rng.uniform(0.25, 0.55)), 2),   # COGS/unit
            "referral_pct": 0.15,                                            # Amazon referral fee
            "fba_fee": round(float(rng.uniform(2.5, 6.0)), 2),               # per unit
        })
    return pd.DataFrame(rows)
