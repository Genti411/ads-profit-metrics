# Advertising & Profitability Metrics

An Amazon-seller-style analytics service tying **ad performance** to **bottom-line
profitability**. A pandas engine computes the KPIs per SKU and in aggregate; a
FastAPI app serves JSON and an HTML dashboard that flags unprofitable SKUs.

| Area | What's shown |
|------|--------------|
| **Data analytics** | per-SKU + portfolio rollups, profit waterfall |
| **Advertising metrics** | ACOS, ROAS, TACOS, CTR, CPC, ad conversion |
| **Profitability** | COGS, referral + FBA fees, contribution margin, net profit/margin |

## Metrics

**Advertising:** ad spend, ad sales, impressions, clicks, **CTR**, **CPC**,
**ACOS** (`ad_spend / ad_sales`), **ROAS** (`ad_sales / ad_spend`), **TACOS**
(`ad_spend / total_sales`), ad conversion.
**Profitability:** total sales, COGS, referral fees, FBA fees, gross profit,
**net profit** (contribution = `sales − COGS − fees − ad_spend`), **net margin**,
and a count of **unprofitable SKUs**. The per-SKU table is sorted worst-first and
flags any SKU losing money.

## Run

```bash
docker build -t ads-profit-metrics . && docker run --rm -p 8000:8000 ads-profit-metrics
# dashboard: http://localhost:8000      JSON: http://localhost:8000/api/metrics
```

Loads deterministic synthetic data on startup; replace `adsmetrics/data.py` with
your Amazon Advertising report joined to COGS/fee data (same columns).

## Tests

```bash
pip install -r requirements.txt pytest && python -m pytest
```

Tests assert ACOS, ROAS, TACOS, CTR, CPC, COGS, fees, contribution, net margin,
and the worst-first SKU ranking on hand-checked inputs.

## Layout

```
adsmetrics/metrics.py    pandas advertising + profitability engine (pure)
adsmetrics/data.py       synthetic ad + cost data
adsmetrics/dashboard.py  HTML dashboard (ad + profit sections)
adsmetrics/app.py        FastAPI (/, /api/metrics, /healthz)
tests/                   metric-formula tests
```
