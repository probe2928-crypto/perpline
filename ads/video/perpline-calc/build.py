#!/usr/bin/env python3
"""Builds both aspect ratios of the Perpline fee-calculator ad from src/template.html.

  python3 build.py   -> index.html (9:16) + ../perpline-calc-16x9/index.html (16:9)

1080x1080 core method (luft/ads/video/HOUSE_STYLE.md §3). The phone screen is the real
/tools/futures-fee-calculator.html component rebuilt live in the DOM with the page's own
CSS values, its own VENUES table and its own calc() formula (no screenshot, no logo).
Every rate is copied from tools/futures-fee-calculator.html (VENUES, checked Oct 2026).
"""
import math, pathlib

ROOT = pathlib.Path(__file__).parent
DUR = 20.0

# copied verbatim from tools/futures-fee-calculator.html
VENUES = [("BTCC", .025, .045, 60), ("OKX", .02, .05, 40), ("Gate", .02, .05, 50), ("BingX", .02, .05, 45),
          ("OrangeX", .02, .05, 50), ("Bitget", .02, .06, 40), ("Bitunix", .02, .06, 55), ("BloFin", .02, .06, 55),
          ("Deepcoin", .04, .06, 55)]
N_POS, TRIPS = 10000, 20

def rows():
    d = []
    for name, mk, tk, rb in VENUES:
        g = N_POS * (tk / 100) * 2 * TRIPS
        d.append((name, g, g * (1 - rb / 100), rb))
    return sorted(d, key=lambda r: r[2])  # same stable sort as the page

def letters(word):
    return "".join(f'<span class="mask"><span>{c}</span></span>' for c in word)

def site(sid):
    bars = "".join(
        f'<div class="bar" data-g="{g:.2f}" data-net="{net:.2f}"><span class="n">{n}</span><div class="track"><div class="fill"></div><div class="fill reb"></div></div><span class="v">${net:,.2f}</span></div>'
        for n, g, net, rb in rows())
    return f'''<div class="site" id="{sid}"><div class="pg">
<header class="top"><span class="wordmark">Perpline</span><span class="menu-btn">Menu</span></header>
<section class="tc-hero"><span class="label">Tool · Fee calculator</span><h1>What your futures trading <em>really costs.</em></h1><p class="lede">Type your position size and how often you trade. The bars show the monthly fee on 9 exchanges at standard rates, before and after a Perpline rebate. Rates checked Oct 2026; your live account rate applies.</p></section>
<section class="tc-sec"><div class="controls">
<div class="field f-pos"><span class="label">Position size, USDT</span><div class="inp"><span class="val">10000</span><i class="caret"></i></div><span class="hint">Margin × leverage. 1,000 at 10× is 10,000.</span></div>
<div class="field f-ot"><span class="label">Order type</span><div class="seg"><span class="on">Market order</span><span>Limit order</span></div></div>
<div class="field"><span class="label">Round trips per month</span><div class="inp"><span>20</span></div></div>
<div class="check"><span class="box"><svg viewBox="0 0 18 18"><path d="M4 9.4l3.3 3.2L14 5.6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> Include Perpline rebate</div>
</div>
<div class="bars">{bars}</div>
<p class="fine">{TRIPS} round trips a month at $10,000, after rebate. The faint line is the fee before rebate. Funding not included.</p>
</section></div></div>'''

def columns():
    out = []
    for k, (n, g, net, rb) in enumerate(rows()):
        out.append(f'<div class="col" data-g="{g:.0f}" data-net="{net:.0f}" style="left:{k*110}px">'
                   f'<div class="box ghost"><i class="fr"></i><i class="sr"></i><i class="sl"></i><i class="tp"></i></div>'
                   f'<div class="box solid{" best" if k == 0 else ""}"><i class="fr"></i><i class="sr"></i><i class="sl"></i><i class="tp"></i></div>'
                   f'<b class="cv">${g:.0f}</b><span class="cn">{n}</span></div>')
    return "".join(out)

def blocks():
    return "".join(f'<div class="blk" style="left:{k*92}px"><div class="box"><i class="fr"></i><i class="sr"></i><i class="sl"></i><i class="tp"></i></div></div>' for k in range(10))

LAND_CSS = """
#s2-caps{left:-300px;top:380px;width:560px;height:300px}
.cap2{top:0;width:560px;flex-direction:column;align-items:flex-start;justify-content:flex-start;gap:12px}
.cap2 .n{font-size:28px}
.cap2 .t{font-size:70px;line-height:1.12}
#s2-capbg{display:none}
#s1-lab{top:170px}
#s1-num{top:200px}
#s1-f{top:512px}
#s1-chip{top:668px}
#s1-hook{top:770px;font-size:56px}
"""

def build(fmt):
    P = fmt == "portrait"
    if P:
        W, H, OX, OY, res, out = 1080, 1920, 0, 240, "portrait", "index.html"
    else:
        W, H, OX, OY, res, out = 1920, 1080, 420, 0, "landscape", "../perpline-calc-16x9/index.html"
    hcy = 520 if P else 540
    swoosh_y = 700
    iris_x, iris_y = 540 + 300, swoosh_y - 14
    tokens = dict(
        W=W, H=H, OX=OX, OY=OY, RES=res, DUR=DUR, S7DUR=round(DUR - 17.0, 2), LAND=0 if P else 1,
        GLOWY=round((OY + 480) / H * 100, 1),
        WM_S1=letters("PERPLINE"), WM_S7=letters("PERPLINE"),
        SITE_A=site("siteA"), SITE_B=site("siteB"), COLS=columns(), BLOCKS=blocks(),
        PHONE_SCALE=1.62 if P else 1.0, PHONE_TX=0 if P else 250,
        CH_S=.86 if P else .95, CH_Y=960 if P else 840,
        HERO_S=1.35 if P else 1.1, HERO_TOP=hcy - 330, HERO_CY=hcy,
        PUSH_S=1.1 if P else 1.0, PUSH_TX=540 if P else 600, PUSH_TY=690 if P else 560, S4CAP_Y=990 if P else 860,
        S5_CARD_Y=0 if P else 20, LEV_Y=720 if P else 700,
        SWOOSH_Y=swoosh_y, S6SUB_Y=760,
        IRISX=OX + iris_x, IRISY=OY + iris_y, IRISR=int(math.hypot(W, H)) + 40,
        E_WM_L=0 if P else -340, E_WM_T=-50 if P else 110, E_WM_W=1080 if P else 1000, E_J="center" if P else "flex-start",
        E_WM_S=124 if P else 104, E_WM_LS=.28, E_H_L=0 if P else -340, E_H_T=118 if P else 260, E_H_W=1080 if P else 1000,
        E_TA="center" if P else "left", E_H_S=84 if P else 100,
        CTA_L=76 if P else -340, CTA_Y=862 if P else 520, CTA_W=520 if P else 900, CTA_H=100, E_J2="flex-start",
        URL_L=76 if P else -340, URL_Y=806 if P else 640, URL_W=520 if P else 900, URL_TA="left",
        E_PX=560 if P else 960, E_PY=352 if P else 150, E_PS=0.92 if P else 0.9, SPEC_EXTRA=40,
        FINE_L=76 if P else -340, FINE_Y=978 if P else 720, FINE_W=470 if P else 640, FINE_TA="left",
        LEGAL_Y=1046 if P else 1030, FLOOR_P=round((OY + 1108) / H * 100, 2) if P else 92,
        EXTRA_CSS="" if P else LAND_CSS,
    )
    html = (ROOT / "src/template.html").read_text()
    for k, v in tokens.items():
        html = html.replace("{{" + k + "}}", str(v))
    assert "{{" not in html, html[html.index("{{"):html.index("{{") + 40]
    (ROOT / out).parent.mkdir(exist_ok=True)
    (ROOT / out).write_text(html)
    print("wrote", out, W, "x", H)

if __name__ == "__main__":
    for r in rows():
        print(r)
    for fmt in ("portrait", "landscape"):
        build(fmt)
