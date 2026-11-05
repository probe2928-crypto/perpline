"""Perpline · AlphaX zero-fee spotlight (EN, with 中文 switch).
Sejun's instruction 2026-11-05: push the 0% maker / 0% taker point hard, keep offer details light.
Facts used: AlphaX press release (Jul 2026) — limited-time zero-fee framework for makers and takers
in eligible regions, covering crypto perpetuals, crypto spot and USDT-margined TradFi perpetuals.
Not promoted in Korean (ko/ build is not generated for this page)."""

REF = "https://www.alphax.com/en-us/register?invite_code=7lxP6X"

CSS = """
.ax-hero{position:relative;overflow:hidden;padding-block:clamp(56px,9vw,128px) clamp(44px,6vw,80px);border-bottom:1px solid var(--hair)}
.ax-hero .label{display:block;margin-bottom:22px}
.ax-zero{display:grid;grid-template-columns:1fr 1fr;gap:clamp(16px,4vw,64px);margin:0;max-width:1000px}
.ax-zero>div{border-top:1px solid var(--ink);padding-top:14px}
.ax-zero span{display:block;font-family:var(--display);font-size:clamp(84px,15vw,220px);line-height:.86;letter-spacing:-.03em}
.ax-zero span em{font-style:italic;color:var(--tone)}
.ax-zero small{display:block;font-family:var(--sans);font-size:clamp(13px,1.4vw,15px);letter-spacing:.32em;text-transform:uppercase;color:var(--muted);margin:6px 0 18px 4px}
.ax-hero .lede{max-width:56ch;margin-top:26px;font-size:clamp(18px,1.8vw,21px)}
.ax-cta{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin-top:34px}
.ax-cta .note{font-size:13px;color:var(--muted)}
.ax-orb{position:absolute;right:-6vw;top:-10vw;width:min(38vw,460px);aspect-ratio:1;border-radius:50%;border:1px solid var(--tone);opacity:.35;pointer-events:none}
.ax-math{padding-block:clamp(48px,7vw,96px);border-bottom:1px solid var(--hair)}
.ax-math h2{font-size:clamp(34px,4.6vw,60px);max-width:18ch}
.ax-tbl{width:100%;border-collapse:collapse;margin-top:34px;font-variant-numeric:tabular-nums}
.ax-tbl th{text-align:left;font:500 11.5px var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--muted);padding:0 16px 12px 0;border-bottom:1px solid var(--ink)}
.ax-tbl td{padding:18px 16px 18px 0;border-bottom:1px solid var(--hair);font-size:17px}
.ax-tbl td.big{font-family:var(--display);font-size:clamp(26px,3vw,38px);line-height:1}
.ax-tbl tr.us td{color:var(--tone)}
.ax-math .fine{margin-top:16px;font-size:13px;color:var(--muted);max-width:70ch}
.ax-what{padding-block:clamp(48px,7vw,96px);border-bottom:1px solid var(--hair)}
.ax-grid{display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));margin-top:30px}
.ax-grid div{border-top:1px solid var(--ink);padding-top:16px}
.ax-grid b{display:block;font-family:var(--display);font-weight:400;font-size:26px;line-height:1.1;margin-bottom:8px}
.ax-grid p{margin:0;color:var(--muted);font-size:15.5px}
.ax-risk{padding-block:clamp(36px,5vw,56px) clamp(56px,8vw,96px)}
.ax-risk p{max-width:76ch;font-size:13.5px;color:var(--muted);margin:0 0 10px}
.ax-lang{display:inline-flex;border:1px solid var(--hair);margin-top:26px}
.ax-lang button{appearance:none;border:0;background:transparent;color:var(--muted);font:500 12px var(--sans);letter-spacing:.18em;text-transform:uppercase;padding:9px 14px;cursor:pointer;min-height:40px}
.ax-lang button+button{border-left:1px solid var(--hair)}
.ax-lang button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
html:not([data-al]) [data-l="zh"],html[data-al="en"] [data-l="zh"],html[data-al="zh"] [data-l="en"]{display:none!important}
@media (prefers-reduced-motion:no-preference){.ax-zero span{animation:axIn .9s cubic-bezier(.2,.8,.2,1) both}.ax-zero>div:nth-child(2) span{animation-delay:.12s}}
@keyframes axIn{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
"""

T = {
 "label": {"en": "IX · Spotlight · AlphaX", "zh": "IX · 特别推荐 · AlphaX"},
 "maker": {"en": "Maker fee", "zh": "挂单手续费"},
 "taker": {"en": "Taker fee", "zh": "吃单手续费"},
 "lede": {"en": "For a limited time, AlphaX charges nothing to trade in eligible regions. No maker fee, no taker fee, on crypto perpetuals, spot and USDT-margined TradFi perpetuals. Every basis point you used to hand the exchange stays in your P&L.",
          "zh": "限时活动：在符合条件的地区，AlphaX 交易不收手续费。加密永续、现货以及 USDT 本位的传统金融永续合约，挂单 0%、吃单 0%。以前交给交易所的每一个基点，现在都留在你的盈亏里。"},
 "cta": {"en": "Open an AlphaX account", "zh": "注册 AlphaX"},
 "ctanote": {"en": "Referral code 7lxP6X · applied automatically through this link", "zh": "邀请码 7lxP6X · 通过此链接注册自动生效"},
 "mathh": {"en": "What 0% is worth on a $100,000 trade", "zh": "一笔 10 万美元的交易，0% 意味着什么"},
 "th": {"en": ["Venue", "Open as maker", "Open as taker", "Round trip, taker"], "zh": ["交易所", "挂单开仓", "吃单开仓", "吃单开平一次"]},
 "typical": {"en": "Typical perp rate (0.02% / 0.05%)", "zh": "常见永续费率（0.02% / 0.05%）"},
 "fine": {"en": "Fees only, before funding and spread. One round trip a day at the typical taker rate is about $36,500 a year on a $100,000 position.",
          "zh": "仅计算手续费，不含资金费率与点差。按常见吃单费率，10 万美元仓位每天开平一次，一年约 36,500 美元。"},
 "whath": {"en": "Where the zero applies", "zh": "零手续费覆盖哪些市场"},
 "w": {"en": [("Crypto perpetuals", "BTC, ETH and the majors, both sides of the book at 0%."),
              ("Crypto spot", "Buy and sell spot without a trading fee."),
              ("TradFi perpetuals", "Stock, index and commodity perps, margined in USDT.")],
       "zh": [("加密永续", "BTC、ETH 等主流币，挂单吃单均为 0%。"),
              ("加密现货", "现货买卖不收交易手续费。"),
              ("传统金融永续", "股票、指数与大宗商品永续，以 USDT 保证金交易。")]},
 "risk": {"en": ["Zero-fee trading is a limited-time AlphaX programme for eligible regions; AlphaX sets and may change its terms. Funding payments and spreads still apply.",
                 "Leveraged derivatives carry a high risk of losing all of your margin, and very high leverage makes that faster. Not available in restricted jurisdictions, including South Korea and the United States. This is a referral link and Perpline may earn a commission. Nothing here is financial advice."],
          "zh": ["零手续费为 AlphaX 面向合格地区的限时计划，具体条款以 AlphaX 为准并可能调整。资金费率与点差仍会产生。",
                 "杠杆衍生品可能导致保证金全部亏损，杠杆越高风险越快。受限司法辖区（包括韩国和美国）不可使用。此为推荐链接，Perpline 可能获得佣金。本页不构成任何投资建议。"]},
}
TITLE = {"en": "AlphaX: 0% Maker, 0% Taker Crypto Trading", "zh": "AlphaX：挂单 0%、吃单 0% 的加密交易"}


def build_alphax(head, header, footer, esc, common_js, config, fab=""):
    L = ["en", "zh"]
    def each(key, tag="span", cls=""):
        c = f' class="{cls}"' if cls else ""
        return "".join(f'<{tag}{c} data-l="{l}">{esc(T[key][l])}</{tag}>' for l in L)
    rows_th = "".join(f'<tr data-l="{l}">' + "".join(f"<th>{esc(h)}</th>" for h in T["th"][l]) + "</tr>" for l in L)
    typical = "".join(f'<span data-l="{l}">{esc(T["typical"][l])}</span>' for l in L)
    grid = "".join(f'<div data-l="{l}"><b>{esc(a)}</b><p>{esc(b)}</p></div>' for l in L for a, b in T["w"][l])
    risk = "".join(f'<p data-l="{l}">{esc(p)}</p>' for l in L for p in T["risk"][l])
    js = f"""(function(){{var H=document.documentElement;var T={{en:{TITLE['en']!r},zh:{TITLE['zh']!r}}};
function set(x){{H.setAttribute("data-al",x);document.title=T[x]+" | {config['brand']}";
[].forEach.call(document.querySelectorAll(".ax-lang [data-set]"),function(b){{b.setAttribute("aria-pressed",b.dataset.set===x?"true":"false")}});
try{{var u=new URL(location.href);if(x==="zh")u.searchParams.set("lang","zh");else u.searchParams.delete("lang");history.replaceState(null,"",u)}}catch(e){{}}}}
set(/[?&]lang=zh\\b/.test(location.search)?"zh":"en");
document.addEventListener("click",function(e){{var b=e.target.closest&&e.target.closest(".ax-lang [data-set]");if(b)set(b.dataset.set)}});}})();"""
    page = head(TITLE["en"] + f" | {config['brand']}",
                "AlphaX charges 0% maker and 0% taker fees on crypto perpetuals, spot and TradFi perpetuals. See what zero fees are worth on a $100,000 trade.",
                config["domain"] + "/alphax.html") + f"""<style>{CSS}</style><!--BODY-->{header('')}
<main>
  <section class="ax-hero"><span class="ax-orb" aria-hidden="true"></span><div class="wrap">
    {each('label', 'span', 'label')}
    <h1 class="ax-zero"><div><span><em>0%</em></span>{each('maker', 'small')}</div><div><span><em>0%</em></span>{each('taker', 'small')}</div></h1>
    {each('lede', 'p', 'lede')}
    <div class="ax-cta"><a class="btn" href="{REF}" target="_blank" rel="noopener sponsored">{each('cta')} →</a>{each('ctanote', 'span', 'note')}</div>
    <div class="ax-lang" role="group" aria-label="Language"><button type="button" data-set="en" aria-pressed="true">EN</button><button type="button" data-set="zh" aria-pressed="false">中文</button></div>
  </div></section>
  <section class="ax-math"><div class="wrap">
    {each('mathh', 'h2')}
    <div style="overflow-x:auto"><table class="ax-tbl">
      <thead>{rows_th}</thead>
      <tbody>
        <tr><td>{typical}</td><td class="big">$20</td><td class="big">$50</td><td class="big">$100</td></tr>
        <tr class="us"><td>AlphaX</td><td class="big">$0</td><td class="big">$0</td><td class="big">$0</td></tr>
      </tbody>
    </table></div>
    {each('fine', 'p', 'fine')}
  </div></section>
  <section class="ax-what"><div class="wrap">
    {each('whath', 'h2')}
    <div class="ax-grid">{grid}</div>
    <div class="ax-cta"><a class="btn" href="{REF}" target="_blank" rel="noopener sponsored">{each('cta')} →</a></div>
  </div></section>
  <section class="ax-risk"><div class="wrap">{risk}</div></section>
</main>
{footer('')}
{fab}
<script>{js}</script>
<script>window.HOME="index.html"; window.LANG="en";
{common_js}
btcPill();</script>"""
    return page
