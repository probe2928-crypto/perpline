"""OG 공유 이미지 생성기 (1200x630, 아이보리 톤).
assets/og.png(사이트 공통) + assets/og/<가이드 slug>.png(가이드별 제목).
숫자(최대 페이백 %, 거래소 수)는 build.py VENUES에서 읽는다 — 손으로 적지 않는다.
실행: python3 src/make_og.py  (Playwright 필요, 빌드와 별개로 소재가 바뀔 때만)
"""
import pathlib, sys, html, os, base64, glob
sys.path.insert(0, str(pathlib.Path(__file__).parent))
ROOT = pathlib.Path(__file__).resolve().parent.parent

import build  # noqa: E402  (VENUES, CONFIG)
from guides import _guides  # noqa: E402

V = build.VENUES
MAX = max(v["rebate"] for v in V)
N = len(V)

def _fonts():
    """OG_FONTS=<폴더>(@fontsource woff2)가 있으면 파일을 박아 넣고, 없으면 Google Fonts를 부른다."""
    d = os.environ.get("OG_FONTS")
    if not d:
        return "@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Jost:wght@400;500&display=swap');"
    out = []
    for fam, pat, w, st in [("DM Serif Display", "dm-serif-display-latin-400-normal", 400, "normal"),
                            ("DM Serif Display", "dm-serif-display-latin-400-italic", 400, "italic"),
                            ("Jost", "jost-latin-400-normal", 400, "normal"), ("Jost", "jost-latin-500-normal", 500, "normal")]:
        f = glob.glob(f"{d}/**/{pat}.woff2", recursive=True)[0]
        b = base64.b64encode(open(f, "rb").read()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url(data:font/woff2;base64,{b}) format('woff2')}}")
    return "".join(out)

CSS = _fonts() + """
*{box-sizing:border-box;margin:0}
body{width:1200px;height:630px;background:#FBF4EC;color:#111;font-family:Jost,sans-serif;position:relative;overflow:hidden}
.frame{position:absolute;inset:28px;border:1px solid #E4D5C4}
.top{position:absolute;left:84px;right:84px;top:72px;display:flex;justify-content:space-between;align-items:baseline;
 font-size:17px;font-weight:500;letter-spacing:.32em;text-transform:uppercase}
.top span:last-child{color:#655D55;letter-spacing:.22em;font-size:15px}
.rule{position:absolute;left:84px;top:116px;width:56px;height:2px;background:#1F2FA0}
h1{position:absolute;left:84px;right:84px;top:178px;font-family:'DM Serif Display',serif;font-weight:400;
 font-size:var(--fs,92px);line-height:1.02;letter-spacing:-.01em}
h1 em{color:#1F2FA0}
.foot{position:absolute;left:84px;right:84px;bottom:76px;display:flex;gap:0;font-size:24px;color:#111;border-top:1px solid #E4D5C4;padding-top:22px}
.foot span+span::before{content:"·";margin:0 18px;color:#655D55}
"""

def page(kicker, h1, fs):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="frame"></div>
<div class="top"><span>Perpline</span><span>{html.escape(kicker)}</span></div><div class="rule"></div>
<h1 style="--fs:{fs}px">{h1}</h1>
<div class="foot"><span>Up to {MAX}% of fees back</span><span>{N} futures exchanges</span><span>Paid weekly in USDT</span></div>
</body></html>"""

def main():
    from playwright.sync_api import sync_playwright
    jobs = [("og.png", page("Fee rebates", "Your trading fees,<br><em>returned.</em>", 112))]
    for g in _guides({v["slug"]: v for v in V}, build.pct, build.net, build.link, build.CONFIG, build.TG_DM):
        jobs.append((f"og/{g['slug']}.png", page("Guide", g["h1"].replace("<em>", "<br><em>", 1), 84)))
    (ROOT / "assets" / "og").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        for name, doc in jobs:
            pg.set_content(doc, wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.screenshot(path=str(ROOT / "assets" / name))
            print("wrote", name)
        b.close()

if __name__ == "__main__":
    main()
