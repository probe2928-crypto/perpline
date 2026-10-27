#!/usr/bin/env python3
"""Perpline static site builder.
Edit CONFIG / VENUES below, then run:  python3 build.py
Output goes to ../site/  (upload that folder to Cloudflare Pages).
"""
import json, html, os, pathlib, datetime, re

OUT = pathlib.Path(__file__).resolve().parent.parent  # repo root = site

# ============ CONFIG ============
CONFIG = {
    "domain": "https://probe2928-crypto.github.io/perpline",  # change to your real domain later
    "brand": "Perpline",
    "telegram_dm": "btcbullit",                # 1:1 support
    "telegram_group_url": "https://t.me/+_QeSr3G2JGYxMmJl",   # community group invite link
    "telegram_group_name": "Perpline Community",
    "track_base": "",                          # your Worker URL, e.g. https://perpline-api.xxx.workers.dev  (empty = direct links)
    "form_endpoint": "",                       # same Worker URL (CS form posts here). Empty = opens Telegram
    "fees_checked": "Oct 2026",
    "edition": "Édition No. 01 · Octobre 2026",
}

# rebate = % of the trading fees the user paid that Perpline returns
# code = referral code shown on the page (None = applied through the link only)
VENUES = [
    dict(slug="btcc",     name="BTCC",     maker=0.025, taker=0.045, rebate=50, code="DDHOR6",
         ref="https://partner.btcc.com/kr/c/DDHOR6",
         note="Running since 2011, one of the longest-operating crypto exchanges.",
         about="BTCC has been operating since 2011, which makes it one of the oldest names in crypto trading. Its standard futures taker fee of 0.045% is the lowest on our list."),
    dict(slug="okx",      name="OKX",      maker=0.02, taker=0.05, rebate=30, code="96335797",
         ref="https://www.okx.com/join/96335797",
         note="Lv.1 rate. Deep BTC liquidity and a full options venue.",
         about="OKX is one of the largest derivatives venues by volume, with perpetuals, dated futures and options in one account. The rate shown is its Lv.1 (entry) fee tier."),
    dict(slug="gate",     name="Gate",     maker=0.02, taker=0.05, rebate=40, code=None,
         ref="https://www.gate.com/share/vfffufhw",
         note="VIP0 rate. One of the widest altcoin futures lists.",
         about="Gate has operated since 2013 and lists one of the widest ranges of altcoin perpetuals. The rate shown is its VIP0 (entry) tier for USDT-margined perpetuals."),
    dict(slug="bingx",    name="BingX",    maker=0.02, taker=0.05, rebate=35, code="8PFSGN",
         ref="https://bingx.com/invite/8PFSGN/",
         note="Copy trading built in alongside standard perps.",
         about="BingX combines standard USDT-margined perpetuals with built-in copy trading, so you can follow other traders' positions from the same account."),
    dict(slug="orangex",  name="OrangeX",  maker=0.02, taker=0.05, rebate=40, code="4htatgs2",
         ref="https://www.orangex.com/register?i=4htatgs2",
         note="Standard 0.02% / 0.05% perpetual rate.",
         about="OrangeX charges the common 0.02% maker / 0.05% taker rate on perpetuals. With our rebate, the taker fee you actually pay drops below most of the market."),
    dict(slug="bitget",   name="Bitget",   maker=0.02, taker=0.06, rebate=30, code=None,
         ref="https://partner.bitget.com/bg/PJHUWG",
         note="Fee depends on account level; BGB holders get discounts.",
         about="Bitget is known for copy trading and a large futures market. Fees fall with account level, and holding its BGB token unlocks further discounts."),
    dict(slug="bitunix",  name="Bitunix",  maker=0.02, taker=0.06, rebate=45, code="Lbya",
         ref="https://www.bitunix.com/register?vipCode=Lbya",
         note="Standard 0.02% / 0.06% perpetual rate.",
         about="Bitunix charges 0.02% maker and 0.06% taker on perpetuals. A 45% rebate brings the taker fee you actually pay to 0.033%, cheaper than every listed headline rate."),
    dict(slug="blofin",   name="BloFin",   maker=0.02, taker=0.06, rebate=45, code="9mqzvd",
         ref="https://blofin.com/register?breferral_code=9mqzvd",
         note="Standard 0.02% / 0.06% perpetual rate.",
         about="BloFin charges 0.02% maker and 0.06% taker on perpetuals. With a 45% rebate, your effective taker fee falls to 0.033%."),
    dict(slug="deepcoin", name="Deepcoin", maker=0.04, taker=0.06, rebate=45, code=None,
         ref="https://s.deepcoin.com/jdhaafj",
         note="Higher maker fee than most; better suited to market orders.",
         about="Deepcoin's maker fee of 0.04% is higher than most venues here, so it suits traders who mainly use market orders. A 45% rebate cuts the taker fee you pay to 0.033%."),
    dict(slug="biconomy", name="Biconomy", maker=None, taker=None, rebate=50, code="W999H2024",
         ref="https://www.biconomy.com/sign-up?r_user_id=W999H2024",
         note="Lists crypto, gold and stock perpetuals.",
         about="Biconomy lists perpetuals on crypto as well as gold and US stock tickers. We could not verify its current published futures fee, so check the fee page after you sign up."),
    dict(slug="crypfine", name="Crypfine", maker=None, taker=None, rebate=50, code="NDVTRSK",
         ref="https://www.crypfine.com/auth/NDVTRSK",
         note="Check the fee schedule on the site.",
         about="Crypfine is the newest venue on our list. We could not verify its current published futures fee, so check the fee schedule on the site before trading."),
]
DEX = []  # same shape; add perp DEX venues here

# Each exchange page gets its own "edition" tone and layout variant
TONES = [
    ("Bleu Klein", "#1F2FA0", "#8C97FF"),
    ("Bordeaux",   "#6B1D2E", "#E08A9B"),
    ("Vert anglais","#1E4A38", "#7FC7A6"),
    ("Noir",       "#111111", "#EDEAE4"),
    ("Ocre",       "#7A5418", "#E2B66A"),
    ("Ardoise",    "#2F3D4C", "#9DB2C8"),
]

# ============ helpers ============
def esc(s): return html.escape(str(s), quote=True)
def pct(v): return "—" if v is None else (f"{v:.3f}".rstrip("0").rstrip(".") + "%")
def net(v, r): return None if v is None else round(v * (1 - r / 100), 4)
LOGO_DIR = OUT / "assets" / "logos"
# official exchange logos (CoinGecko exchange images). A file in assets/logos/<slug>.svg|png|webp overrides these.
LOGOS = {
    "btcc": "https://coin-images.coingecko.com/markets/images/12/large/BTCC-LogoOnly_200x200.png?1722494798",
    "okx": "https://coin-images.coingecko.com/markets/images/96/large/WeChat_Image_20220117220452.png?1706864283",
    "gate": "https://coin-images.coingecko.com/markets/images/60/large/Frame_1.png?1747795534",
    "bingx": "https://coin-images.coingecko.com/markets/images/812/large/YtFwQwJr_400x400.jpg?1706864837",
    "orangex": "https://coin-images.coingecko.com/markets/images/1272/large/Subtract.png?1706865272",
    "bitget": "https://coin-images.coingecko.com/markets/images/540/large/2023-07-25_21.47.43.jpg?1706864507",
    "bitunix": "https://coin-images.coingecko.com/markets/images/1185/large/APP_icon_1024.png?1706865197",
    "blofin": "https://coin-images.coingecko.com/markets/images/1645/large/blofin_logo.jpeg?1718852326",
    "deepcoin": "https://coin-images.coingecko.com/markets/images/1005/large/deepcoin.jpeg?1706864992",
    "biconomy": "https://coin-images.coingecko.com/markets/images/633/large/logo_B._200x200.png?1723787144"
}
def logo(v, prefix, cls):
    src = None
    for ext in ("svg", "png", "webp"):
        if (LOGO_DIR / f"{v['slug']}.{ext}").exists():
            src = f"{prefix}assets/logos/{v['slug']}.{ext}"; break
    src = src or LOGOS.get(v["slug"])
    if not src: return ""
    return f'<span class="{cls}"><img src="{esc(src)}" alt="{esc(v["name"])} logo" loading="{'lazy' if cls=='vlogo' else 'eager'}" referrerpolicy="no-referrer"></span>'

def link(v, src):
    if CONFIG["track_base"]:
        return f'{CONFIG["track_base"].rstrip("/")}/go/{v["slug"]}?src={src}'
    return v["ref"]
TG_DM = f'https://t.me/{CONFIG["telegram_dm"]}'
TG_GROUP = CONFIG["telegram_group_url"]

def ranked(lst):
    known = sorted([v for v in lst if v["taker"] is not None], key=lambda v: (v["taker"], v["maker"]))
    return known + [v for v in lst if v["taker"] is None]

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Jost:wght@300;400;500;600&display=swap">'

CSS = r"""
/* Layout: a maison advertising page. Centered spaced wordmark, Didone display set very large, airy columns, hairline rules, one tone color per page. */
:root{
  --paper:#FFFFFF; --ink:#111111; --muted:#6E6A65; --hair:#E5E2DD; --wash:#F5F4F1;
  --tone:#1F2FA0; --tone-ink:#FFFFFF; --up:#1E6B47; --down:#9B2335;
  --display:"DM Serif Display","Didot","Bodoni 72",Georgia,serif;
  --sans:"Jost","Futura","Century Gothic",system-ui,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0D0D0E; --ink:#F1EEE8; --muted:#9A958E; --hair:#2A2A2C; --wash:#161617;
  --tone:var(--tone-d,#8C97FF); --tone-ink:#0D0D0E; --up:#6CC79C; --down:#E58A99; color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#0D0D0E; --ink:#F1EEE8; --muted:#9A958E; --hair:#2A2A2C; --wash:#161617;
  --tone:var(--tone-d,#8C97FF); --tone-ink:#0D0D0E; --up:#6CC79C; --down:#E58A99; color-scheme:dark}
*{box-sizing:border-box}
[hidden]{display:none!important}
img{max-width:100%}
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.6;font-weight:400;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
a{color:inherit}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible{outline:1px solid var(--ink);outline-offset:3px}
p{margin:0}
h1,h2,h3{margin:0;font-family:var(--display);font-weight:400;text-wrap:balance;line-height:1.02;letter-spacing:-.01em}
h1{font-size:clamp(44px,8.2vw,112px)}
h2{font-size:clamp(34px,5vw,64px)}
h3{font-size:24px}
em{font-style:italic}
.label{font-family:var(--sans);font-size:11.5px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.num{font-variant-numeric:tabular-nums lining-nums}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.fine{font-size:13px;color:var(--muted);line-height:1.6}
.rule{height:1px;background:var(--hair);border:0;margin:0}

/* header */
header.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--paper);border-bottom:1px solid var(--hair)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:21;background:var(--paper)}
.top .wrap{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;padding-block:18px}
.wordmark{font-family:var(--sans);font-weight:500;font-size:15px;letter-spacing:.42em;text-transform:uppercase;text-decoration:none;padding-left:.42em;white-space:nowrap}
.top nav{display:flex;gap:26px}
.top nav a,.top .right a{font-size:12px;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;color:var(--muted)}
.top nav a:hover,.top .right a:hover{color:var(--ink)}
.top .right{display:flex;justify-content:flex-end;gap:18px;align-items:center}
.btc{font-size:12px;letter-spacing:.12em;color:var(--muted);white-space:nowrap}
.btc b{color:var(--ink);font-weight:500}
.langsw{font-size:11.5px!important;letter-spacing:.14em!important;color:var(--ink)!important;border:1px solid var(--ink);padding:5px 10px;text-transform:none!important}
.menu-btn{display:none;font:inherit;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;padding:9px 12px;border:1px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer}
.menu-panel{border-top:1px solid var(--hair);background:var(--paper)}
.top .menu-panel .wrap{display:flex;flex-direction:column;align-items:stretch;padding-block:8px 20px}
.menu-panel a{font-family:var(--display);font-size:28px;line-height:1.2;padding-block:12px;border-bottom:1px solid var(--hair);text-decoration:none}
.menu-panel a:last-child{border-bottom:0}
@media (max-width:820px){.menu-btn{display:inline-block}.top .right{gap:12px}.btc{font-size:11px;letter-spacing:.06em}}
@media (max-width:820px){.top nav{display:none}.top .wrap{grid-template-columns:auto 1fr}.wordmark{justify-self:start;padding-left:0}.top .right a.hide-sm{display:none}}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font-family:var(--sans);font-size:12.5px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;padding:15px 26px;text-decoration:none;border:1px solid var(--ink);background:var(--ink);color:var(--paper);cursor:pointer;white-space:nowrap;transition:background .2s,color .2s}
.btn:hover{background:transparent;color:var(--ink)}
.btn.line{background:transparent;color:var(--ink)}
.btn.line:hover{background:var(--ink);color:var(--paper)}
.btn.tone{background:var(--tone);border-color:var(--tone);color:var(--tone-ink)}
.btn.tone:hover{background:transparent;color:var(--tone)}
.btn.sm{padding:11px 18px;font-size:11.5px}
.textlink{font-size:12px;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:2px}
@media (prefers-reduced-motion:reduce){.btn{transition:none}}

/* hero */
.hero{padding-block:clamp(56px,9vw,120px) clamp(40px,6vw,80px);display:flex;flex-direction:column;gap:28px}
.hero.center{align-items:center;text-align:center}
.hero h1 em{color:var(--tone)}
.lede{font-size:clamp(17px,1.6vw,20px);font-weight:300;max-width:46ch;color:var(--ink)}
.hero.center .lede{margin-inline:auto}
.cta{display:flex;gap:14px;flex-wrap:wrap}
.hero.center .cta{justify-content:center}
.figures{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);margin-top:12px}
.figures div{padding:22px 8px;display:flex;flex-direction:column;gap:6px;align-items:center;text-align:center}
.figures div + div{border-left:1px solid var(--hair)}
.figures b{font-family:var(--display);font-weight:400;font-size:clamp(30px,4vw,46px);line-height:1}
@media (max-width:560px){.figures b{font-size:26px}.figures .label{font-size:10px;letter-spacing:.14em}}

/* sections */
section.chapter{padding-block:clamp(64px,9vw,120px);border-top:1px solid var(--hair)}
.chap-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px 56px;align-items:end;margin-bottom:48px}
.chap-head p{color:var(--muted);font-weight:300;max-width:52ch}
@media (max-width:820px){.chap-head{grid-template-columns:1fr}}
.chap-head .label{display:block;margin-bottom:16px}

/* tabs */
.tabs{display:flex;gap:36px;margin-bottom:28px;border-bottom:1px solid var(--hair)}
.tab{font:inherit;font-size:12.5px;letter-spacing:.22em;text-transform:uppercase;padding:0 0 14px;border:0;border-bottom:1px solid transparent;margin-bottom:-1px;background:none;color:var(--muted);cursor:pointer}
.tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--ink)}
.tab .c{font-family:var(--display);font-style:italic;letter-spacing:0;text-transform:none;font-size:15px;margin-left:6px}
.tab-desc{font-weight:300;color:var(--muted);margin-bottom:22px;max-width:70ch}

/* venue list */
.vlist{list-style:none;margin:0;padding:0;border-top:1px solid var(--ink)}
.vrow{display:grid;grid-template-columns:56px minmax(0,1.5fr) 80px 80px 96px 110px auto;gap:18px;align-items:center;padding-block:24px;border-bottom:1px solid var(--hair)}
.vhead{padding-block:0 12px;border-bottom:0}
.vhead span{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
.vno{font-family:var(--display);font-style:italic;font-size:18px;color:var(--muted)}
.vname{display:flex;flex-direction:column;gap:4px;min-width:0}
.vname a.nm{font-family:var(--display);font-size:clamp(26px,2.6vw,34px);line-height:1.05;text-decoration:none;display:inline-flex;align-items:center;gap:14px}
.vlogo{flex:none;width:40px;height:40px;background:#FFFFFF;border:1px solid var(--hair);border-radius:50%;overflow:hidden;display:block}
.vlogo img{width:100%;height:100%;object-fit:cover;display:block}
.xlogo{display:block;width:88px;height:88px;background:#FFFFFF;border-radius:50%;margin-top:22px;overflow:hidden;box-shadow:0 0 0 1px var(--hair)}
.xhero.v1 .xlogo{margin-inline:auto}
.xlogo img{width:100%;height:100%;object-fit:cover;display:block}
.vname a.nm:hover{color:var(--tone)}
.vname .vnote{font-size:13.5px;color:var(--muted);font-weight:300}
.vfee{font-size:15px}
.vfee.na{color:var(--muted);font-size:13px}
.vreb{font-family:var(--display);font-size:30px;line-height:1;color:var(--tone)}
.vreb small{font-family:var(--sans);font-size:10px;letter-spacing:.18em;text-transform:uppercase;display:block;color:var(--muted);margin-top:6px}
.vnet{font-size:15px;font-weight:500}
.k{display:none}
.lowest{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--tone);margin-top:2px}
@media (max-width:900px){
  .vhead{display:none}
  .vrow{grid-template-columns:52px 1fr auto;grid-template-areas:"n m r" "n f f" "n g g" "n b b";gap:10px 14px;padding-block:22px}
  .vno{grid-area:n;align-self:start;padding-top:8px;font-size:15px}
  .vname{grid-area:m}
  .vreb{grid-area:r;text-align:right}
  .vfees{grid-area:f;display:flex;gap:22px;flex-wrap:wrap}
  .vfees.netc{grid-area:g}
  .vrow .btn{grid-area:b;justify-self:start}
  .k{display:inline;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-right:6px}
}
@media (min-width:901px){.vfees{display:contents}}
.empty{border-top:1px solid var(--ink);padding:64px 0;text-align:center;display:flex;flex-direction:column;gap:16px;align-items:center}
.empty p{color:var(--muted);max-width:50ch;font-weight:300}

/* rebate chapter */
.steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-top:1px solid var(--ink)}
.steps li{list-style:none;padding:28px 28px 32px 0;display:flex;flex-direction:column;gap:12px}
.steps li + li{padding-left:28px;border-left:1px solid var(--hair)}
.steps .n{font-family:var(--display);font-style:italic;font-size:44px;line-height:1;color:var(--tone)}
.steps p{color:var(--muted);font-weight:300}
@media (max-width:820px){.steps{grid-template-columns:1fr}.steps li + li{padding-left:0;border-left:0;border-top:1px solid var(--hair)}}
.terms{margin-top:48px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 56px}
.terms div{display:flex;justify-content:space-between;gap:16px;padding-block:14px;border-bottom:1px solid var(--hair);font-size:15px}
.terms div span:first-child{color:var(--muted)}
.terms div span:last-child{text-align:right}
@media (max-width:820px){.terms{grid-template-columns:1fr}}

/* calculator */
.calc{display:grid;grid-template-columns:340px minmax(0,1fr);gap:56px;align-items:start}
@media (max-width:860px){.calc{grid-template-columns:1fr;gap:36px}}
.controls{display:flex;flex-direction:column;gap:24px}
.field{display:flex;flex-direction:column;gap:8px}
.field input[type=number]{font-family:var(--display);font-size:30px;padding:6px 0 8px;border:0;border-bottom:1px solid var(--ink);background:transparent;color:var(--ink);width:100%;border-radius:0}
.field .hint{font-size:13px;color:var(--muted);font-weight:300}
.seg{display:flex;border:1px solid var(--ink)}
.seg button{flex:1;font:inherit;font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;padding:12px 8px;border:0;background:transparent;color:var(--ink);cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.check{display:flex;gap:10px;align-items:center;font-size:14px}
.check input{width:18px;height:18px;accent-color:var(--tone)}
.bars{display:flex;flex-direction:column}
.bar{display:grid;grid-template-columns:110px minmax(0,1fr) 110px;gap:16px;align-items:center;padding-block:11px;border-bottom:1px solid var(--hair)}
.bar .n{font-family:var(--display);font-size:20px}
.bar .track{height:2px;background:var(--hair);position:relative}
.bar .fill{position:absolute;inset:0 auto 0 0;background:var(--ink);transition:width .3s}
.bar .fill.reb{background:var(--tone)}
.bar .v{text-align:right;font-variant-numeric:tabular-nums;font-size:15px}
@media (max-width:520px){.bar{grid-template-columns:84px minmax(0,1fr) 88px;gap:10px}.bar .n{font-size:17px}}
@media (prefers-reduced-motion:reduce){.bar .fill{transition:none}}

/* market */
.market{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:56px;align-items:center;margin-bottom:72px}
@media (max-width:860px){.market{grid-template-columns:1fr;gap:32px}}
.price{font-family:var(--display);font-size:clamp(60px,9vw,128px);line-height:.9;letter-spacing:-.02em;font-variant-numeric:lining-nums tabular-nums}
.price small{font-size:.32em;color:var(--muted);vertical-align:.95em;margin-right:6px}
.stats{display:flex;flex-wrap:wrap;gap:14px 36px;margin-top:22px}
.stat{display:flex;flex-direction:column;gap:4px}
.stat b{font-weight:500;font-variant-numeric:tabular-nums}
.chg.up{color:var(--up)} .chg.down{color:var(--down)}
.ladder svg{width:100%;height:auto;display:block}
.note-grid{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:56px}
@media (max-width:860px){.note-grid{grid-template-columns:1fr}}
.prose{display:flex;flex-direction:column;gap:18px;max-width:64ch}
.prose p{font-size:18px;font-weight:300}
.prose p:first-child::first-letter{font-family:var(--display);float:left;font-size:4.2em;line-height:.82;padding:6px 10px 0 0;color:var(--tone)}
.facts{border-top:1px solid var(--ink)}
.fact{display:flex;justify-content:space-between;gap:16px;padding-block:13px;border-bottom:1px solid var(--hair);font-size:15px}
.fact span:first-child{color:var(--muted)}
.fact span:last-child{font-variant-numeric:tabular-nums;font-weight:500;text-align:right}
.neg{color:var(--down)} .pos{color:var(--up)}
.scen{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin-top:56px;border-top:1px solid var(--ink)}
.scen article{padding:26px 26px 0 0;display:flex;flex-direction:column;gap:10px}
.scen article + article{padding-left:26px;border-left:1px solid var(--hair)}
.scen p{color:var(--muted);font-weight:300;font-size:15.5px}
.scen p strong{color:var(--ink);font-weight:500}
@media (max-width:760px){.scen{grid-template-columns:1fr}.scen article + article{padding-left:0;border-left:0;border-top:1px solid var(--hair);padding-top:26px}.scen article{padding-bottom:26px}}

/* community */
.duo{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;border-top:1px solid var(--ink)}
.duo > div{padding:36px 40px 0 0;display:flex;flex-direction:column;gap:18px}
.duo > div + div{padding-left:40px;border-left:1px solid var(--hair)}
@media (max-width:820px){.duo{grid-template-columns:1fr}.duo > div + div{padding-left:0;border-left:0;border-top:1px solid var(--hair);margin-top:36px}}
.handle{font-family:var(--display);font-size:clamp(28px,3.4vw,42px);line-height:1.05}
.duo p{color:var(--muted);font-weight:300}
.row{display:flex;gap:12px;flex-wrap:wrap}
form.cs{display:flex;flex-direction:column;gap:18px}
form.cs label{display:flex;flex-direction:column;gap:8px}
form.cs input,form.cs select,form.cs textarea{font:inherit;font-size:16px;padding:10px 0;border:0;border-bottom:1px solid var(--hair);background:transparent;color:var(--ink);border-radius:0;width:100%}
form.cs select{padding-right:8px}
form.cs input:focus,form.cs textarea:focus,form.cs select:focus{border-bottom-color:var(--ink);outline:none}
form.cs textarea{min-height:110px;resize:vertical}
.ok{color:var(--up);font-size:14px} .err{color:var(--down);font-size:14px}

/* faq */
.faq{border-top:1px solid var(--ink);max-width:860px}
details{border-bottom:1px solid var(--hair);padding-block:22px}
summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:20px;font-family:var(--display);font-size:clamp(20px,2.2vw,26px);line-height:1.25}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-family:var(--sans);font-weight:300;color:var(--muted)}
details[open] summary::after{content:"–"}
details p{margin-top:12px;color:var(--muted);font-weight:300;max-width:66ch}

/* footer */
footer{border-top:1px solid var(--ink);padding-block:64px 80px}
.foot{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:40px}
@media (max-width:860px){.foot{grid-template-columns:1fr}}
.foot .wordmark{display:inline-block;margin-bottom:14px}
.foot p{font-size:13px;color:var(--muted);font-weight:300}
.foot h4{margin:0 0 10px;font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:500}
.foot .restrict h4{color:var(--down)}
.foot ul{list-style:none;margin:0;padding:0;columns:2;font-size:14px}
.foot li{padding-block:3px}
.foot li a{text-decoration:none;color:var(--muted)}
.foot li a:hover{color:var(--ink)}


/* ---- stage (hero carousel) ---- */
.stage{position:relative;overflow:hidden;border-bottom:1px solid var(--hair);touch-action:pan-y}
.stage-track{display:flex;transition:transform 1.25s cubic-bezier(.77,0,.18,1);will-change:transform}
.slide{position:relative;flex:0 0 100%;min-width:0;min-height:clamp(540px,76vh,780px);display:flex;align-items:center;overflow:hidden}
.slide .fx{position:absolute;inset:0;width:100%;height:100%;display:block}
.slide-in{position:relative;z-index:1;display:flex;flex-direction:column;align-items:flex-start;gap:22px;padding-block:72px 128px;width:100%}
.slide h1,.slide h2{font-size:clamp(46px,7.6vw,108px);line-height:.98}
.slide .lede{max-width:44ch}
.slide.on .slide-in > *{animation:slideRise 1.1s cubic-bezier(.2,.7,.1,1) both}
.slide.on .slide-in > *:nth-child(2){animation-delay:.08s}
.slide.on .slide-in > *:nth-child(3){animation-delay:.16s}
.slide.on .slide-in > *:nth-child(4){animation-delay:.24s}
@keyframes slideRise{from{transform:translateX(48px)}to{transform:none}}
.s-silk{background:var(--paper);color:var(--ink)}
.s-silk h1 em{color:var(--tone)}
.s-gold{background:#0B0B0C;color:#F1EEE8}
.s-gold .label{color:#C9A45C}
.s-gold h2 em{color:#C9A45C}
.mega{font-family:var(--display);font-size:clamp(120px,21vw,290px);line-height:.78;color:#C9A45C;margin:0}
.mega i{font-size:.45em}
.btn.inv-gold{background:#C9A45C;border-color:#C9A45C;color:#0B0B0C}
.btn.inv-gold:hover{background:transparent;color:#C9A45C}
.s-tone{background:var(--tone);color:var(--tone-ink)}
.s-tone .label,.s-tone .lede{color:var(--tone-ink);opacity:.85}
.btn.inv{background:var(--tone-ink);border-color:var(--tone-ink);color:var(--tone)}
.btn.inv:hover{background:transparent;color:var(--tone-ink)}
.s-chart{background:var(--wash);color:var(--ink)}
.s-chart h2 em{color:var(--tone)}
.stage-ui{position:absolute;left:0;right:0;bottom:28px;z-index:2;display:flex;justify-content:space-between;align-items:center;gap:16px;color:var(--ink)}
.stage[data-ui="light"] .stage-ui{color:#F1EEE8}
.stage-dots{display:flex;gap:10px}
.stage-dots button{width:56px;height:36px;background:none;border:0;padding:0;cursor:pointer;color:inherit}
.stage-dots span{display:block;height:2px;background:currentColor;opacity:.35;position:relative;overflow:hidden}
.stage-dots button[aria-selected="true"] span{opacity:1;background:transparent;box-shadow:inset 0 0 0 1px currentColor}
.stage-dots span::after{content:"";position:absolute;inset:0;background:currentColor;transform:scaleX(0);transform-origin:left}
.stage-dots button[aria-selected="true"] span::after{transform:scaleX(1)}
.stage-dots button.run span::after{animation:prog 7s linear forwards}
@keyframes prog{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.stage-arrows{display:flex;gap:6px}
.stage-arrows button{font:inherit;font-size:15px;width:44px;height:44px;border:1px solid currentColor;background:transparent;color:inherit;cursor:pointer;border-radius:50%}
.stage-arrows button:hover{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.stage[data-ui="light"] .stage-arrows button:hover{background:#F1EEE8;border-color:#F1EEE8;color:#0B0B0C}
@media (max-width:700px){.slide{min-height:560px}.slide-in{padding-block:56px 112px}.stage-dots button{width:34px}.stage-arrows button{width:38px;height:38px}}

/* ---- marquees ---- */
.mq{overflow:hidden;border-bottom:1px solid var(--hair);padding-block:22px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent);mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent)}
.mq-track{display:flex;width:max-content;animation:mq 70s linear infinite}
.mq:hover .mq-track{animation-play-state:paused}
@keyframes mq{to{transform:translateX(-50%)}}
.mq-item{display:inline-flex;align-items:center;gap:12px;padding-right:64px;text-decoration:none;white-space:nowrap}
.mq-logo{width:30px;height:30px;border-radius:50%;overflow:hidden;background:#fff;display:block;flex:none}
.mq-logo img{width:100%;height:100%;object-fit:cover;display:block}
.mq-name{font-family:var(--display);font-size:26px}
.mq-pct{font-family:var(--display);font-style:italic;font-size:22px;color:var(--tone)}
.mq-item:hover .mq-name{color:var(--tone)}
.mq-text{padding-block:26px;background:var(--ink);color:var(--paper);border-bottom:0}
.mq-text .mq-track{animation-duration:55s;animation-direction:reverse}
.mq-text span{font-family:var(--display);font-style:italic;font-size:clamp(26px,3vw,40px);padding-right:28px;white-space:nowrap}
.mq-text i{font-style:normal;opacity:.5;padding-right:28px;font-size:26px}
.xhero{position:relative;overflow:hidden}
.xhero > .fx{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none}
.xhero > .wrap{position:relative;z-index:1}
@media (prefers-reduced-motion:reduce){
  .stage-track{transition:none}.slide.on .slide-in > *{animation:none}
  .mq-track{animation:none}.mq{overflow-x:auto}
  .stage-dots button.run span::after{animation:none}
}

/* floating support */
.fab{position:fixed;right:calc(18px + env(safe-area-inset-right,0px));bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:30;display:flex;flex-direction:column;align-items:flex-end;gap:10px}
.fab-btn{font:inherit;font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;padding:14px 20px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);cursor:pointer;display:inline-flex;align-items:center;gap:10px}
.fab-btn svg{flex:none}
@media (max-width:700px){.fab-btn{padding:0;width:50px;height:50px;border-radius:50%;justify-content:center}.fab-btn .fab-t{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
.fab-panel{width:min(330px,calc(100vw - 36px));background:var(--paper);border:1px solid var(--ink);padding:22px;display:flex;flex-direction:column;gap:2px}
.fab-panel h3{font-size:24px;margin-bottom:10px}
.fab-panel .opt{font:inherit;text-align:left;display:flex;flex-direction:column;gap:2px;padding:14px 0;border:0;border-top:1px solid var(--hair);background:none;color:var(--ink);text-decoration:none;cursor:pointer}
.fab-panel .opt b{font-weight:500}
.fab-panel .opt span{font-size:13px;color:var(--muted);font-weight:300}
"""

def head(title, desc, canonical, extra_ld="", tone=None):
    tone_css = ""
    if tone:
        tone_css = f'<style>:root{{--tone:{tone[1]};--tone-d:{tone[2]}}}</style>'
    return f"""<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='32' fill='%231F2FA0'/%3E%3Ctext x='33' y='46' font-family='Georgia,serif' font-style='italic' font-size='40' text-anchor='middle' fill='%23F4F1EA'%3EP%3C/text%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{CONFIG['domain']}/assets/icon.png">
<meta property="og:image" content="{CONFIG['domain']}/assets/og.png"><meta name="twitter:image" content="{CONFIG['domain']}/assets/og.png">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{esc(canonical)}"><meta name="twitter:card" content="summary_large_image">
{FONTS}
<style>{CSS}</style>
{tone_css}
{extra_ld}"""

def header(prefix):
    return f"""<header class="top">
  <div class="wrap">
    <nav aria-label="Sections">
      <a href="{prefix}index.html#venues">Exchanges</a>
      <a href="{prefix}index.html#rebate">Rebate</a>
      <a href="{prefix}index.html#note">Market</a>
    </nav>
    <a class="wordmark" href="{prefix}index.html">{CONFIG['brand']}</a>
    <div class="right">
      <a class="hide-sm" href="{TG_GROUP}" target="_blank" rel="noopener">Community</a>
      <a class="langsw" id="langSw" href="#" hidden>한국어</a>
      <span class="btc">BTC <b id="pillPrice" class="num">$80,300</b></span>
      <button type="button" class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="menuPanel">Menu</button>
    </div>
  </div>
  <div class="menu-panel" id="menuPanel" role="navigation" aria-label="Menu" hidden>
    <div class="wrap">
      <a href="{prefix}index.html#venues">Exchanges</a>
      <a href="{prefix}index.html#rebate">Rebate</a>
      <a href="{prefix}index.html#fees">Fee calculator</a>
      <a href="{prefix}index.html#note">Market</a>
      <a href="{prefix}index.html#faq">Questions</a>
      <a href="{TG_GROUP}" target="_blank" rel="noopener">Community</a>
      <a href="{TG_DM}" target="_blank" rel="noopener">Support on Telegram</a>
    </div>
  </div>
</header>"""

def footer(prefix):
    items = "".join(f'<li><a href="{prefix}exchanges/{v["slug"]}.html">{esc(v["name"])} referral code</a></li>' for v in ranked(VENUES))
    return f"""<footer>
  <div class="wrap foot">
    <div>
      <a class="wordmark" href="{prefix}index.html">{CONFIG['brand']}</a>
      <p>Fee-first guides to crypto perpetual futures venues, with up to 50% of your trading fees returned.</p>
      <p style="margin-top:14px">Support: <a href="{TG_DM}" target="_blank" rel="noopener">@{CONFIG['telegram_dm']}</a> on Telegram · Community: <a href="{TG_GROUP}" target="_blank" rel="noopener">{CONFIG['telegram_group_name']}</a> on Telegram</p>
    </div>
    <div>
      <h4>Exchange guides</h4>
      <ul>{items}</ul>
    </div>
    <div>
      <div class="restrict"><h4>Restricted jurisdictions</h4>
      <p>Not directed at residents of the Republic of Korea, the United States, or any jurisdiction where the listed exchanges are not licensed or registered to serve local users. If you live in one of these places, do not use the links on this site.</p></div>
      <h4 style="margin-top:22px">Risk &amp; disclosure</h4>
      <p>Leveraged derivatives carry a high risk of losing all of your margin. Nothing here is financial advice. Links are referral links; we earn a commission and share part of it with you as a fee rebate. Rebates are paid by {CONFIG['brand']}, not by the exchanges. © 2026 {CONFIG['brand']}.</p>
    </div>
  </div>
</footer>"""

FAB = f"""<div class="fab">
  <div class="fab-panel" id="fabPanel" hidden role="dialog" aria-labelledby="fabH">
    <h3 id="fabH">How can we help?</h3>
    <a class="opt" href="{TG_DM}" target="_blank" rel="noopener"><b>Chat on Telegram</b><span>Claim a rebate or ask about sign-up</span></a>
    <a class="opt" href="{TG_GROUP}" target="_blank" rel="noopener"><b>Join the community</b><span>Market notes and new listings</span></a>
    <button type="button" class="opt" id="fabForm"><b>Send a support request</b><span>We reply on Telegram</span></button>
  </div>
  <button type="button" class="fab-btn" id="fabBtn" aria-expanded="false" aria-controls="fabPanel"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg><span class="fab-t">Support</span></button>
</div>"""

FX_JS = r"""
/* ---- motion scenes (canvas) ---- */
const FX=(function(){
  const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
  const items=[]; let cols={}, frame=0;
  function rgb(c){ c=(c||"#000").trim(); if(c.startsWith("#")){ if(c.length===4) c="#"+[...c.slice(1)].map(x=>x+x).join(""); return [1,3,5].map(i=>parseInt(c.slice(i,i+2),16)); } const m=c.match(/\d+(\.\d+)?/g); return m?m.slice(0,3).map(Number):[0,0,0]; }
  function readCols(){ const cs=getComputedStyle(document.documentElement); ["--tone","--tone-ink","--ink","--paper","--muted","--hair"].forEach(k=>cols[k]=rgb(cs.getPropertyValue(k))); }
  const A=(k,a)=>{ const c=cols[k]||k; return `rgba(${c[0]},${c[1]},${c[2]},${a})`; };
  function rnd(seed){ return ()=>{ seed=(seed*16807)%2147483647; return (seed-1)/2147483646; }; }
  const SCENES={
    silk(s,t){ const {ctx,w,h}=s, col=s.col||"--tone"; ctx.clearRect(0,0,w,h); const N=28; ctx.lineWidth=1;
      for(let i=0;i<N;i++){ const k=i/(N-1); ctx.strokeStyle=A(col,0.05+0.30*Math.sin(Math.PI*k)); ctx.beginPath();
        for(let x=-20;x<=w+20;x+=10){ const y=h*0.58+Math.sin(x*0.0030+t*0.22+k*2.4)*h*0.15+Math.sin(x*0.0012-t*0.15+k*5.1)*h*0.11+(k-0.5)*h*0.42*Math.cos(t*0.05+x*0.0007);
          x===-20?ctx.moveTo(x,y):ctx.lineTo(x,y); } ctx.stroke(); } },
    orbit(s,t){ const {ctx,w,h}=s; ctx.clearRect(0,0,w,h); const cx=w>760?w*0.74:w*0.62, cy=h*0.48, R=Math.min(w,h)*0.46;
      for(let r=0;r<9;r++){ const rad=R*(0.25+r*0.095); ctx.strokeStyle=`rgba(201,164,92,${0.06+r*0.012})`; ctx.lineWidth=1; ctx.beginPath(); ctx.ellipse(cx,cy,rad,rad*0.92,0,0,Math.PI*2); ctx.stroke();
        const n=6+r*3, dir=r%2?1:-1; for(let j=0;j<n;j++){ const a=j/n*Math.PI*2+t*0.09*dir*(1+r*0.08); const px=cx+Math.cos(a)*rad, py=cy+Math.sin(a)*rad*0.92;
          ctx.fillStyle=`rgba(201,164,92,${0.25+0.55*((Math.sin(a*3+t)+1)/2)})`; ctx.beginPath(); ctx.arc(px,py,1.2+((j+r)%3)*0.7,0,Math.PI*2); ctx.fill(); } } },
    drift(s,t){ const {ctx,w,h}=s; ctx.clearRect(0,0,w,h); const imgs=s.imgs||[]; ctx.strokeStyle=A("--tone-ink",0.10); ctx.lineWidth=1;
      for(let x=(t*14)%120-120;x<w;x+=120){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
      if(!imgs.length) return; const rows=3;
      for(let r=0;r<rows;r++){ const size=[64,84,56][r], gap=size*2.6, speed=[18,11,26][r], y=h*(0.24+r*0.26), off=(t*speed+r*90)%(gap*imgs.length);
        for(let k=0;k<imgs.length+3;k++){ const im=imgs[(k+r*3)%imgs.length]; let x=w-((k*gap+off)%(gap*(imgs.length+1)))+gap; if(x<-size||x>w+size) continue; if(!im.complete||!im.naturalWidth) continue;
          ctx.save(); ctx.globalAlpha=0.55; ctx.beginPath(); ctx.arc(x,y,size/2,0,Math.PI*2); ctx.clip(); ctx.fillStyle="#fff"; ctx.fillRect(x-size/2,y-size/2,size,size); ctx.drawImage(im,x-size/2,y-size/2,size,size); ctx.restore(); } } },
    chart(s,t){ const {ctx,w,h}=s; ctx.clearRect(0,0,w,h); if(!s.pts){ const r=rnd(7); let v=0.5; s.pts=[]; for(let i=0;i<220;i++){ v+= (r()-0.48)*0.045; v=Math.max(0.12,Math.min(0.88,v)); s.pts.push(v);} }
      ctx.strokeStyle=A("--hair",1); ctx.lineWidth=1; for(let g=1;g<6;g++){ const y=h*g/6; ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
      const cyc=14, p=Math.min(1,((t%cyc)/cyc)*1.25), n=Math.max(2,Math.floor(s.pts.length*p)); const narrow=w<760, X=i=>w*(narrow?0.02:0.46)+(w*(narrow?0.96:0.52))*i/(s.pts.length-1), Y=v=>h*(0.52+0.36*(1-v)); if(narrow) ctx.globalAlpha=0.4;
      const grad=ctx.createLinearGradient(0,h*0.5,0,h); grad.addColorStop(0,A("--tone",0.22)); grad.addColorStop(1,A("--tone",0));
      ctx.beginPath(); ctx.moveTo(X(0),Y(s.pts[0])); for(let i=1;i<n;i++) ctx.lineTo(X(i),Y(s.pts[i])); ctx.lineTo(X(n-1),h); ctx.lineTo(X(0),h); ctx.closePath(); ctx.fillStyle=grad; ctx.fill();
      ctx.beginPath(); ctx.moveTo(X(0),Y(s.pts[0])); for(let i=1;i<n;i++) ctx.lineTo(X(i),Y(s.pts[i])); ctx.strokeStyle=A("--tone",0.9); ctx.lineWidth=1.6; ctx.stroke();
      const hx=X(n-1), hy=Y(s.pts[n-1]); ctx.fillStyle=A("--tone",1); ctx.beginPath(); ctx.arc(hx,hy,4,0,Math.PI*2); ctx.fill(); ctx.strokeStyle=A("--tone",0.25); ctx.beginPath(); ctx.arc(hx,hy,10+4*Math.sin(t*3),0,Math.PI*2); ctx.stroke(); ctx.globalAlpha=1; }
  };
  function add(cv){
    const fx=cv.dataset.fx; if(!SCENES[fx]) return; const ctx=cv.getContext("2d"); if(!ctx) return;
    const s={cv,ctx,fx,w:1,h:1,vis:true,col:cv.dataset.col?("--"+cv.dataset.col):null};
    if(cv.dataset.logos){ try{ s.imgs=JSON.parse(cv.dataset.logos).map(u=>{ const im=new Image(); im.referrerPolicy="no-referrer"; im.src=u; return im; }); }catch(e){ s.imgs=[]; } }
    const size=()=>{ const r=cv.getBoundingClientRect(), d=Math.min(2,window.devicePixelRatio||1); s.w=r.width||cv.parentNode.clientWidth; s.h=r.height||cv.parentNode.clientHeight; cv.width=Math.max(1,s.w*d); cv.height=Math.max(1,s.h*d); ctx.setTransform(d,0,0,d,0,0); };
    size(); addEventListener("resize",size);
    if("IntersectionObserver" in window){ new IntersectionObserver(es=>es.forEach(e=>s.vis=e.isIntersecting),{threshold:0}).observe(cv); }
    items.push(s);
  }
  function loop(ts){ const t=ts/1000; if(frame++%90===0) readCols(); items.forEach(s=>{ if(s.vis) SCENES[s.fx](s,t); }); requestAnimationFrame(loop); }
  function init(){ readCols(); document.querySelectorAll("canvas.fx").forEach(add);
    if(reduce){ items.forEach(s=>SCENES[s.fx](s,9)); setTimeout(()=>{ readCols(); items.forEach(s=>SCENES[s.fx](s,9)); },1200); } else requestAnimationFrame(loop);
    try{ matchMedia("(prefers-color-scheme: dark)").addEventListener("change",readCols); new MutationObserver(readCols).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]}); }catch(e){} }
  return {init,reduce};
})();
FX.init();
"""

COMMON_JS = r"""
const $ = id => document.getElementById(id);
(function(){ try{ const sw=$("langSw"); if(!sw||!window.LANG_ALT) return;
  if(window.LANG==="ko") localStorage.setItem("perpline_owner","1");
  if(window.LANG==="ko"||localStorage.getItem("perpline_owner")==="1"){ sw.href=window.LANG_ALT; sw.textContent=window.LANG==="ko"?"EN":"한국어"; sw.hidden=false; }
}catch(e){} })();
const fmt = n => n.toLocaleString("en-US",{maximumFractionDigits:0});
(function(){ const b=$("menuBtn"), p=$("menuPanel"); if(!b||!p) return;
  const set=o=>{ p.hidden=!o; b.setAttribute("aria-expanded",String(o)); b.textContent=o?(window.LANG==="ko"?"닫기":"Close"):(window.LANG==="ko"?"메뉴":"Menu"); };
  b.addEventListener("click",()=>set(p.hidden)); p.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>set(false)));
  addEventListener("resize",()=>{ if(innerWidth>820) set(false); }); if(window.LANG==="ko") b.textContent="메뉴";
})();
function fab(open){ $("fabPanel").hidden=!open; $("fabBtn").setAttribute("aria-expanded",open); }
$("fabBtn").addEventListener("click",()=>fab($("fabPanel").hidden));
document.addEventListener("keydown",e=>{ if(e.key==="Escape") fab(false); });
const fabForm=$("fabForm");
if(fabForm) fabForm.addEventListener("click",()=>{ fab(false); const f=$("community"); if(f){ f.scrollIntoView({behavior:"smooth"}); setTimeout(()=>$("csTg")&&$("csTg").focus(),400);} else { location.href=(window.HOME||"index.html")+"#community"; } });
async function btcPill(){
  try{
    const r = await fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",{cache:"no-store"});
    if(!r.ok) throw 0; const j = await r.json();
    $("pillPrice").textContent = "$"+fmt(j.bitcoin.usd);
  }catch(e){}
}
"""

# ============ INDEX ============
MQ_WORDS = ["Paid every Monday", "In USDT", "No password", "No API keys", "Up to 50% back", "Eleven exchanges", "Ranked by fee"]

def marquee(rows, prefix):
    items = "".join(
        f'<a class="mq-item" href="{prefix}exchanges/{v["slug"]}.html">{logo(v, prefix, "mq-logo")}<span class="mq-name">{esc(v["name"])}</span><span class="mq-pct">{v["rebate"]}%</span></a>'
        for v in rows)
    dup = items.replace('<a ', '<a tabindex="-1" aria-hidden="true" ')
    return f'<div class="mq mq-logos" aria-label="Exchanges and rebates"><div class="mq-track">{items}{dup}</div></div>'

def venue_rows(lst, ol_id, src='home'):
    rows = ranked(lst)
    min_t = min([v["taker"] for v in rows if v["taker"] is not None], default=None)
    out = []
    for i, v in enumerate(rows):
        n_t = net(v["taker"], v["rebate"])
        fee_m = f'<span class="vfee num"><span class="k">Maker</span>{pct(v["maker"])}</span>' if v["maker"] is not None else '<span class="vfee na"><span class="k">Maker</span>Check site</span>'
        fee_t = f'<span class="vfee num"><span class="k">Taker</span>{pct(v["taker"])}</span>' if v["taker"] is not None else '<span class="vfee na"><span class="k">Taker</span>Check site</span>'
        net_s = f'<span class="vnet num"><span class="k">You pay</span>{pct(n_t)}</span>' if n_t is not None else '<span class="vfee na"><span class="k">You pay</span>—</span>'
        low = '<span class="lowest">Lowest headline taker</span>' if v["taker"] is not None and v["taker"] == min_t else ""
        out.append(f"""<li class="vrow">
  <span class="vno">No.&nbsp;{i+1:02d}</span>
  <span class="vname"><a class="nm" href="exchanges/{v['slug']}.html">{logo(v,'','vlogo')}{esc(v['name'])}</a><span class="vnote">{esc(v['note'])}</span>{low}</span>
  <span class="vfees">{fee_m}{fee_t}</span>
  <span class="vreb">{v['rebate']}%<small>Rebate</small></span>
  <span class="vfees netc">{net_s}</span>
  <a class="btn sm" href="{esc(link(v,src))}" target="_blank" rel="sponsored nofollow noopener" aria-label="Sign up for {esc(v['name'])}">Sign up</a>
</li>""")
    return "\n".join(out)


def build_landing():
    rk = ranked(VENUES)
    lo, hi = min(v["rebate"] for v in VENUES), max(v["rebate"] for v in VENUES)
    nets = [net(v["taker"], v["rebate"]) for v in VENUES if v["taker"] is not None]
    lpcss = """
.notice{background:var(--ink);color:var(--paper);font-size:12.5px;letter-spacing:.06em;text-align:center;padding-block:10px}
.notice b{font-weight:500}
.lp-hero{position:relative;overflow:hidden;border-bottom:1px solid var(--hair)}
.lp-hero > .fx{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none}
.lp-hero .wrap{position:relative;z-index:1;padding-block:clamp(56px,9vw,112px) clamp(48px,7vw,88px);display:flex;flex-direction:column;gap:24px;align-items:flex-start}
.lp-hero h1{font-size:clamp(46px,7.4vw,104px)}
.lp-hero h1 em{color:var(--tone)}
.lp-points{display:flex;flex-wrap:wrap;gap:10px 28px;font-size:14px;color:var(--muted)}
.lp-points span::before{content:"— ";color:var(--tone)}
"""
    faqs = [
        ("How much do I get back?", f"Between {lo}% and {hi}% of the futures trading fees you pay, depending on the exchange. Each rate is shown in the list above."),
        ("When and how am I paid?", "Every Monday (UTC), in USDT, to your exchange UID or wallet. Minimum payout is 10 USDT; smaller amounts roll over."),
        ("Do you need my password or API key?", "No. Only the exchange name and your account UID. Never share your password, 2FA codes or API keys with anyone."),
        ("I already have an account. Does it count?", "Usually not. Exchanges attach a referral only when the account is created, so the rebate needs a new account opened through our link."),
    ]
    page = f"""{head(f"Up to {hi}% Back on Crypto Futures Fees | {CONFIG['brand']}",
        f"Sign up to one of {len(VENUES)} futures exchanges through Perpline and get {lo}–{hi}% of your trading fees back in USDT every Monday.",
        CONFIG['domain'] + "/start.html")}
<style>{lpcss}</style>
<!--BODY-->
<div class="notice" role="note"><div class="wrap"><b>Not available to residents of the United States or South Korea.</b> 18+ · Leveraged trading can lose you all of your margin.</div></div>
{header('')}
<main id="top">
  <section class="lp-hero" aria-labelledby="h1">
    <canvas class="fx" data-fx="silk" aria-hidden="true"></canvas>
    <div class="wrap">
      <span class="label">La remise · {CONFIG['brand']}</span>
      <h1 id="h1">Get up to {hi}% of your<br>futures fees <em>back.</em></h1>
      <p class="lede">Open a futures account through {CONFIG['brand']}, trade as usual, and we send part of every fee you pay back to you in USDT, every Monday.</p>
      <div class="cta"><a class="btn" href="#venues">Choose an exchange</a><a class="btn line" href="#how">How it works</a></div>
      <div class="lp-points"><span>{len(VENUES)} exchanges</span><span>{lo}–{hi}% back</span><span>Paid weekly in USDT</span><span>No password, no API keys</span></div>
    </div>
  </section>
  {marquee(rk, "")}
  <section class="chapter" id="venues" aria-labelledby="venH" style="border-top:0">
    <div class="wrap">
      <div class="chap-head">
        <div><span class="label">I · La sélection</span><h2 id="venH">Pick your exchange</h2></div>
        <p>Ranked by taker fee, the rate most market orders pay. "You pay" is the taker fee after your rebate. Lowest after rebate: {pct(min(nets))}.</p>
      </div>
      <div class="vrow vhead" aria-hidden="true"><span>No.</span><span>Exchange</span><span>Maker</span><span>Taker</span><span>Rebate</span><span>You pay</span><span></span></div>
      <ol class="vlist">{venue_rows(VENUES, 'cex', 'lp')}</ol>
      <p class="fine" style="margin-top:20px">Standard (non-VIP) USDT-margined perpetual fees, checked {CONFIG['fees_checked']}. Your live account rate applies.</p>
    </div>
  </section>
  <section class="chapter" id="how" aria-labelledby="howH">
    <div class="wrap">
      <div class="chap-head"><div><span class="label">II · La remise</span><h2 id="howH">Three steps to your rebate</h2></div>
      <p>Exchanges pay us a commission on referred traders' fees. We pass {lo}–{hi}% of your fees back to you.</p></div>
      <ol class="steps">
        <li><span class="n">1</span><h3>Sign up through our link</h3><p>Open a new account with the Sign up button above. The rebate only works for accounts created through our link.</p></li>
        <li><span class="n">2</span><h3>Send us your UID</h3><p>Send the exchange name and your account UID to <a href="{TG_DM}" target="_blank" rel="noopener">@{CONFIG['telegram_dm']}</a> on Telegram. We confirm within 24 hours.</p></li>
        <li><span class="n">3</span><h3>Get paid every Monday</h3><p>Trade as usual. Each Monday we send last week's rebate in USDT to your exchange UID or wallet.</p></li>
      </ol>
      <div class="cta" style="margin-top:40px"><a class="btn" href="#venues">Choose an exchange</a><a class="btn line" href="{TG_DM}" target="_blank" rel="noopener">Ask on Telegram</a></div>
    </div>
  </section>
  <section class="chapter" id="faq" aria-labelledby="faqH">
    <div class="wrap">
      <div class="chap-head"><div><span class="label">III · Questions</span><h2 id="faqH">Before you sign up</h2></div></div>
      <div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in faqs)}</div>
      <p class="fine" style="margin-top:28px"><a href="index.html">See the full site, fee calculator and market notes →</a></p>
    </div>
  </section>
</main>
{footer('')}
{FAB}
<script>
window.LANG="en"; window.LANG_ALT="";
{COMMON_JS}
{FX_JS}
btcPill();
</script>
"""
    return page

def build_index():
    rk = ranked(VENUES)
    max_reb = max(v["rebate"] for v in VENUES)
    nets = [net(v["taker"], v["rebate"]) for v in VENUES if v["taker"] is not None]
    js_venues = json.dumps([{k: v[k] for k in ("name","maker","taker","rebate")} for v in rk])
    ld = {"@context":"https://schema.org","@type":"WebSite","name":CONFIG["brand"],"url":CONFIG["domain"]}
    dex_block = (f"""<div class="vrow vhead" aria-hidden="true"><span>No.</span><span>Protocol</span><span>Maker</span><span>Taker</span><span>Rebate</span><span>You pay</span><span></span></div>
        <ol class="vlist">{venue_rows(DEX,'dex')}</ol>""" if DEX else f"""<div class="empty">
          <span class="label">Bientôt</span>
          <h3>Perp DEX listings are on the way</h3>
          <p>On-chain perpetual exchanges with the same fee-first ranking and rebate. Join the community to hear when they go live.</p>
          <a class="btn line sm" href="{TG_GROUP}" target="_blank" rel="noopener">Join the community</a>
        </div>""")
    marquee_logos = marquee(rk, "")
    logo_urls = esc(json.dumps([LOGOS[v["slug"]] for v in rk if v["slug"] in LOGOS]))
    page = f"""{head(f"{CONFIG['brand']} — Crypto Futures Referral Codes & Up to {max_reb}% Fee Rebate",
        f"Compare {len(VENUES)} crypto futures exchanges by fee, sign up with our referral links, and get {min(v['rebate'] for v in VENUES)}–{max_reb}% of your trading fees back in USDT every week.",
        CONFIG['domain'] + "/", f'<script type="application/ld+json">{json.dumps(ld)}</script>')}
<!--BODY-->
{header('')}
<main id="top">
  <section class="stage" id="stage" aria-roledescription="carousel" aria-label="Perpline highlights">
    <div class="stage-track" id="stageTrack">
      <article class="slide s-silk" aria-roledescription="slide" aria-label="1 of 4">
        <canvas class="fx" data-fx="silk" aria-hidden="true"></canvas>
        <div class="slide-in wrap">
          <span class="label">{CONFIG['edition']}</span>
          <h1 id="h1">Your trading fees,<br><em>returned.</em></h1>
          <p class="lede">Sign up to a futures exchange through {CONFIG['brand']} and we send {min(v['rebate'] for v in VENUES)}–{max_reb}% of the fees you pay back to you, in USDT, every week.</p>
          <div class="cta"><a class="btn" href="#venues">Choose an exchange</a><a class="btn line" href="#rebate">How the rebate works</a></div>
        </div>
      </article>
      <article class="slide s-gold" aria-roledescription="slide" aria-label="2 of 4">
        <canvas class="fx" data-fx="orbit" aria-hidden="true"></canvas>
        <div class="slide-in wrap">
          <span class="label">La remise</span>
          <p class="mega num">{max_reb}<i>%</i></p>
          <h2>of your futures fees,<br><em>back every Monday.</em></h2>
          <div class="cta"><a class="btn inv-gold" href="#rebate">How the rebate works</a></div>
        </div>
      </article>
      <article class="slide s-tone" aria-roledescription="slide" aria-label="3 of 4">
        <canvas class="fx" data-fx="drift" data-logos='{logo_urls}' aria-hidden="true"></canvas>
        <div class="slide-in wrap">
          <span class="label">La sélection</span>
          <h2>Eleven exchanges,<br><em>ranked by what they cost.</em></h2>
          <p class="lede">From BTCC at 0.045% to the 0.022% you pay after our rebate.</p>
          <div class="cta"><a class="btn inv" href="#venues">See the ranking</a></div>
        </div>
      </article>
      <article class="slide s-chart" aria-roledescription="slide" aria-label="4 of 4">
        <canvas class="fx" data-fx="chart" aria-hidden="true"></canvas>
        <div class="slide-in wrap">
          <span class="label">Le marché</span>
          <h2>Bitcoin, read<br><em>three times a week.</em></h2>
          <p class="lede">BTC <b class="num" id="stageBtc">$80,300</b> · desk notes every Monday, Wednesday and Friday.</p>
          <div class="cta"><a class="btn" href="#note">Read the note</a></div>
        </div>
      </article>
    </div>
    <div class="stage-ui wrap">
      <div class="stage-dots" role="tablist" aria-label="Choose slide">
        <button type="button" role="tab" aria-label="Slide 1"><span></span></button>
        <button type="button" role="tab" aria-label="Slide 2"><span></span></button>
        <button type="button" role="tab" aria-label="Slide 3"><span></span></button>
        <button type="button" role="tab" aria-label="Slide 4"><span></span></button>
      </div>
      <div class="stage-arrows">
        <button type="button" id="stagePrev" aria-label="Previous slide">←</button>
        <button type="button" id="stagePause" aria-label="Pause slideshow">❙❙</button>
        <button type="button" id="stageNext" aria-label="Next slide">→</button>
      </div>
    </div>
  </section>
  {marquee_logos}
  <div class="wrap">
    <div class="figures">
      <div><b class="num">{len(VENUES)+len(DEX)}</b><span class="label">Venues</span></div>
      <div><b class="num">{max_reb}%</b><span class="label">Top rebate</span></div>
      <div><b class="num">{pct(min(nets))}</b><span class="label">Lowest taker after rebate</span></div>
    </div>
  </div>

  <section class="chapter" id="venues" aria-labelledby="venH" style="border-top:0">
    <div class="wrap">
      <div class="chap-head">
        <div><span class="label">I · La sélection</span><h2 id="venH">The exchanges</h2></div>
        <p>Ranked by headline taker fee, the rate most market orders pay. "You pay" is the taker fee after your {CONFIG['brand']} rebate. Open a name for the full guide and referral code.</p>
      </div>
      <div class="tabs" role="tablist" aria-label="Venue type">
        <button class="tab" role="tab" id="tab-cex" aria-controls="panel-cex" aria-selected="true">Exchanges <span class="c">{len(VENUES)}</span></button>
        <button class="tab" role="tab" id="tab-dex" aria-controls="panel-dex" aria-selected="false" tabindex="-1">Perp DEX <span class="c">{len(DEX)}</span></button>
      </div>
      <div role="tabpanel" id="panel-cex" aria-labelledby="tab-cex">
        <p class="tab-desc">Centralized exchanges. You register with email, verify identity where required, and the exchange holds your funds.</p>
        <div class="vrow vhead" aria-hidden="true"><span>No.</span><span>Exchange</span><span>Maker</span><span>Taker</span><span>Rebate</span><span>You pay</span><span></span></div>
        <ol class="vlist">{venue_rows(VENUES,'cex')}</ol>
      </div>
      <div role="tabpanel" id="panel-dex" aria-labelledby="tab-dex" hidden>
        <p class="tab-desc">On-chain perpetual exchanges. You trade from your own wallet and keep custody of your funds.</p>
        {dex_block}
      </div>
      <p class="fine" style="margin-top:20px">Standard (non-VIP) USDT-margined perpetual fees as listed by each exchange or TradersUnion, checked {CONFIG['fees_checked']}. Your live account rate applies. "Check site" means we could not verify the current rate.</p>
    </div>
  </section>

  <div class="mq mq-text" aria-hidden="true"><div class="mq-track">{"".join(f'<span>{w}</span><i>·</i>' for w in MQ_WORDS*2)}</div></div>
  <section class="chapter" id="rebate" aria-labelledby="rebH" style="border-top:0">
    <div class="wrap">
      <div class="chap-head">
        <div><span class="label">II · La remise</span><h2 id="rebH">How the rebate works</h2></div>
        <p>Exchanges pay us a commission on the fees our referred traders pay. We pass {min(v['rebate'] for v in VENUES)}–{max_reb}% of your fees back to you. We never ask for your password, API keys or funds.</p>
      </div>
      <ol class="steps">
        <li><span class="n">1</span><h3>Sign up through our link</h3><p>Register a new account using the Sign up button or referral code on this site. The rebate only works for accounts created through our link.</p></li>
        <li><span class="n">2</span><h3>Send us your UID</h3><p>Send the exchange name and your account UID to <a href="{TG_DM}" target="_blank" rel="noopener">@{CONFIG['telegram_dm']}</a> on Telegram. We confirm the link within 24 hours.</p></li>
        <li><span class="n">3</span><h3>Get paid every Monday</h3><p>Trade as usual. Every Monday we send your rebate for the previous week in USDT to your exchange UID or wallet.</p></li>
      </ol>
      <div class="terms">
        <div><span>Rebate rate</span><span>{min(v['rebate'] for v in VENUES)}–{max_reb}% of trading fees, by exchange</span></div>
        <div><span>Paid in</span><span>USDT</span></div>
        <div><span>Schedule</span><span>Weekly, every Monday (UTC)</span></div>
        <div><span>Minimum payout</span><span>10 USDT; smaller amounts roll over</span></div>
        <div><span>Covers</span><span>Futures trading fees on accounts linked to us</span></div>
        <div><span>Not covered</span><span>Wash trading, self-referral, fee-free promotions</span></div>
      </div>
      <p class="fine" style="margin-top:20px">Rebates are calculated from the commission reports each exchange gives us and are paid by {CONFIG['brand']}, not by the exchange. Rates can change with 7 days' notice in our Telegram community.</p>
    </div>
  </section>

  <section class="chapter" id="fees" aria-labelledby="feeH">
    <div class="wrap">
      <div class="chap-head">
        <div><span class="label">III · Le calcul</span><h2 id="feeH">What a month of trading costs</h2></div>
        <p>Opening and closing a position each pay a fee on the full position size, leverage included. Compare venues before and after your rebate.</p>
      </div>
      <div class="calc">
        <div class="controls">
          <div class="field"><label class="label" for="notional">Position size, USDT</label><input id="notional" type="number" inputmode="decimal" min="0" step="100" value="10000"><span class="hint">Margin × leverage. 1,000 at 10× is 10,000.</span></div>
          <div class="field"><span class="label" id="otLabel">Order type</span>
            <div class="seg" role="group" aria-labelledby="otLabel"><button type="button" id="otTaker" aria-pressed="true">Market order</button><button type="button" id="otMaker" aria-pressed="false">Limit order</button></div></div>
          <div class="field"><label class="label" for="trades">Round trips per month</label><input id="trades" type="number" inputmode="numeric" min="1" step="1" value="20"></div>
          <label class="check" for="withReb"><input type="checkbox" id="withReb" checked> Include {CONFIG['brand']} rebate</label>
        </div>
        <div><div class="bars" id="bars" aria-live="polite"></div><p class="fine" id="calcNote" style="margin-top:16px"></p></div>
      </div>
    </div>
  </section>

  <section class="chapter" id="note" aria-labelledby="noteH">
    <div class="wrap">
      <div class="market">
        <div>
          <span class="label">BTC / USD · <span id="feedLabel">Snapshot · Oct 25, 2026</span></span>
          <div class="price" style="margin-top:14px"><small>$</small><span id="priceVal">80,300</span></div>
          <div class="stats">
            <div class="stat"><span class="label">24h</span><b class="chg" id="chg">—</b></div>
            <div class="stat"><span class="label">24h low</span><b id="lo">79,263</b></div>
            <div class="stat"><span class="label">24h high</span><b id="hi">81,445</b></div>
            <div class="stat"><span class="label">Updated</span><b id="upd">Oct 25, 2026</b></div>
          </div>
        </div>
        <div class="ladder" aria-label="Key price levels">
          <span class="label">Levels in play</span>
          <svg id="ladder" viewBox="0 0 420 300" role="img" aria-label="Price ladder showing support and resistance levels" style="margin-top:12px"></svg>
        </div>
      </div>
      <div class="chap-head">
        <div><span class="label">IV · Le marché · Sunday, Oct 25, 2026</span><h2 id="noteH">Longs flushed under $80K. The Fed decides the next leg.</h2></div>
      </div>
      <div class="note-grid">
        <div class="prose">
          <p>Bitcoin slipped below $80,000 late in the week and is holding around $80,300. The move was driven by forced selling, not fresh shorts: more than nine in ten BTC liquidations over the last 24 hours hit long positions. When the selling is mostly liquidations, it often runs out once over-leveraged longs are cleared.</p>
          <p>The pressure came from outside crypto. US spot Bitcoin ETFs posted their largest single-day outflow since late June on Oct 22, the same day the Nasdaq had its worst session since early June on worries about AI spending. Oil also climbed to its highest level since May, which pushes back against hopes for rate cuts.</p>
          <p>The next catalyst is the Fed. The FOMC meets Oct 27–28 with the decision on Wednesday. Until then, the $79.3K low and the $81.0–81.4K band are the lines that matter. Leverage is still the main risk in both directions, so size positions so a single wick can't liquidate you.</p>
        </div>
        <div class="facts" aria-label="Key numbers">
          <div class="fact"><span>BTC liquidations, 24h</span><span>$239.7M</span></div>
          <div class="fact"><span>Share that were longs</span><span class="neg">93.1%</span></div>
          <div class="fact"><span>All-crypto liquidations, 24h</span><span>$820.8M</span></div>
          <div class="fact"><span>Spot ETF net flow, Oct 22</span><span class="neg">−$635.5M</span></div>
          <div class="fact"><span>Spot ETF net flow, Oct 23</span><span class="neg">−$137.9M</span></div>
          <div class="fact"><span>Spot ETF net flow, Oct 21</span><span class="pos">+$528.4M</span></div>
          <div class="fact"><span>FOMC decision</span><span>Wed, Oct 28</span></div>
        </div>
      </div>
      <div class="scen">
        <article><span class="label" style="color:var(--up)">If it reclaims</span><h3>Close above $81.4K</h3><p>Pressure shifts to shorts. <strong>$81.7K</strong> and then the <strong>$84.3K</strong> rebound high from Oct 21 come back into view.</p></article>
        <article><span class="label">If it chops</span><h3>$79.3K – $81.4K</h3><p>Most likely into the Fed. Expect <strong>low conviction</strong> and fake breaks on both sides while funding resets.</p></article>
        <article><span class="label" style="color:var(--down)">If it loses</span><h3>Close below $79.3K</h3><p>A fresh round of <strong>long liquidations</strong> is likely. Watch whether ETF outflows continue after the decision.</p></article>
      </div>
      <p class="fine" style="margin-top:28px">Market commentary for information only. Not investment advice. Data: CoinGecko, CoinGlass and SoSoValue figures as reported Oct 24–25, 2026.</p>
    </div>
  </section>

  <section class="chapter" id="community" aria-labelledby="comH">
    <div class="wrap">
      <div class="chap-head">
        <div><span class="label">V · La communauté</span><h2 id="comH">Community &amp; support</h2></div>
        <p>Market notes and new listings go to the community first. For rebates and sign-up help, message us directly or send a request.</p>
      </div>
      <div class="duo">
        <div>
          <span class="label">Community</span>
          <span class="handle">{CONFIG['telegram_group_name']}</span>
          <p>Desk notes three times a week, new exchange listings, rebate updates and trader discussion.</p>
          <div class="row"><a class="btn" href="{TG_GROUP}" target="_blank" rel="noopener">Join the community</a></div>
          <span class="label" style="margin-top:18px">Direct support</span>
          <span class="handle">@{CONFIG['telegram_dm']}</span>
          <p>Send your UID to claim a rebate, or ask anything about a listed exchange.</p>
          <div class="row"><a class="btn line" href="{TG_DM}" target="_blank" rel="noopener">Message on Telegram</a></div>
        </div>
        <div>
          <span class="label">Support request</span>
          <form class="cs" id="csForm" novalidate>
            <label for="csTg"><span class="label">Your Telegram username</span><input id="csTg" type="text" autocomplete="off" required placeholder="@username"></label>
            <input id="csHp" type="text" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">
            <label for="csTopic"><span class="label">Topic</span><select id="csTopic"><option>Claim my rebate</option><option>Sign-up help</option><option>Referral not applied</option><option>Question about an exchange</option><option>Partnership / listing</option><option>Other</option></select></label>
            <label for="csMsg"><span class="label">Message</span><textarea id="csMsg" required placeholder="Exchange, your UID, and what you need."></textarea></label>
            <div><button class="btn" type="submit">Send request</button></div>
            <p id="csStatus" role="status"></p>
          </form>
        </div>
      </div>
    </div>
  </section>

  <section class="chapter" id="faq" aria-labelledby="faqH">
    <div class="wrap">
      <div class="chap-head"><div><span class="label">VI · Questions</span><h2 id="faqH">Before you trade</h2></div></div>
      <div class="faq">
        <details><summary>How much rebate will I get?</summary><p>Between {min(v['rebate'] for v in VENUES)}% and {max_reb}% of the futures trading fees you pay, depending on the exchange. Each exchange's rate is shown in the list and on its guide page.</p></details>
        <details><summary>Do you need my password or API key?</summary><p>No. We only need the exchange name and your account UID to match your trades to our commission report. Never share your password, 2FA codes or API keys with anyone.</p></details>
        <details><summary>I already have an account. Can I still get the rebate?</summary><p>Usually not. Exchanges link a referral only when the account is created. You would need to open a new account through our link.</p></details>
        <details><summary>What is a perpetual future?</summary><p>A contract that tracks an asset's price with no expiry date. You post margin and can go long or short with leverage. A funding payment between longs and shorts, usually every 8 hours, keeps the price close to spot.</p></details>
        <details><summary>How does liquidation work?</summary><p>If losses eat your margin down to the maintenance level, the exchange closes your position. At 10× leverage, a move of roughly 9–10% against you can wipe out isolated margin.</p></details>
        <details><summary>CEX or perp DEX?</summary><p>A centralized exchange is easier to start with and usually has deeper liquidity, but it holds your funds. A perp DEX lets you trade from your own wallet, so you keep custody, but you manage your own keys and pay network fees.</p></details>
        <details><summary>Can I use these exchanges where I live?</summary><p>Maybe not. Each exchange decides who it serves. Check the exchange's terms for your country before registering. This site is not for residents of the jurisdictions listed below.</p></details>
      </div>
    </div>
  </section>
</main>
{footer('')}
{FAB}
<script>
window.LANG="en"; window.LANG_ALT="ko/index.html";
{COMMON_JS}
{FX_JS}
const CONTACT = {{ telegram:"{CONFIG['telegram_dm']}", formEndpoint:"{CONFIG['form_endpoint']}" }};
const VENUES = {js_venues};
const SNAP = {{ price:80300, lo:79263, hi:81445, chg:null, when:"Oct 25, 2026" }};
const LEVELS = [
  {{ p:84333, label:"Oct 21 rebound high", kind:"r" }},
  {{ p:81668, label:"Oct 23 level", kind:"r" }},
  {{ p:81445, label:"24h high · resistance", kind:"r" }},
  {{ p:79263, label:"24h low · support", kind:"s" }}
];
"""
    page += CAROUSEL_JS_SRC + INDEX_JS
    return page

CAROUSEL_JS_SRC = r"""
/* ---- stage carousel ---- */
(function(){
  const st=$("stage"); if(!st) return;
  const tr=$("stageTrack"), slides=[...tr.children], dots=[...st.querySelectorAll(".stage-dots button")];
  const UI=["auto","light","light","auto"]; let i=0, timer=null, paused=FX.reduce, hover=false;
  function go(n){
    i=(n+slides.length)%slides.length; tr.style.transform=`translateX(${-100*i}%)`;
    slides.forEach((s,k)=>{ const on=k===i; s.classList.toggle("on",on); s.setAttribute("aria-hidden",String(!on)); s.querySelectorAll("a,button").forEach(a=>a.tabIndex=on?0:-1); });
    dots.forEach((d,k)=>{ d.setAttribute("aria-selected",String(k===i)); d.classList.remove("run"); void d.offsetWidth; if(k===i&&!paused&&!hover) d.classList.add("run"); });
    st.dataset.ui=UI[i]; schedule();
  }
  function schedule(){ clearTimeout(timer); if(!paused&&!hover) timer=setTimeout(()=>go(i+1),7000); }
  dots.forEach((d,k)=>d.addEventListener("click",()=>go(k)));
  $("stagePrev").addEventListener("click",()=>go(i-1));
  $("stageNext").addEventListener("click",()=>go(i+1));
  const pb=$("stagePause");
  function setPaused(p){ paused=p; pb.textContent=p?"▶":"❙❙"; pb.setAttribute("aria-label",p?"Play slideshow":"Pause slideshow"); go(i); }
  pb.addEventListener("click",()=>setPaused(!paused)); if(paused) setPaused(true);
  st.addEventListener("mouseenter",()=>{ hover=true; clearTimeout(timer); dots.forEach(d=>d.classList.remove("run")); });
  st.addEventListener("mouseleave",()=>{ hover=false; go(i); });
  st.addEventListener("keydown",e=>{ if(e.key==="ArrowRight") go(i+1); if(e.key==="ArrowLeft") go(i-1); });
  let x0=null; st.addEventListener("pointerdown",e=>{ x0=e.clientX; });
  st.addEventListener("pointerup",e=>{ if(x0==null) return; const dx=e.clientX-x0; x0=null; if(Math.abs(dx)>50) go(dx<0?i+1:i-1); });
  document.addEventListener("visibilitychange",()=>{ if(document.hidden) clearTimeout(timer); else schedule(); });
  go(0);
})();
"""

INDEX_JS = r"""
/* tabs */
function openTab(k, focus){
  ["cex","dex"].forEach(t=>{ const on=t===k, tab=$("tab-"+t); tab.setAttribute("aria-selected",on); tab.tabIndex=on?0:-1; $("panel-"+t).hidden=!on; if(on&&focus) tab.focus(); });
}
["cex","dex"].forEach(t=>$("tab-"+t).addEventListener("click",()=>openTab(t)));
document.querySelector(".tabs").addEventListener("keydown",e=>{ if(e.key==="ArrowRight"||e.key==="ArrowLeft") openTab($("tab-cex").getAttribute("aria-selected")==="true"?"dex":"cex",true); });
if(location.hash==="#dex") openTab("dex");

/* calculator */
let mode="taker";
function calc(){
  const n=Math.max(0,parseFloat($("notional").value)||0), t=Math.max(1,parseInt($("trades").value)||1), reb=$("withReb").checked;
  const money=x=>"$"+x.toLocaleString("en-US",{minimumFractionDigits:2,maximumFractionDigits:2});
  const data=VENUES.filter(v=>v[mode]!=null).map(v=>{ const g=n*(v[mode]/100)*2*t; return {name:v.name,g,net:reb?g*(1-v.rebate/100):g}; }).sort((a,b)=>a.net-b.net);
  const max=Math.max(...data.map(d=>d.g),0.0001); const box=$("bars"); box.textContent="";
  data.forEach(d=>{
    const row=document.createElement("div"); row.className="bar";
    row.innerHTML='<span class="n"></span><div class="track"><div class="fill"></div><div class="fill reb"></div></div><span class="v"></span>';
    row.querySelector(".n").textContent=d.name;
    const fills=row.querySelectorAll(".fill");
    fills[0].style.width=(d.g/max*100)+"%"; fills[0].style.opacity=reb?.18:1;
    fills[1].style.width=reb?(d.net/max*100)+"%":"0";
    row.querySelector(".v").textContent=money(d.net);
    box.appendChild(row);
  });
  const saved=data.reduce((s,d)=>s+(d.g-d.net),0)/Math.max(data.length,1);
  $("calcNote").textContent = reb
    ? `${t} round trips a month at $${fmt(n)}, after rebate. The faint line is the fee before rebate; on average the rebate saves ${money(saved)} a month. Funding not included.`
    : `${t} round trips a month at $${fmt(n)}, before rebate. Funding not included.`;
}
["notional","trades","withReb"].forEach(id=>$(id).addEventListener("input",calc));
$("otTaker").addEventListener("click",()=>{mode="taker";$("otTaker").setAttribute("aria-pressed","true");$("otMaker").setAttribute("aria-pressed","false");calc();});
$("otMaker").addEventListener("click",()=>{mode="maker";$("otMaker").setAttribute("aria-pressed","true");$("otTaker").setAttribute("aria-pressed","false");calc();});
calc();

/* ladder */
function drawLadder(price){
  const svg=$("ladder"), NS="http://www.w3.org/2000/svg"; svg.textContent="";
  const ps=LEVELS.map(l=>l.p).concat(price), top=Math.max(...ps)+600, bot=Math.min(...ps)-600;
  const y=p=>16+(top-p)/(top-bot)*(300-32), css=getComputedStyle(document.documentElement), c=k=>css.getPropertyValue(k).trim();
  const el=(t,a)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);svg.appendChild(e);return e;};
  const ls=[...LEVELS].sort((a,b)=>b.p-a.p); let lastLab=-99, lastNum=-99;
  ls.forEach(l=>{
    const yy=y(l.p), col=l.kind==="s"?c("--up"):c("--down");
    el("line",{x1:80,x2:420,y1:yy,y2:yy,stroke:col,"stroke-width":1,"stroke-dasharray":"2 5"});
    const ny=Math.max(yy+4,lastNum+15); lastNum=ny;
    el("text",{x:0,y:ny,"font-family":"Jost, sans-serif","font-size":12,fill:c("--muted")}).textContent=fmt(l.p);
    let ly=yy-7; if(ly<lastLab+15) ly=yy+15; lastLab=ly;
    el("text",{x:420,y:ly,"text-anchor":"end","font-family":"Jost, sans-serif","font-size":11,"letter-spacing":"1.5",fill:col}).textContent=l.label.toUpperCase();
  });
  const py=y(price);
  el("line",{x1:80,x2:420,y1:py,y2:py,stroke:c("--ink"),"stroke-width":1.5});
  el("text",{x:0,y:py+6,"font-family":"DM Serif Display, serif","font-size":18,fill:c("--ink")}).textContent=fmt(price);
}
let lastPrice=SNAP.price;
try{ matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>drawLadder(lastPrice)); new MutationObserver(()=>drawLadder(lastPrice)).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]}); }catch(e){}
function render(d,live){
  lastPrice=d.price; $("priceVal").textContent=fmt(d.price); $("pillPrice").textContent="$"+fmt(d.price); if($("stageBtc")) $("stageBtc").textContent="$"+fmt(d.price);
  $("lo").textContent=d.lo?fmt(d.lo):"—"; $("hi").textContent=d.hi?fmt(d.hi):"—";
  const ch=$("chg"); if(d.chg==null){ch.textContent="—";ch.className="chg";} else {ch.textContent=(d.chg>=0?"+":"")+d.chg.toFixed(2)+"%";ch.className="chg "+(d.chg>=0?"up":"down");}
  $("upd").textContent=d.when; $("feedLabel").textContent=live?"Live":"Snapshot · "+SNAP.when; drawLadder(d.price);
}
render(SNAP,false);
async function pull(){
  try{ const r=await fetch("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin",{cache:"no-store"}); if(!r.ok) throw 0; const j=(await r.json())[0];
    render({price:j.current_price,lo:j.low_24h,hi:j.high_24h,chg:j.price_change_percentage_24h,when:new Date().toLocaleTimeString("en-US",{hour:"2-digit",minute:"2-digit"})},true);
  }catch(e){}
}
pull(); setInterval(pull,60000);

/* support form -> Telegram (via worker) */
$("csForm").addEventListener("submit",async e=>{
  e.preventDefault();
  const st=$("csStatus"), msg=$("csMsg").value.trim(), tp=$("csTopic").value, hp=$("csHp").value;
  let tg=$("csTg").value.trim().replace(/^https?:\/\/t\.me\//,"");
  if(hp) return;
  if(!/^@?[A-Za-z0-9_]{5,32}$/.test(tg)){ st.className="err"; st.textContent="Enter your Telegram username, like @username, so we can reply."; $("csTg").focus(); return; }
  if(!tg.startsWith("@")) tg="@"+tg;
  if(msg.length<10){ st.className="err"; st.textContent="Add a few more details to your message."; $("csMsg").focus(); return; }
  if(CONTACT.formEndpoint){
    try{
      const r=await fetch(CONTACT.formEndpoint.replace(/\/$/,"")+"/cs",{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify({telegram:tg,topic:tp,message:msg,page:location.href,website:hp})});
      if(!r.ok) throw 0;
      st.className="ok"; st.textContent="Request sent. We'll message "+tg+" on Telegram."; $("csForm").reset(); return;
    }catch(err){ st.className="err"; st.textContent="Couldn't send right now. Message us directly on Telegram @"+CONTACT.telegram+"."; return; }
  }
  st.className=""; st.textContent="Message us directly on Telegram @"+CONTACT.telegram+" and paste your question there.";
  window.open("https://t.me/"+CONTACT.telegram,"_blank","noopener");
});
</script>
"""

# ============ EXCHANGE PAGES ============
def build_exchange(v, idx):
    tone = TONES[idx % len(TONES)]
    variant = idx % 3  # 0: tone block, 1: centered type, 2: split
    rk = ranked(VENUES)
    known = [x for x in rk if x["taker"] is not None]
    name, r = v["name"], v["rebate"]
    n_t, n_m = net(v["taker"], r), net(v["maker"], r)
    # monthly example: $10k, 20 round trips, taker
    ex = None
    if v["taker"] is not None:
        gross = 10000 * v["taker"] / 100 * 2 * 20
        ex = (gross, gross * r / 100, gross * (1 - r / 100))
    rank_line = ""
    if v["taker"] is not None:
        pos = [x["slug"] for x in known].index(v["slug"]) + 1
        rest = [x for x in known if x["slug"] != v["slug"]]
        cheaper_after = sum(1 for x in rest if x["taker"] > n_t)
        tail = ("every other venue on our list" if cheaper_after == len(rest)
                else f"{cheaper_after} of the other {len(rest)} venues")
        rank_line = (f"{name}'s headline taker fee ranks No. {pos} of {len(known)} venues with a verified fee. "
                     f"After the {r}% rebate, the {pct(n_t)} you actually pay is below the headline taker fee of {tail}.")
    code_html = (f"""<div class="kv"><span class="label">Referral code</span>
          <span class="code"><b id="code">{esc(v['code'])}</b><button type="button" class="btn line sm" id="copyCode">Copy</button></span></div>"""
        if v["code"] else
        """<div class="kv"><span class="label">Referral code</span><span class="code"><b style="font-size:20px">Applied automatically</b></span><span class="fine">Use our sign-up link and the referral is attached for you.</span></div>""")
    title = f"{name} Referral Code 2026: {r}% Fee Rebate | {CONFIG['brand']}"
    desc = (f"{name} referral code" + (f" {v['code']}" if v['code'] else "") +
            f": sign up through {CONFIG['brand']} and get {r}% of your {name} futures trading fees back in USDT every week. Fees, sign-up steps and FAQ.")
    canonical = f"{CONFIG['domain']}/exchanges/{v['slug']}.html"
    faqs = [
        (f"What is the {name} referral code?",
         (f"Our {name} referral code is {v['code']}. " if v['code'] else f"Our {name} referral is applied through our sign-up link, so there is no code to type. ") +
         f"Register through our link, then send your UID to @{CONFIG['telegram_dm']} on Telegram to activate the {r}% fee rebate."),
        (f"How much rebate do I get on {name}?",
         f"{CONFIG['brand']} returns {r}% of the futures trading fees you pay on {name}, paid weekly in USDT." +
         (f" On the standard taker fee of {pct(v['taker'])}, that brings your effective rate to {pct(n_t)}." if n_t is not None else "")),
        (f"What are {name} futures fees?",
         (f"The standard (non-VIP) USDT-margined perpetual fee on {name} is {pct(v['maker'])} maker and {pct(v['taker'])} taker, checked {CONFIG['fees_checked']}. Your live account rate applies."
          if v['taker'] is not None else f"We could not verify {name}'s current published futures fee. Check the fee page on the exchange after signing up.")),
        (f"Can I add a {name} referral code to an existing account?",
         f"Usually not. Exchanges link a referral when the account is created, so the rebate requires a new {name} account opened through our link."),
        ("Do you need my password or API key?",
         "No. We only need the exchange name and your account UID. Never share your password, 2FA codes or API keys with anyone."),
        (f"Is {name} available in my country?",
         f"{name} decides which countries it serves. Check its terms for your country before registering. This site is not for residents of the Republic of Korea or the United States."),
    ]
    ld = [
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":CONFIG['brand'],"item":CONFIG['domain']+"/"},
            {"@type":"ListItem","position":2,"name":f"{name} referral code","item":canonical}]},
    ]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    others = [x for x in rk if x["slug"] != v["slug"]][:5]
    others_html = "".join(f"""<a class="other" href="{x['slug']}.html"><span class="on">{esc(x['name'])}</span><span class="label">{x['rebate']}% rebate · taker {pct(x['taker']) if x['taker'] is not None else 'n/a'}</span></a>""" for x in others)
    signup = esc(link(v, v["slug"]))

    if variant == 0:
        hero = f"""<section class="xhero v0"><canvas class="fx" data-fx="silk" data-col="tone-ink" aria-hidden="true"></canvas>
      <div class="wrap">
        <span class="label" style="color:inherit;opacity:.8">{CONFIG['brand']} · Édition {tone[0]}</span>
        {logo(v,'../','xlogo')}<h1>{esc(name)}</h1>
        <p class="tag">Referral code &amp; <em>{r}% fee rebate</em></p>
        <div class="cta"><a class="btn inv" href="{signup}" target="_blank" rel="sponsored nofollow noopener">Sign up to {esc(name)}</a><a class="btn inv line" href="#claim">Claim the rebate</a></div>
      </div>
    </section>"""
    elif variant == 1:
        hero = f"""<section class="xhero v1"><canvas class="fx" data-fx="silk" aria-hidden="true"></canvas><div class="wrap">
        <span class="label">{CONFIG['brand']} · Édition {tone[0]}</span>
        {logo(v,'../','xlogo')}<h1>{esc(name)}</h1>
        <span class="bar-tone" aria-hidden="true"></span>
        <p class="tag">Referral code &amp; <em>{r}% of your fees, returned</em></p>
        <div class="cta"><a class="btn tone" href="{signup}" target="_blank" rel="sponsored nofollow noopener">Sign up to {esc(name)}</a><a class="btn line" href="#claim">Claim the rebate</a></div>
      </div></section>"""
    else:
        hero = f"""<section class="xhero v2"><canvas class="fx" data-fx="silk" aria-hidden="true"></canvas><div class="wrap split">
        <div>
          <span class="label">{CONFIG['brand']} · Édition {tone[0]}</span>
          {logo(v,'../','xlogo')}<h1>{esc(name)}</h1>
          <p class="tag">Referral code &amp; <em>fee rebate</em></p>
          <div class="cta"><a class="btn" href="{signup}" target="_blank" rel="sponsored nofollow noopener">Sign up to {esc(name)}</a><a class="btn line" href="#claim">Claim the rebate</a></div>
        </div>
        <div class="bigpct" aria-hidden="true"><span>{r}</span><i>%</i></div>
      </div></section>"""

    xcss = """
.xhero{padding-block:clamp(64px,10vw,140px)}
.xhero h1{font-size:clamp(64px,13vw,176px);line-height:.92;letter-spacing:-.02em;margin:18px 0 10px}
.xhero .tag{font-family:var(--display);font-size:clamp(22px,2.6vw,32px);font-weight:400}
.xhero .tag em{font-style:italic}
.xhero .cta{margin-top:34px}
.xhero.v0{background:var(--tone);color:var(--tone-ink)}
.xhero.v0 .label{color:var(--tone-ink)}
.btn.inv{background:var(--tone-ink);border-color:var(--tone-ink);color:var(--tone)}
.btn.inv:hover{background:transparent;color:var(--tone-ink)}
.btn.inv.line{background:transparent;color:var(--tone-ink)}
.btn.inv.line:hover{background:var(--tone-ink);color:var(--tone)}
.xhero.v1{text-align:center}
.xhero.v1 .cta{justify-content:center}
.xhero.v1 h1 {color:var(--ink)}
.bar-tone{display:block;width:72px;height:3px;background:var(--tone);margin:30px auto 22px}
.xhero.v1 .tag em,.xhero.v2 .tag em{color:var(--tone)}
.split{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:40px;align-items:center}
@media (max-width:820px){.split{grid-template-columns:1fr}}
.bigpct{font-family:var(--display);color:var(--tone);line-height:.8;text-align:right;white-space:nowrap}
.bigpct span{font-size:clamp(140px,22vw,300px)}
.bigpct i{font-size:clamp(60px,8vw,110px);font-style:italic}
@media (max-width:820px){.bigpct{text-align:left}}
.facts4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--ink);border-bottom:1px solid var(--hair)}
.facts4 .kv{padding:26px 22px 26px 0;display:flex;flex-direction:column;gap:10px;min-width:0}
.facts4 .kv + .kv{padding-left:22px;border-left:1px solid var(--hair)}
.facts4 b{font-family:var(--display);font-weight:400;font-size:clamp(28px,3vw,40px);line-height:1}
.facts4 b.mt{font-size:clamp(24px,2.3vw,32px)}
.facts4 .tone b{color:var(--tone)}
.code{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.code b{letter-spacing:.06em;word-break:break-all}
@media (max-width:900px){.facts4{grid-template-columns:1fr 1fr}.facts4 .kv:nth-child(3){padding-left:0;border-left:0}.facts4 .kv:nth-child(n+3){border-top:1px solid var(--hair)}}
@media (max-width:480px){.facts4{grid-template-columns:1fr}.facts4 .kv + .kv{padding-left:0;border-left:0;border-top:1px solid var(--hair)}}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px}
@media (max-width:860px){.two{grid-template-columns:1fr}}
.about p{font-size:19px;font-weight:300;max-width:56ch}
.about p + p{margin-top:16px;color:var(--muted);font-size:16px}
.ledger{border-top:1px solid var(--ink)}
.ledger div{display:flex;justify-content:space-between;gap:16px;padding-block:15px;border-bottom:1px solid var(--hair)}
.ledger div span:first-child{color:var(--muted)}
.ledger div span:last-child{font-variant-numeric:tabular-nums;font-weight:500}
.ledger .tot span:last-child{font-family:var(--display);font-size:28px;font-weight:400;color:var(--tone)}
.olist{list-style:none;margin:0;padding:0;border-top:1px solid var(--ink);counter-reset:s}
.olist li{display:grid;grid-template-columns:64px minmax(0,1fr);gap:16px;padding-block:22px;border-bottom:1px solid var(--hair);counter-increment:s}
.olist li::before{content:counter(s,upper-roman);font-family:var(--display);font-style:italic;font-size:26px;color:var(--tone);line-height:1.1}
.olist b{font-weight:500;display:block;margin-bottom:4px}
.olist p{color:var(--muted);font-weight:300}
.others{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border-top:1px solid var(--ink)}
.other{padding:22px 18px 22px 0;display:flex;flex-direction:column;gap:6px;text-decoration:none}
.other + .other{padding-left:18px;border-left:1px solid var(--hair)}
.other .on{font-family:var(--display);font-size:26px}
.other:hover .on{color:var(--tone)}
@media (max-width:900px){.others{grid-template-columns:1fr 1fr}.other + .other{padding-left:0;border-left:0}.other{border-bottom:1px solid var(--hair)}}
.crumbs{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding-block:18px}
.crumbs a{text-decoration:none;display:inline-block;padding-block:10px}
"""
    fee_cards = f"""<div class="kv"><span class="label">Maker / taker</span><b class="num mt">{pct(v['maker'])} / {pct(v['taker'])}</b></div>""" if v["taker"] is not None else """<div class="kv"><span class="label">Maker / taker</span><b style="font-size:20px">Check site</b></div>"""
    net_card = f"""<div class="kv tone"><span class="label">Taker you pay</span><b class="num">{pct(n_t)}</b></div>""" if n_t is not None else f"""<div class="kv tone"><span class="label">Paid weekly in</span><b>USDT</b></div>"""
    ledger = (f"""<div class="ledger">
          <div><span>Position size</span><span>$10,000</span></div>
          <div><span>Round trips per month</span><span>20</span></div>
          <div><span>Taker fees paid to {esc(name)}</span><span>${ex[0]:,.2f}</span></div>
          <div><span>{CONFIG['brand']} rebate ({r}%)</span><span class="pos">+${ex[1]:,.2f}</span></div>
          <div class="tot"><span>Net cost per month</span><span>${ex[2]:,.2f}</span></div>
        </div>
        <p class="fine" style="margin-top:14px">Example at the standard taker rate. Funding payments not included.</p>""" if ex else
        f"""<p class="fine">We'll add a worked example once {esc(name)}'s fee is verified. The {r}% rebate applies to whatever futures fee you pay.</p>""")

    page = f"""{head(title, desc, canonical, ld_html, tone)}
<style>{xcss}</style>
<!--BODY-->
{header('../')}
<main>
  <div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">{CONFIG['brand']}</a> / <a href="../index.html#venues">Exchanges</a> / {esc(name)}</nav></div>
  {hero}
  {marquee([x for x in rk if x["slug"] != v["slug"]], "../")}
  <div class="wrap" style="margin-top:clamp(40px,6vw,72px)">
    <div class="facts4">
      {code_html}
      <div class="kv tone"><span class="label">Fee rebate</span><b class="num">{r}%</b></div>
      {fee_cards}
      {net_card}
    </div>
  </div>

  <section class="chapter" style="border-top:0">
    <div class="wrap two">
      <div class="about">
        <span class="label">I · L'essentiel</span>
        <h2 style="margin:16px 0 28px">About {esc(name)}</h2>
        <p>{esc(v['about'])}</p>
        {f'<p>{esc(rank_line)}</p>' if rank_line else ''}
      </div>
      <div>
        <span class="label">II · Le calcul</span>
        <h2 style="margin:16px 0 28px">A month on {esc(name)}</h2>
        {ledger}
      </div>
    </div>
  </section>

  <section class="chapter">
    <div class="wrap two">
      <div>
        <span class="label">III · L'inscription</span>
        <h2 style="margin:16px 0 28px">How to sign up</h2>
        <ol class="olist">
          <li><div><b>Open our {esc(name)} link</b><p>Use the Sign up button on this page so the referral is attached to your new account.</p></div></li>
          <li><div><b>Register</b><p>Create the account with your email or phone and set a strong password and 2FA.</p></div></li>
          <li><div><b>Verify if asked</b><p>Complete identity verification if {esc(name)} requires it for your country or for futures access.</p></div></li>
          <li><div><b>Fund and open futures</b><p>Deposit USDT, transfer it to your futures account and start with low leverage.</p></div></li>
        </ol>
        <div class="cta" style="margin-top:28px"><a class="btn" href="{signup}" target="_blank" rel="sponsored nofollow noopener">Sign up to {esc(name)}</a></div>
      </div>
      <div id="claim">
        <span class="label">IV · La remise</span>
        <h2 style="margin:16px 0 28px">Claim your {r}% rebate</h2>
        <ol class="olist">
          <li><div><b>Find your UID</b><p>In {esc(name)}, open your profile. Your UID is the account number shown there.</p></div></li>
          <li><div><b>Send it on Telegram</b><p>Send "{esc(name)} + your UID" to <a href="{TG_DM}" target="_blank" rel="noopener">@{CONFIG['telegram_dm']}</a> on Telegram. We confirm within 24 hours.</p></div></li>
          <li><div><b>Get paid every Monday</b><p>Your rebate for the previous week arrives in USDT. Minimum 10 USDT; smaller amounts roll over.</p></div></li>
        </ol>
        <div class="cta" style="margin-top:28px"><a class="btn line" href="{TG_DM}" target="_blank" rel="noopener">Send my UID</a></div>
      </div>
    </div>
  </section>

  <section class="chapter">
    <div class="wrap">
      <div class="chap-head"><div><span class="label">V · Questions</span><h2>{esc(name)} referral FAQ</h2></div></div>
      <div class="faq">
        {''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in faqs)}
      </div>
    </div>
  </section>

  <section class="chapter">
    <div class="wrap">
      <div class="chap-head"><div><span class="label">VI · Ailleurs</span><h2>Other exchanges</h2></div><p>Every venue is ranked on the home page by fee, with its rebate.</p></div>
      <div class="others">{others_html}</div>
    </div>
  </section>
</main>
{footer('../')}
{FAB}
<script>
window.HOME="../index.html"; window.LANG="en"; window.LANG_ALT="../ko/exchanges/{v['slug']}.html";
{COMMON_JS}
{FX_JS}
btcPill();
const cc=$("copyCode");
if(cc) cc.addEventListener("click",async()=>{{
  try{{ await navigator.clipboard.writeText($("code").textContent); cc.textContent="Copied"; }}
  catch(e){{ const r=document.createRange(); r.selectNodeContents($("code")); const s=getSelection(); s.removeAllRanges(); s.addRange(r); cc.textContent="Selected"; }}
  setTimeout(()=>cc.textContent="Copy",1600);
}});
</script>
"""
    return page

import sys as _sys
_sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from i18n_ko import translate as _ko

def ko_doc(doc, depth_alt, alt_href, canon):
    d = _ko(doc)
    d = d.replace('<html lang="en">', '<html lang="ko">', 1)
    d = d.replace('<head><meta charset="utf-8">', f'<head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow">', 1)
    d = d.replace("</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600&family=Noto+Sans+KR:wght@300;400;500&display=swap">'
                  '<style>:root{--display:"DM Serif Display","Noto Serif KR",serif;--sans:"Jost","Noto Sans KR",system-ui,sans-serif}'
                  '.label,.tab,.btn,.top nav a,.top .right a{letter-spacing:.08em}h1,h2,h3,summary{word-break:keep-all}p,li{word-break:keep-all}</style></head>', 1)
    d = d.replace('window.LANG="en";', 'window.LANG="ko";').replace('window.LANG_ALT="ko/index.html"', f'window.LANG_ALT="{alt_href}"')
    d = re.sub(r'window\.LANG_ALT="\.\./ko/exchanges/[a-z0-9]+\.html"', f'window.LANG_ALT="{alt_href}"', d)
    d = d.replace('src="assets/logos/', f'src="{depth_alt}assets/logos/').replace('src="../assets/logos/', f'src="{depth_alt}../assets/logos/')
    d = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canon}">', d, count=1)
    return d

def full_doc(page):
    h, b = page.split("<!--BODY-->", 1)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            + h + "</head><body>" + b + "</body></html>\n")

PREVIEW = OUT / ".preview"  # artifact preview copy (git-ignored)

def build():
    for root in (OUT, PREVIEW):
        (root / "exchanges").mkdir(parents=True, exist_ok=True)
    idx = build_index()
    (OUT / "index.html").write_text(full_doc(idx), encoding="utf-8")
    (OUT / "ko" / "exchanges").mkdir(parents=True, exist_ok=True)
    (OUT / "ko" / "index.html").write_text(ko_doc(full_doc(idx), "../", "../index.html", CONFIG["domain"] + "/"), encoding="utf-8")
    (PREVIEW / "index.html").write_text(idx.replace("<!--BODY-->", ""), encoding="utf-8")  # artifact adds its own skeleton
    for i, v in enumerate(ranked(VENUES)):
        doc = full_doc(build_exchange(v, i))
        (OUT / "exchanges" / f"{v['slug']}.html").write_text(doc, encoding="utf-8")
        (OUT / "ko" / "exchanges" / f"{v['slug']}.html").write_text(
            ko_doc(doc, "../", f"../../exchanges/{v['slug']}.html", f"{CONFIG['domain']}/exchanges/{v['slug']}.html"), encoding="utf-8")
        (PREVIEW / "exchanges" / f"{v['slug']}.html").write_text(doc, encoding="utf-8")
    lp = full_doc(build_landing())
    (OUT / "start.html").write_text(lp.replace('<head><meta charset="utf-8">', '<head><meta charset="utf-8"><meta name="robots" content="noindex">', 1), encoding="utf-8")
    nf = full_doc(head(f"Page not found | {CONFIG['brand']}", "This page does not exist.", CONFIG["domain"] + "/404.html") +
        f"""<!--BODY-->{header(CONFIG['domain'] + '/')}<main><section class="hero center" style="min-height:60vh;justify-content:center">
<span class="label">Erreur 404</span><h1>This page has <em>moved on.</em></h1>
<p class="lede">The page you opened does not exist. The exchanges and rebates are on the home page.</p>
<div class="cta"><a class="btn" href="{CONFIG['domain']}/">Back to Perpline</a><a class="btn line" href="{TG_DM}" target="_blank" rel="noopener">Ask on Telegram</a></div>
</section></main>{footer(CONFIG['domain'] + '/')}<script>{COMMON_JS}btcPill();</script>""")
    nf = nf.replace("<div class=\"fab\">", "<div class=\"fab\" hidden>")
    (OUT / "404.html").write_text(nf.replace('<head><meta charset="utf-8">', '<head><meta charset="utf-8"><meta name="robots" content="noindex">', 1), encoding="utf-8")
    today = datetime.date.today().isoformat()
    urls = [CONFIG["domain"] + "/"] + [f"{CONFIG['domain']}/exchanges/{v['slug']}.html" for v in ranked(VENUES)]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {CONFIG['domain']}/sitemap.xml\n", encoding="utf-8")
    wdir = OUT / "worker"; wdir.mkdir(exist_ok=True)
    tpl = (pathlib.Path(__file__).resolve().parent / "worker.template.js").read_text(encoding="utf-8")
    refs = {v["slug"]: v["ref"] for v in VENUES + DEX}
    (wdir / "worker.js").write_text(tpl.replace("/*REFS*/{}", json.dumps(refs, indent=2)), encoding="utf-8")
    print("built", len(VENUES), "exchange pages ->", OUT)

if __name__ == "__main__":
    build()
