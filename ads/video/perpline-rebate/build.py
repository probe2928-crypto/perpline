#!/usr/bin/env python3
"""Builds both aspect ratios of the Perpline rebate ad from src/template.html.

  python3 build.py   -> index.html (9:16) + ../perpline-rebate-16x9/index.html (16:9)

1080x1080 core method (luft/ads/video/HOUSE_STYLE.md §3). Phone screens are real
captures of perpline.tech (light theme, promo strip and chat button hidden, exchange
logos not loaded, so no third-party logo appears). Every rate is from src/build.py VENUES.
"""
import math, pathlib, random

ROOT = pathlib.Path(__file__).parent
DUR = 20.0

def letters(word):
    return "".join(f'<span class="mask"><span>{c}</span></span>' for c in word)

def week():
    rnd = random.Random(20261110)
    out = []
    for k, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon"]):
        pay = k == 7
        bars = "" if pay else "".join(f'<i style="height:{rnd.randint(90, 370) if k < 5 else rnd.randint(50, 210)}px"></i>' for _ in range(3))
        out.append(f'<div class="dc{" pay" if pay else ""}" style="left:{k*122}px"><div class="bars">{bars}</div><div class="d">{d}</div></div>')
    return "".join(out)

LAND_CSS = """
#s2-caps{left:-300px;top:380px;width:560px;height:300px}
.cap2{top:0;width:560px;flex-direction:column;align-items:flex-start;justify-content:flex-start;gap:12px}
.cap2 .n{font-size:28px}
.cap2 .t{font-size:70px;line-height:1.12}
#s2-capbg{display:none}
#s3-stage{-webkit-mask-image:none;mask-image:none}
"""

def build(fmt):
    P = fmt == "portrait"
    if P:
        W, H, OX, OY, res, out = 1080, 1920, 0, 240, "portrait", "index.html"
    else:
        W, H, OX, OY, res, out = 1920, 1080, 420, 0, "landscape", "../perpline-rebate-16x9/index.html"
    hcy = 520 if P else 540
    swoosh_y = 700
    iris_x, iris_y = 540 + 330, swoosh_y - 14
    tokens = dict(
        W=W, H=H, OX=OX, OY=OY, RES=res, DUR=DUR, S7DUR=round(DUR - 17.0, 2), LAND=0 if P else 1,
        GLOWY=round((OY + 480) / H * 100, 1),
        WM_S1=letters("PERPLINE"), WM_S7=letters("PERPLINE"),
        S1_WM_Y=60, S1_LAB_Y=250, S1_NUM_Y=300, S1_HOOK_Y=640,
        PHONE_SCALE=1.62 if P else 1.0, PHONE_TX=0 if P else 250,
        RING_S=1.4 if P else 1.15, RING_Y=590 if P else 520, NAMES_Y=962 if P else 900,
        HERO_S=1.35 if P else 1.1, HERO_TOP=hcy - 330, HERO_CY=hcy,
        PUSH_S=1.75 if P else 1.9, PUSH_TX=540 if P else 600, PUSH_TY=250 if P else 330, S4CAP_Y=480,
        S5_CARD_Y=0 if P else 20, WEEK_Y=380 if P else 400, COIN_X=7 * 122 + 53, PAYLAB_X=860,
        WEEK=week(), SWOOSH_Y=swoosh_y, S6SUB_Y=760,
        IRISX=OX + iris_x, IRISY=OY + iris_y, IRISR=int(math.hypot(W, H)) + 40,
        E_WM_L=0 if P else -340, E_WM_T=-66 if P else 110, E_WM_W=1080 if P else 1000, E_J="center" if P else "flex-start",
        E_WM_S=124 if P else 104, E_WM_LS=.28, E_H_L=0 if P else -340, E_H_T=104 if P else 260, E_H_W=1080 if P else 1000,
        E_TA="center" if P else "left", E_H_S=84 if P else 104,
        CTA_L=80 if P else -340, CTA_Y=972 if P else 520, CTA_W=520 if P else 900, CTA_H=100, E_J2="flex-start",
        URL_L=80 if P else -340, URL_Y=912 if P else 640, URL_W=520 if P else 900, URL_TA="left",
        E_PX=618 if P else 1030, E_PY=318 if P else 100, E_PS=0.9 if P else 0.98, SPEC_EXTRA=40,
        FINE_L=40 if P else -340, FINE_Y=1104 if P else 720, FINE_W=1000 if P else 640, FINE_TA="center" if P else "left",
        LEGAL_Y=1046 if P else 1030, FLOOR_P=round((OY + 1180) / H * 100, 2) if P else 92,
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
    for fmt in ("portrait", "landscape"):
        build(fmt)
