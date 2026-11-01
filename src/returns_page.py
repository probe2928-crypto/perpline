"""Perpline · Returns — monthly / quarterly / yearly coin returns heatmap.
Widget + data are shared with CHAINBRIEF (same github.io origin):
  script  https://probe2928-crypto.github.io/chainbrief/returns.js
  data    https://probe2928-crypto.github.io/chainbrief/api/returns.json (refreshed every 6h by chainbrief deploy)
Public page: English with a 中文 switch (?lang=zh). Korean copy lives only in the owner-only ko/ build."""
import pathlib

CB = "https://probe2928-crypto.github.io/chainbrief/"
RT_CSS = (pathlib.Path(__file__).resolve().parent / "returns.css").read_text(encoding="utf-8")
CSS = """
.rt{--line:var(--hair);--mute:var(--muted);--f-num:var(--display);--f-label:var(--sans);--f-display:var(--display);--fs-label:11px;--fs-meta:13px;--tr-caps:.18em}
.rt-page{padding-block:clamp(48px,7vw,96px) clamp(28px,4vw,48px);border-bottom:1px solid var(--hair)}
.rt-page h1{font-size:clamp(44px,6.4vw,88px)}
.rt-page .lede{margin-top:18px;max-width:62ch}
.rt-lang{display:inline-flex;border:1px solid var(--hair);margin-top:22px}
.rt-lang button{appearance:none;border:0;background:transparent;color:var(--muted);font:500 12px var(--sans);letter-spacing:.18em;text-transform:uppercase;padding:9px 14px;cursor:pointer;min-height:40px}
.rt-lang button+button{border-left:1px solid var(--hair)}
.rt-lang button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.rt-body{padding-block:clamp(32px,5vw,56px) clamp(56px,8vw,96px)}
.rt-body .wrap{max-width:1120px}
.rt-table td{color:var(--ink)}
[data-l]{display:none}
html:not([data-rl]) [data-l="en"],html:not([data-rl]) [data-l="ko"],html[data-rl="en"] [data-l="en"],html[data-rl="zh"] [data-l="zh"],html[data-rl="ko"] [data-l="ko"]{display:revert}
""" + RT_CSS

COPY = {
    "en": ("Crypto returns, <em>month by month.</em>",
           "Bitcoin, Ether, Solana and XRP: how much each rose or fell in every month, quarter and year. Read down a column for seasonality, across a row for the shape of a year. Cards on top compare this month, quarter and year with the historical median."),
    "zh": ("加密货币收益，<em>逐月看清。</em>",
           "比特币、以太坊、Solana、XRP 每个月、每个季度、每一年涨跌多少，一张表看清。竖着看是同一月份历年的表现（季节性），横着看是当年的走势。上方卡片把本月、本季、年初至今与历史中位数对比。"),
    "ko": ("코인 수익률, <em>달마다 한눈에.</em>",
           "비트코인·이더리움·솔라나·XRP가 달마다, 분기마다, 해마다 얼마나 오르고 내렸는지 한 표로 봐요. 세로로 보면 같은 달의 해마다 성적(계절성), 가로로 보면 그해의 흐름이에요. 위 카드는 이번 달·분기·올해를 역대 중앙값과 비교해요."),
}
TITLE = {"en": "Crypto Returns Heatmap — Monthly, Quarterly & Yearly", "zh": "加密货币收益率热力图 · 月度、季度与年度", "ko": "코인 수익률 히트맵 · 월별·분기별·연도별"}

def build_returns(head, header, footer, esc, common_js, config, fab="", lang="en"):
    langs = ["ko"] if lang == "ko" else ["en", "zh"]
    h1 = "".join(f'<h1 data-l="{l}">{COPY[l][0]}</h1>' for l in langs)
    lede = "".join(f'<p class="lede" data-l="{l}">{esc(COPY[l][1])}</p>' for l in langs)
    switch = "" if lang == "ko" else '<div class="rt-lang" role="group" aria-label="Language"><button type="button" data-set="en" aria-pressed="true">EN</button><button type="button" data-set="zh" aria-pressed="false">中文</button></div>'
    js = f"""(function(){{var H=document.documentElement,R=document.getElementById("rtApp");
var l={'"ko"' if lang == "ko" else '(/[?&]lang=zh\\b/.test(location.search)?"zh":"en")'};
var T={{en:{TITLE['en']!r},zh:{TITLE['zh']!r},ko:{TITLE['ko']!r}}};
function set(x,re){{l=x;H.setAttribute("data-rl",x);document.title=T[x]+" | {config['brand']}";
[].forEach.call(document.querySelectorAll(".rt-lang [data-set]"),function(b){{b.setAttribute("aria-pressed",b.dataset.set===x?"true":"false")}});
R.setAttribute("data-lang",x);if(re&&window.RTinit)window.RTinit(R);
try{{var u=new URL(location.href);if(x==="zh")u.searchParams.set("lang","zh");else u.searchParams.delete("lang");history.replaceState(null,"",u)}}catch(e){{}}}}
set(l,false);
document.addEventListener("click",function(e){{var b=e.target.closest&&e.target.closest(".rt-lang [data-set]");if(b)set(b.dataset.set,true)}});}})();"""
    page = head(TITLE["en"] + f" | {config['brand']}",
                "Bitcoin, Ether, Solana and XRP monthly, quarterly and yearly returns in one heatmap, with month, quarter and year to date against historical medians, win rates and seasonality.",
                config["domain"] + "/returns.html") + f"""<style>{CSS}</style><!--BODY-->{header('')}
<main>
  <section class="rt-page"><div class="wrap">
    <span class="label">VIII · Les rendements</span>
    {h1}{lede}{switch}
  </div></section>
  <section class="rt-body"><div class="wrap">
    <div class="rt" id="rtApp" data-returns data-lang="{lang}" data-src="{CB}api/returns.json"></div>
  </div></section>
</main>
{footer('')}
{fab}
<script>{js}</script>
<script src="{CB}returns.js" defer></script>
<script>window.HOME="index.html"; window.LANG="en"; window.LANG_ALT="ko/returns.html";
{common_js}
btcPill();</script>"""
    return page
