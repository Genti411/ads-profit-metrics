"""Advertising & profitability KPI computation (Amazon-seller style).

Input is a per-SKU pandas DataFrame with columns:
  sku, units, total_sales, ad_spend, ad_sales, impressions, clicks, ad_orders,
  unit_cost, referral_pct, fba_fee
"""
from __future__ import annotations

import pandas as pd


def _safe(n, d):
    return float(n) / float(d) if d else 0.0


def _per_sku(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["cogs"] = d["units"] * d["unit_cost"]
    d["referral_fees"] = d["total_sales"] * d["referral_pct"]
    d["fba_fees"] = d["units"] * d["fba_fee"]
    d["acos"] = (d.apply(lambda r: _safe(r["ad_spend"], r["ad_sales"]), axis=1) * 100).round(1)
    d["roas"] = d.apply(lambda r: round(_safe(r["ad_sales"], r["ad_spend"]), 2), axis=1)
    d["contribution"] = (d["total_sales"] - d["cogs"] - d["referral_fees"]
                         - d["fba_fees"] - d["ad_spend"]).round(2)
    d["net_margin"] = (d.apply(lambda r: _safe(r["contribution"], r["total_sales"]), axis=1)
                       * 100).round(1)
    d["unprofitable"] = d["contribution"] < 0
    return d


def compute(df: pd.DataFrame) -> dict:
    d = _per_sku(df)

    ad_spend = float(d["ad_spend"].sum())
    ad_sales = float(d["ad_sales"].sum())
    impressions = int(d["impressions"].sum())
    clicks = int(d["clicks"].sum())
    total_sales = float(d["total_sales"].sum())
    cogs = float(d["cogs"].sum())
    referral = float(d["referral_fees"].sum())
    fba = float(d["fba_fees"].sum())
    net_profit = float(d["contribution"].sum())

    summary = {
        # advertising
        "ad_spend": round(ad_spend, 2),
        "ad_sales": round(ad_sales, 2),
        "impressions": impressions,
        "clicks": clicks,
        "ctr_pct": round(_safe(clicks, impressions) * 100, 2),
        "cpc": round(_safe(ad_spend, clicks), 2),
        "acos_pct": round(_safe(ad_spend, ad_sales) * 100, 1),       # ad cost of sales
        "roas": round(_safe(ad_sales, ad_spend), 2),                  # return on ad spend
        "tacos_pct": round(_safe(ad_spend, total_sales) * 100, 1),    # total ACOS
        "ad_conversion_pct": round(_safe(d["ad_orders"].sum(), clicks) * 100, 2),
        # profitability
        "total_sales": round(total_sales, 2),
        "cogs": round(cogs, 2),
        "referral_fees": round(referral, 2),
        "fba_fees": round(fba, 2),
        "gross_profit": round(total_sales - cogs, 2),
        "net_profit": round(net_profit, 2),
        "net_margin_pct": round(_safe(net_profit, total_sales) * 100, 1),
        "unprofitable_skus": int(d["unprofitable"].sum()),
    }

    cols = ["sku", "total_sales", "ad_spend", "acos", "roas", "contribution",
            "net_margin", "unprofitable"]
    skus = d.sort_values("contribution")[cols].to_dict(orient="records")
    return {"summary": summary, "skus": skus}
