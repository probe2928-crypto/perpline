"""Perpline · Guides — long-form English fee guides for search (guides/<slug>.html).
Rules: only fee numbers checked on the exchange's own pages (source link + date in the text),
no Korea/US targeting, no return promises or price calls. Referral links and rebates come from VENUES."""
import json

# footer links (slug, anchor text) — keep in sync with _guides()
LINKS = [("bitget-futures-fees", "Bitget futures fees explained")]

CSS = """
.gd-hero{padding-block:clamp(48px,7vw,96px) clamp(28px,4vw,48px);border-bottom:1px solid var(--hair)}
.gd-hero h1{font-size:clamp(40px,6vw,80px);line-height:1;max-width:18ch;margin:16px 0 18px}
.gd-hero .lede{max-width:58ch}
.gd-meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:22px}
.gd{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:clamp(32px,6vw,88px);padding-block:clamp(40px,6vw,80px)}
@media (max-width:960px){.gd{grid-template-columns:1fr}}
.gd-body{min-width:0;max-width:68ch}
.gd-body h2{font-size:clamp(28px,3.2vw,40px);margin:56px 0 18px;line-height:1.1}
.gd-body h2:first-child{margin-top:0}
.gd-body p,.gd-body li{font-size:18px;font-weight:300;line-height:1.7}
.gd-body p + p{margin-top:16px}
.gd-body a{text-underline-offset:3px}
.gd-body ul{margin:16px 0 0;padding-left:20px}
.gd-body ul li + li{margin-top:8px}
.gd-body .src{font-size:13.5px;color:var(--muted);margin-top:14px}
.gd-tbl{width:100%;border-collapse:collapse;margin:22px 0 6px;font-variant-numeric:tabular-nums}
.gd-tbl th,.gd-tbl td{text-align:left;padding:13px 10px 13px 0;border-bottom:1px solid var(--hair);font-size:15.5px;vertical-align:top}
.gd-tbl th{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:500;border-bottom:1px solid var(--ink)}
.gd-tbl td:last-child,.gd-tbl th:last-child{text-align:right;padding-right:0}
.gd-tbl tr.tot td{font-weight:500}
.gd-tbl tr.tot td:last-child{font-family:var(--display);font-size:22px;color:var(--tone);font-weight:400}
.gd-scroll{overflow-x:auto}
.gd-steps{list-style:none;margin:20px 0 0;padding:0;border-top:1px solid var(--ink);counter-reset:s}
.gd-steps li{display:grid;grid-template-columns:48px minmax(0,1fr);gap:12px;padding-block:18px;border-bottom:1px solid var(--hair);counter-increment:s}
.gd-steps li::before{content:counter(s);font-family:var(--display);font-style:italic;font-size:26px;color:var(--tone);line-height:1.1}
.gd-steps b{font-weight:500;display:block;margin-bottom:2px}
.gd-steps p{font-size:16px!important;color:var(--muted)}
.gd-risk{margin-top:56px;padding:24px;border:1px solid var(--ink)}
.gd-risk h2{margin-top:0!important;font-size:26px!important}
.gd-risk p{font-size:15.5px!important}
.gd-side{align-self:start;position:sticky;top:88px;display:flex;flex-direction:column;gap:18px}
@media (max-width:960px){.gd-side{position:static}}
.gd-card{border-top:1px solid var(--ink);padding-top:18px;display:flex;flex-direction:column;gap:10px}
.gd-card b.big{font-family:var(--display);font-weight:400;font-size:44px;line-height:1;color:var(--tone)}
.gd-card .btn{justify-content:center;text-align:center}
.gd-faq{margin-top:56px}
.gd-top{display:none}
@media (max-width:960px){.gd-top{display:grid;grid-template-columns:minmax(0,1fr);gap:10px;margin-top:22px;padding-top:16px;border-top:1px solid var(--ink)}
.gd-top .row{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
.gd-top b{font-family:var(--display);font-weight:400;font-size:30px;line-height:1;color:var(--tone)}
.gd-top .btn{width:100%;min-height:52px;font-size:15px;letter-spacing:.02em;text-transform:none}}
"""


def _guides(V, pct, net, link, config, tg_dm):
    """Guide data. Each guide is built from the live VENUES entry so the rebate and link never drift."""
    out = []

    # ---- Bitget futures fees ---------------------------------------------------------------
    b = V["bitget"]
    # Verified 2026-11-03 on Bitget's own "Bitget Trading Fees FAQ" (updated 2026-08-20):
    # standard futures 0.02% maker / 0.06% taker, funding exchanged every 8 hours.
    MAKER, TAKER = 0.02, 0.06
    assert (b["maker"], b["taker"]) == (MAKER, TAKER), "Bitget fee in VENUES no longer matches the verified guide numbers"
    r = b["rebate"]
    FAQ_URL = "https://www.bitget.com/support/articles/12560603892734"
    BRK_URL = "https://www.bitget.com/support/articles/12560603825829"
    signup = link(b, "guide-bitget-fees")
    pos = 10000
    t_side, m_side = pos * TAKER / 100, pos * MAKER / 100
    rt_t = t_side * 2                 # market in, market out
    rt_mix = m_side + t_side          # limit in, market out
    n = 20
    mo_t, mo_mix = rt_t * n, rt_mix * n
    back_t, back_mix = mo_t * r / 100, mo_mix * r / 100
    eff_t, eff_m = net(TAKER, r), net(MAKER, r)
    def usd(x): return f"${x:,.2f}"

    body = f"""
<h2>The short version</h2>
<p>On a standard Bitget account, USDT-margined perpetual futures cost <b>{pct(MAKER)} for maker orders and {pct(TAKER)} for taker orders</b>. Those are the rates Bitget lists in its own trading fees FAQ, which we checked on 3 November 2026. Bitget says the rate falls as you climb its VIP levels, which depend on trading volume, assets or BGB holdings.</p>
<p>Most traders who search for "Bitget futures fees" are not VIPs. They pay the standard rate, often as a taker, and the cost adds up faster than the small percentages suggest. This guide shows how the fee is calculated, what a normal month of trading costs in dollars, and how a {r}% fee rebate through {config['brand']} changes that number.</p>
<p class="src">Source: <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a> (Bitget support centre, updated 20 Aug 2026), checked 3 Nov 2026. Your live account rate is shown in Bitget's fee page after you log in and always takes precedence.</p>

<h2>Maker or taker: which one are you paying?</h2>
<p>Every futures fill on Bitget is either a maker or a taker trade. A <b>maker</b> order adds liquidity: a limit order that rests on the order book until someone else trades against it. A <b>taker</b> order removes liquidity: a market order, or a limit order priced so that it fills immediately.</p>
<p>The gap matters. At the standard rate, taking costs three times as much as making ({pct(TAKER)} against {pct(MAKER)}). Stop-losses and most fast exits are taker trades, so even patient traders end up paying the higher rate on part of their volume.</p>

<h2>How the fee is calculated</h2>
<p>Bitget charges the fee on the value of the order, not on your margin. In its <a href="https://www.bitget.com/academy/Fee-Structure-and-Fee-Calculations-on-Bitget" target="_blank" rel="noopener">fee calculation guide</a> the exchange puts it simply: transaction fee equals order value times fee rate. Leverage does not change the rate, but it does change the order value you can open with the same margin, which is why fees feel heavier at high leverage.</p>
<p>Take a {usd(pos)} position. A taker fill costs {usd(pos)} × {pct(TAKER)} = <b>{usd(t_side)}</b>. A maker fill costs {usd(pos)} × {pct(MAKER)} = <b>{usd(m_side)}</b>. You pay once to open and again to close, so a full round trip with market orders on both sides costs {usd(rt_t)}.</p>

<h2>What a month of trading costs, before and after the rebate</h2>
<p>Here are two common patterns, each with twenty {usd(pos)} round trips in a month. The first uses market orders in and out. The second opens with a resting limit order and closes with a market order, which is how many swing traders actually work.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Per month</th><th>Market in, market out</th><th>Limit in, market out</th></tr></thead>
  <tbody>
    <tr><td>Fee per round trip</td><td>{usd(rt_t)}</td><td>{usd(rt_mix)}</td></tr>
    <tr><td>Fees paid to Bitget (20 round trips)</td><td>{usd(mo_t)}</td><td>{usd(mo_mix)}</td></tr>
    <tr><td>{config['brand']} rebate ({r}%)</td><td>+{usd(back_t)}</td><td>+{usd(back_mix)}</td></tr>
    <tr class="tot"><td>Net trading cost</td><td>{usd(mo_t - back_t)}</td><td>{usd(mo_mix - back_mix)}</td></tr>
  </tbody>
</table></div>
<p class="src">Standard rates {pct(MAKER)} / {pct(TAKER)} from Bitget's FAQ, checked 3 Nov 2026. Funding payments and any VIP discount are not included. The example is arithmetic, not a forecast of your trading.</p>
<p>Put another way, the {r}% rebate brings the taker rate you effectively pay from {pct(TAKER)} to <b>{pct(eff_t)}</b>, and the maker rate from {pct(MAKER)} to {pct(eff_m)}. You still pay Bitget's normal fee at the moment you trade. The rebate is paid back to you afterwards by {config['brand']}, in USDT, every Monday.</p>

<h2>Funding is a separate cost</h2>
<p>Perpetual futures also carry funding payments, and they are easy to confuse with trading fees. Bitget's FAQ says funding is exchanged between long and short holders every 8 hours, and its fee breakdown gives the formula as position value times the funding rate. Depending on which side of the market you are on, you either pay or receive it.</p>
<p>Funding goes from trader to trader, not to the exchange, so no rebate applies to it. If you hold positions for days, check the current funding rate and the countdown on the contract page before you open. For a short-term trader, the trading fee is often the bigger and more predictable line on the bill.</p>
<p class="src">Source: <a href="{BRK_URL}" target="_blank" rel="noopener">Understanding Bitget's Fees</a> and the <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, checked 3 Nov 2026.</p>

<h2>Three ways to pay less on Bitget</h2>
<ul>
  <li><b>Use limit orders where you can.</b> Entering with a resting limit order instead of a market order cuts that leg from {pct(TAKER)} to {pct(MAKER)}.</li>
  <li><b>Check your VIP level.</b> Bitget lowers fees as volume, assets or BGB holdings grow. The thresholds change, so read them on Bitget's own fee schedule rather than on third-party lists.</li>
  <li><b>Get part of the fee back.</b> Open your account through a fee-rebate partner and a share of every fee you pay comes back. Through {config['brand']} it is {r}% on Bitget, paid weekly in USDT.</li>
</ul>
<p>Before choosing an exchange on fees alone, compare the rate you would actually pay after rebates. Our <a href="../index.html#venues">exchange ranking</a> lists all eleven venues by taker fee, and the <a href="../index.html#fees">fee calculator</a> lets you enter your own size and number of trades.</p>

<h2>How to sign up and claim the {r}% rebate</h2>
<ol class="gd-steps">
  <li><div><b>Open a new Bitget account through our link</b><p>Use the sign-up button on this page. The referral is attached by the link, so there is no code to type. It only works for a new account.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Set a strong password and two-factor authentication, then complete identity verification if Bitget asks for it in your country.</p></div></li>
  <li><div><b>Copy your UID</b><p>Open your profile in the Bitget app or website. The UID is the account number shown there.</p></div></li>
  <li><div><b>Send "Bitget + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send your password, 2FA codes or API keys.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>The rebate for the previous week arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over to the next week.</p></div></li>
</ol>
<p style="margin-top:20px">There is more on the account itself, including the full list of steps, on our <a href="../exchanges/bitget.html">Bitget referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, quickly, and can wipe out your whole margin. Start with low leverage and only trade money you can afford to lose. A fee rebate lowers your costs; it does not make a losing strategy profitable.</p>
  <p style="margin-top:12px">Bitget decides which countries it serves, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs = [
        ("What are Bitget's futures trading fees?",
         f"On a standard account, Bitget's USDT-margined perpetual futures cost {pct(MAKER)} for maker orders and {pct(TAKER)} for taker orders, according to Bitget's own trading fees FAQ (checked 3 November 2026). VIP levels pay less. The rate shown in your logged-in account always applies."),
        ("How do I get a discount on Bitget futures fees?",
         f"Use limit orders to pay the maker rate, move up Bitget's VIP levels, or open a new account through a fee-rebate partner. Through {config['brand']}, {r}% of the Bitget futures fees you pay comes back in USDT every Monday, which brings the effective taker rate to {pct(eff_t)}."),
        ("Does the rebate cover Bitget funding fees?",
         "No. Funding is exchanged between long and short traders every 8 hours and does not go to the exchange, so there is no commission on it to share. The rebate applies only to the trading fees you pay."),
    ]
    out.append(dict(
        slug="bitget-futures-fees",
        venue=b,
        title=f"Bitget Futures Fees 2026: Maker, Taker & a {r}% Rebate | {config['brand']}",
        h1="Bitget futures fees, <em>explained in dollars.</em>",
        crumb="Bitget futures fees",
        desc=(f"Bitget futures fees are {pct(MAKER)} maker / {pct(TAKER)} taker. What a month of trades really costs, "
              f"how funding differs, and how a {r}% rebate cuts taker to {pct(eff_t)}."),
        lede=(f"The standard rate is {pct(MAKER)} maker and {pct(TAKER)} taker. Here is what that adds up to in a normal month, "
              f"where funding fits in, and how to get {r}% of it back."),
        published="2026-11-03", modified="2026-11-03", checked="3 Nov 2026",
        keyword="bitget futures fees",
        body=body, faqs=faqs, signup=signup,
        side_big=pct(eff_t), side_label=f"Taker you effectively pay after the {r}% rebate (standard {pct(TAKER)})",
    ))
    return out


def build_guides(head, header, footer, esc, common_js, config, fab, venues, pct, net, link, tg_dm):
    """Returns [(slug, page_html)] for every guide; build.py writes guides/<slug>.html."""
    V = {v["slug"]: v for v in venues}
    pages = []
    for g in _guides(V, pct, net, link, config, tg_dm):
        canonical = f"{config['domain']}/guides/{g['slug']}.html"
        h1_plain = g["h1"].replace("<em>", "").replace("</em>", "")
        ld = [
            {"@context": "https://schema.org", "@type": "Article", "headline": h1_plain, "description": g["desc"],
             "datePublished": g["published"], "dateModified": g["modified"], "mainEntityOfPage": canonical,
             "image": f"{config['domain']}/assets/og.png",
             "author": {"@type": "Organization", "name": config["brand"], "url": config["domain"] + "/"},
             "publisher": {"@type": "Organization", "name": config["brand"], "url": config["domain"] + "/"}},
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faqs"]]},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": config["brand"], "item": config["domain"] + "/"},
                {"@type": "ListItem", "position": 2, "name": g["crumb"], "item": canonical}]},
        ]
        ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
        v = g["venue"]
        hd = head(g["title"], g["desc"], canonical, ld_html).replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">', 1)
        page = hd + f"""<style>{CSS}</style><!--BODY-->{header('../')}
<main>
  <div class="wrap"><nav class="crumbs" aria-label="Breadcrumb" style="font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding-block:18px"><a href="../index.html" style="text-decoration:none">{config['brand']}</a> / Guides / {esc(g['crumb'])}</nav></div>
  <section class="gd-hero"><div class="wrap">
    <span class="label">Guide · Fees</span>
    <h1>{g['h1']}</h1>
    <p class="lede">{esc(g['lede'])}</p>
    <div class="gd-top" data-place="guide-top">
      <div class="row"><span class="label">{esc(v['name'])} · {v['rebate']}% rebate</span><b class="num">{esc(g['side_big'])}</b></div>
      <span class="fine">{esc(g['side_label'])}</span>
      <a class="btn" href="{esc(g['signup'])}" target="_blank" rel="sponsored nofollow noopener">Sign up to {esc(v['name'])} · {v['rebate']}% back</a>
    </div>
    <div class="gd-meta"><span class="label">By the {config['brand']} desk</span><span class="label">Fees checked {esc(g['checked'])}</span><span class="label">Not for KR / US residents</span></div>
  </div></section>
  <div class="wrap gd">
    <article class="gd-body">
      {g['body']}
      <section class="gd-faq" aria-labelledby="gdFaq">
        <h2 id="gdFaq">Questions</h2>
        <div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in g['faqs'])}</div>
      </section>
    </article>
    <aside class="gd-side" aria-label="{esc(v['name'])} rebate">
      <div class="gd-card" data-place="guide-side">
        <span class="label">{esc(v['name'])} · {v['rebate']}% rebate</span>
        <b class="big num">{esc(g['side_big'])}</b>
        <span class="fine">{esc(g['side_label'])}</span>
        <a class="btn" href="{esc(g['signup'])}" target="_blank" rel="sponsored nofollow noopener">Sign up to {esc(v['name'])}</a>
        <a class="btn line" href="{tg_dm}" target="_blank" rel="noopener">Send my UID</a>
      </div>
      <div class="gd-card">
        <span class="label">Compare first</span>
        <a href="../index.html#venues">All 11 exchanges ranked by fee</a>
        <a href="../exchanges/{v['slug']}.html">{esc(v['name'])} referral page</a>
      </div>
    </aside>
  </div>
</main>
{footer('../')}
{fab}
<script>window.HOME="../index.html"; window.LANG="en";
{common_js}
btcPill();</script>"""
        pages.append((g["slug"], page, canonical))
    return pages
