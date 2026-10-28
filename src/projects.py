"""Perpline · Projects — Project of the Week / Month (partner features).
Data: src/projects.json. Process: chainbrief docs/PROJECT_PROMO.md."""
import json, pathlib, datetime

DATA = pathlib.Path(__file__).resolve().parent / "projects.json"

CSS = """
.pj-hero{padding-block:clamp(56px,8vw,104px) clamp(36px,5vw,64px);border-bottom:1px solid var(--hair)}
.pj-hero h1{font-size:clamp(48px,7vw,96px)}
.pj-hero .lede{margin-top:20px}
.pj-slot{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:clamp(28px,5vw,72px);align-items:center}
@media (max-width:820px){.pj-slot{grid-template-columns:1fr}}
.pj-vis{position:relative;aspect-ratio:16/10;overflow:hidden;background:var(--wash)}
.pj-vis img.cv{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.8,.2,1)}
.pj-slot:hover .pj-vis img.cv{transform:scale(1.035)}
.pj-vis .lg{position:absolute;left:20px;bottom:20px;width:60px;height:60px;border-radius:50%;box-shadow:0 8px 24px rgba(0,0,0,.25)}
.pj-vis .badge{position:absolute;right:16px;top:16px;background:var(--paper);color:var(--ink);font-size:11px;letter-spacing:.2em;text-transform:uppercase;padding:7px 11px}
.pj-txt h2{font-size:clamp(40px,4.6vw,64px);margin:10px 0 14px}
.pj-txt .hl{font-family:var(--display);font-style:italic;font-size:clamp(22px,2vw,28px);line-height:1.25;margin:0 0 20px}
.pj-txt ul{list-style:none;margin:0 0 26px;padding:0;border-top:1px solid var(--hair)}
.pj-txt li{padding:12px 0;border-bottom:1px solid var(--hair);font-size:15.5px;font-weight:300;line-height:1.55}
.pj-meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin-bottom:6px}
.pj-links{display:flex;flex-wrap:wrap;gap:10px}
.pj-links .btn{padding:13px 20px}
.pj-empty{border:1px dashed var(--hair);padding:40px;text-align:center;color:var(--muted)}
.pj-arch{display:grid;gap:0;border-top:1px solid var(--ink)}
.pj-arch a{display:grid;grid-template-columns:52px minmax(0,1fr) auto;gap:16px;align-items:center;padding:16px 0;border-bottom:1px solid var(--hair);text-decoration:none}
.pj-arch img{width:40px;height:40px;border-radius:50%}
.pj-disc{font-size:13px;color:var(--muted);max-width:70ch;margin-top:28px;line-height:1.6}
"""

def load():
    try:
        return json.loads(DATA.read_text(encoding="utf-8")).get("items", [])
    except FileNotFoundError:
        return []

def current(items, slot, today=None):
    today = today or (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date().isoformat()  # KST
    live = [p for p in items if p.get("slot") == slot and not p.get("archive") and p.get("start", "") <= today <= p.get("end", "9999")]
    return live[0] if live else None

def slot_html(p, esc, kind):
    if not p:
        return f'<div class="pj-empty">No {kind.lower()} feature right now. Projects can apply on Telegram.</div>'
    pts = "".join(f"<li>{esc(t)}</li>" for t in p.get("points", []))
    links = "".join(f'<a class="btn{" line" if i else ""}" href="{esc(h)}" target="_blank" rel="noopener sponsored">{esc(t)}</a>'
                    for i, (t, h) in enumerate([(("Visit " + p["website"].replace("https://", "")), p.get("website")), ("Full story", p.get("story")), ("X", p.get("x")), ("Telegram", p.get("telegram"))]) if h)
    return f"""<article class="pj-slot">
  <div class="pj-vis"><img class="cv" src="assets/projects/{esc(p['slug'])}/cover.jpg" alt="{esc(p['name'])}" loading="lazy" decoding="async"><img class="lg" src="assets/projects/{esc(p['slug'])}/logo.png" alt=""><span class="badge">Sponsored</span></div>
  <div class="pj-txt">
    <div class="pj-meta"><span class="label">{esc(kind)}</span><span class="label">{esc(p.get('label',''))}</span><span class="label">{esc(p.get('sector',''))}</span></div>
    <h2>{esc(p['name'])}</h2>
    <p class="hl">{esc(p.get('headline',''))}</p>
    <ul>{pts}</ul>
    <div class="pj-links">{links}</div>
  </div>
</article>"""

def build_projects(head, header, footer, esc, common_js, config, tg_dm, fab=''):
    items = load()
    week, month = current(items, "week"), current(items, "month")
    shown = {id(week), id(month)}
    past = [p for p in items if id(p) not in shown]
    arch = "".join(f'<a href="{esc(p.get("story") or p.get("website"))}" target="_blank" rel="noopener sponsored"><img src="assets/projects/{esc(p["slug"])}/logo.png" alt=""><span><b>{esc(p["name"])}</b> · {esc(p.get("headline",""))}</span><span class="label">{esc(p.get("label",""))}</span></a>' for p in past)
    page = head(f"Projects — Project of the Week & Month | {config['brand']}",
                "Crypto and AI projects featured by Perpline each week and month. Partner features, clearly labelled.",
                config["domain"] + "/projects.html") + f"""<style>{CSS}</style><!--BODY-->{header('')}
<main>
  <section class="pj-hero"><div class="wrap">
    <span class="label">VII · Les projets</span>
    <h1>Projects, <em>picked weekly.</em></h1>
    <p class="lede">One project for the week, one for the month. Short, plain summaries with official links. Every feature is a paid or partner placement and is labelled as such.</p>
  </div></section>
  <section class="chapter" style="border-top:0"><div class="wrap">
    <div class="chap-head"><div><span class="label">I · La semaine</span><h2>Project of the Week</h2></div><p>Seven days on the front of this page.</p></div>
    {slot_html(week, esc, "Project of the Week")}
  </div></section>
  <section class="chapter"><div class="wrap">
    <div class="chap-head"><div><span class="label">II · Le mois</span><h2>Project of the Month</h2></div><p>A longer run for projects building over the whole month.</p></div>
    {slot_html(month, esc, "Project of the Month")}
  </div></section>
  {f'<section class="chapter"><div class="wrap"><div class="chap-head"><div><span class="label">III · Archives</span><h2>Past features</h2></div></div><div class="pj-arch">{arch}</div></div></section>' if arch else ''}
  <section class="chapter"><div class="wrap">
    <div class="chap-head"><div><span class="label">Contact</span><h2>Feature your project</h2></div><p>Weekly and monthly slots, with a matching story on CHAINBRIEF in English, Korean and Chinese.</p></div>
    <a class="btn" href="{tg_dm}" target="_blank" rel="noopener">Ask on Telegram</a>
    <p class="pj-disc">Features are partner content based on material supplied by each project. They are not investment advice and not an endorsement of any token. Crypto assets are volatile and you can lose money.</p>
  </div></section>
</main>
{footer('')}
{fab}
<script>window.HOME="index.html"; window.LANG="en";
{common_js}
btcPill();</script>"""
    return page
