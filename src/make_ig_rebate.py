"""인스타그램 카루셀 5장(1080x1350) — 가이드 'How fee rebates work' 요약 (2026-11-13 5개 팀 회의 결정, 마케팅·디자인).
숫자는 가이드 본문(Bitget 공식 FAQ 11/3 확인: 0.02% maker / 0.06% taker, Perpline 40%)과 산수만. 페이백 범위는 VENUES에서 읽는다.
레퍼럴 코드 없음. 실행: python3 src/make_ig_rebate.py → ads/social/ig-2026-11-13/*.png
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
ROOT = pathlib.Path(__file__).resolve().parent.parent
import build  # noqa
from make_og import _fonts  # noqa

V = build.VENUES
LO, HI = min(v["rebate"] for v in V), max(v["rebate"] for v in V)
bitget = next(v for v in V if v["slug"] == "bitget")
TAKER, MAKER, R = bitget["taker"], bitget["maker"], bitget["rebate"]
POS = 10_000
fee1 = POS * TAKER / 100
rt = fee1 * 2
back = rt * R / 100
eff = TAKER * (1 - R / 100)
def m(x): return f"${x:,.2f}"
def p(x): return f"{x:g}%"

SLIDES = [
 ("01", "Fee rebates,", "explained in dollars.", "A rebate is a share of the trading fees you already pay, handed back to you after you trade.", ""),
 ("02", "Nothing about", "the trade changes.", f"Same exchange, same order book, same listed rate on every fill. The rebate is paid afterwards, so your real cost falls.", ""),
 ("03", f"${POS:,} trade,", "in and out.", f"As a taker at Bitget's standard {p(TAKER)}: {m(fee1)} to open, {m(fee1)} to close, {m(rt)} in total.",
  f"{R}% back = {m(back)} in USDT"),
 ("04", f"{p(TAKER)} becomes", f"{p(round(eff,4))}.", f"With {R}% returned, you effectively pay {p(round(eff,4))} on a taker fill. Through Perpline the share is {LO}–{HI}%, depending on the exchange.", "Funding payments are not covered."),
 ("05", "Only your UID.", "Never your password.", "Open a new account through our link, send the exchange name and your UID on Telegram, get paid weekly in USDT.", "Leveraged futures can wipe out your margin. A rebate lowers cost, not risk."),
]

CSS = _fonts() + """
*{box-sizing:border-box;margin:0}
body{width:1080px;height:1350px;background:#FBF4EC;color:#111;font-family:Jost,sans-serif;position:relative;overflow:hidden}
.frame{position:absolute;inset:36px;border:1px solid #E4D5C4}
.top{position:absolute;left:96px;right:96px;top:104px;display:flex;justify-content:space-between;font-size:22px;font-weight:500;letter-spacing:.32em;text-transform:uppercase}
.top span:last-child{color:#655D55;letter-spacing:.2em}
.rule{position:absolute;left:96px;top:160px;width:64px;height:2px;background:#1F2FA0}
main{position:absolute;left:96px;right:96px;top:300px}
h1{font-family:'DM Serif Display',serif;font-weight:400;font-size:112px;line-height:1.0;letter-spacing:-.01em}
h1 em{color:#1F2FA0}
.body{margin-top:72px;max-width:840px;font-size:38px;line-height:1.45;color:#2A2622}
.call{position:absolute;left:96px;right:96px;bottom:250px;padding-top:28px;border-top:1px solid #E4D5C4;font-family:'DM Serif Display',serif;font-size:50px;color:#1F2FA0}
.call.small{font-family:Jost,sans-serif;font-size:28px;color:#655D55;line-height:1.4}
.foot{position:absolute;left:96px;right:96px;bottom:110px;display:flex;justify-content:space-between;font-size:22px;letter-spacing:.24em;text-transform:uppercase;color:#655D55}
"""

def page(n, a, b, body, call):
    cls = "call small" if call and not call[0].isdigit() else "call"
    c = f'<div class="{cls}">{call}</div>' if call else ""
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            f"<div class='frame'></div><div class='top'><span>Perpline</span><span>{n} / 05</span></div><div class='rule'></div>"
            f"<main><h1>{a}<br><em>{b}</em></h1><div class='body'>{body}</div></main>{c}"
            f"<div class='foot'><span>perpline.tech</span><span>Fee rebate guide</span></div></body></html>")

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    out = ROOT / "ads/social/ig-2026-11-13"; out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1080, "height": 1350})
        for s in SLIDES:
            pg.set_content(page(*s)); pg.wait_for_timeout(700)
            pg.screenshot(path=str(out / f"rebate-{s[0]}.png"))
        br.close()
    print("ok", LO, HI, TAKER, MAKER, R, fee1, rt, back, eff)
