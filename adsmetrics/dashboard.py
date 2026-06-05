"""Render advertising + profitability metrics as an HTML dashboard."""
from __future__ import annotations


def _card(label: str, value: str, warn: bool = False) -> str:
    color = "#b91c1c" if warn else "#111"
    return (f'<div class="card"><div class="lbl">{label}</div>'
            f'<div class="val" style="color:{color}">{value}</div></div>')


def render(m: dict) -> str:
    s = m["summary"]
    ads = "".join([
        _card("Ad spend", f'${s["ad_spend"]:,.0f}'),
        _card("Ad sales", f'${s["ad_sales"]:,.0f}'),
        _card("ACOS", f'{s["acos_pct"]}%', s["acos_pct"] > 30),
        _card("ROAS", f'{s["roas"]}x', s["roas"] < 3),
        _card("TACOS", f'{s["tacos_pct"]}%', s["tacos_pct"] > 15),
        _card("CTR", f'{s["ctr_pct"]}%'),
        _card("CPC", f'${s["cpc"]:.2f}'),
        _card("Ad conversion", f'{s["ad_conversion_pct"]}%'),
    ])
    profit = "".join([
        _card("Total sales", f'${s["total_sales"]:,.0f}'),
        _card("COGS", f'${s["cogs"]:,.0f}'),
        _card("Referral fees", f'${s["referral_fees"]:,.0f}'),
        _card("FBA fees", f'${s["fba_fees"]:,.0f}'),
        _card("Ad spend", f'${s["ad_spend"]:,.0f}'),
        _card("Net profit", f'${s["net_profit"]:,.0f}', s["net_profit"] < 0),
        _card("Net margin", f'{s["net_margin_pct"]}%', s["net_margin_pct"] < 10),
        _card("Unprofitable SKUs", f'{s["unprofitable_skus"]}', s["unprofitable_skus"] > 0),
    ])
    rows = ""
    for r in m["skus"]:
        flag = '<span class="tag loss">LOSS</span>' if r["unprofitable"] else ""
        prof_color = "#b91c1c" if r["contribution"] < 0 else "#111"
        rows += (f'<tr><td>{r["sku"]}</td><td class="num">${r["total_sales"]:,.0f}</td>'
                 f'<td class="num">${r["ad_spend"]:,.0f}</td><td class="num">{r["acos"]}%</td>'
                 f'<td class="num">{r["roas"]}x</td>'
                 f'<td class="num" style="color:{prof_color}">${r["contribution"]:,.0f}</td>'
                 f'<td class="num">{r["net_margin"]}%</td><td>{flag}</td></tr>')
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Advertising & Profitability</title><style>
body{{font-family:system-ui,sans-serif;margin:2rem;background:#f8fafc;color:#111}}
h1,h2{{margin:0 0 1rem}} .grid{{display:flex;flex-wrap:wrap;gap:.75rem;margin-bottom:2rem}}
.card{{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1rem 1.25rem;min-width:9rem}}
.lbl{{font-size:.75rem;color:#64748b;text-transform:uppercase;letter-spacing:.04em}}
.val{{font-size:1.5rem;font-weight:700;margin-top:.25rem}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden}}
th,td{{padding:.5rem .75rem;border-bottom:1px solid #eef2f7;text-align:left;font-size:.9rem}}
th{{background:#f1f5f9;font-size:.75rem;text-transform:uppercase;color:#475569}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
.tag{{font-size:.7rem;padding:.1rem .4rem;border-radius:6px;color:#fff}} .loss{{background:#b91c1c}}
</style></head><body>
<h1>Advertising &amp; Profitability</h1>
<h2>Advertising</h2><div class="grid">{ads}</div>
<h2>Profitability</h2><div class="grid">{profit}</div>
<h2>Per-SKU (worst contribution first)</h2>
<table><thead><tr><th>SKU</th><th>Sales</th><th>Ad spend</th><th>ACOS</th><th>ROAS</th>
<th>Contribution</th><th>Margin</th><th>Flag</th></tr></thead><tbody>{rows}</tbody></table>
<p style="margin-top:1rem;color:#64748b;font-size:.8rem">JSON: <a href="/api/metrics">/api/metrics</a></p>
</body></html>"""
