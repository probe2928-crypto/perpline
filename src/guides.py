"""Perpline · Guides — long-form English fee guides for search (guides/<slug>.html).
Rules: only fee numbers checked on the exchange's own pages (source link + date in the text),
no Korea/US targeting, no return promises or price calls. Referral links and rebates come from VENUES."""
import json

# footer links (slug, anchor text) — keep in sync with _guides()
LINKS = [("bitget-futures-fees", "Bitget futures fees explained"), ("maker-vs-taker-fees", "Maker vs taker fees in futures"), ("how-funding-fees-work", "How funding fees work"), ("how-fee-rebates-work", "How futures fee rebates work")]

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
.gd-mid{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 20px;margin:40px 0 0;padding:18px 20px;border:1px solid var(--ink)}
.gd-mid .fine{display:block;font-size:13.5px;color:var(--muted);margin-top:4px;max-width:34ch}
.gd-mid .btn{white-space:nowrap}
@media (max-width:560px){.gd-mid .btn{width:100%;text-align:center}}
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

    # ---- Maker vs taker fees (general explainer, Bitget used for the worked numbers) -------------
    # Numbers: Bitget standard futures 0.02% maker / 0.06% taker, verified 2026-11-03 on Bitget's own
    # Trading Fees FAQ (same check as the Bitget guide above). Definitions and the
    # "commission fee = notional value * fee rate" formula read 2026-11-05 on BloFin's help centre.
    ex = V["bitget"]
    assert (ex["maker"], ex["taker"]) == (MAKER, TAKER), "Bitget fee in VENUES no longer matches the verified guide numbers"
    r2 = ex["rebate"]
    BLOFIN_FEE_URL = "https://blofin.zendesk.com/hc/en-us/articles/6228682731151-Trading-Fee"
    signup2 = link(ex, "guide-maker-taker")
    def d(x): return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    margin, lev = 2000, 10
    notional = margin * lev
    f_t, f_m = notional * TAKER / 100, notional * MAKER / 100
    trips = 30
    mixes = [("Market in, market out", f_t + f_t), ("Limit in, market out", f_m + f_t), ("Limit in, limit out", f_m + f_m)]
    rows2 = "".join(
        f"<tr><td>{name}</td><td>{d(rt)}</td><td>{d(rt * trips)}</td><td>+{d(rt * trips * r2 / 100)}</td><td>{d(rt * trips * (1 - r2 / 100))}</td></tr>"
        for name, rt in mixes)
    worst, best = mixes[0][1] * trips, mixes[2][1] * trips
    half = round((MAKER + TAKER) / 2, 4)
    body2 = f"""
<h2>The short version</h2>
<p>Every futures trade you make is charged as either a <b>maker</b> or a <b>taker</b>. Makers add orders to the book and wait. Takers trade against orders that are already there. Almost every exchange charges takers more, often two or three times more, and most retail traders pay the taker rate on far more of their volume than they realise.</p>
<p>This guide explains how an order ends up on one side or the other, how the fee is worked out in dollars, and what a realistic month looks like when you shift part of your trading from taker to maker. We use Bitget's standard USDT-margined futures rates ({pct(MAKER)} maker, {pct(TAKER)} taker, checked on Bitget's own fee FAQ on 3 November 2026) for the worked numbers, because they are typical of the market. The logic is the same on any venue in our <a href="../index.html#venues">exchange ranking</a>.</p>

<h2>What makes an order a maker or a taker</h2>
<p>The label is not about whether you are buying or selling, or long or short. It depends only on what your order does to the order book at the moment it is placed.</p>
<ul>
  <li><b>Taker:</b> an order that fills straight away against resting orders. BloFin's help centre describes it as an order that trades immediately before going on the order book. Market orders are always takers.</li>
  <li><b>Maker:</b> an order that sits on the book, in whole or in part, until someone else fills it. A limit order placed below the current price when buying, or above it when selling, is the usual example.</li>
</ul>
<p>A limit order is not automatically a maker order. If you place a buy limit above the best ask, it crosses the spread and fills at once, so it is charged as a taker. Many exchanges offer a "post-only" option that cancels the order instead of letting it take, which is the simplest way to guarantee the maker rate when you are entering a position.</p>
<p>The trades that quietly push traders onto the taker rate are exits. A stop-loss that triggers a market order is a taker trade. So is closing a position in a hurry, and so is a liquidation. Even a patient trader who enters with limit orders usually pays the taker rate on a good share of exits.</p>
<p class="src">Source: <a href="{BLOFIN_FEE_URL}" target="_blank" rel="noopener">BloFin help centre, "Trading Fee"</a>, read 5 Nov 2026.</p>

<h2>How the fee is calculated</h2>
<p>Futures fees are charged on the full value of the position, not on the margin you put up. BloFin's help centre writes the formula as <i>commission fee = notional value × fee rate</i>, and Bitget's fee guide says the same in different words. Leverage does not change the rate. It changes the notional value you can open with the same margin, which is why fees feel so much heavier at high leverage.</p>
<p>Say you post {d(margin)} of margin at {lev}x. That opens a {d(notional)} position. At Bitget's standard rates:</p>
<ul>
  <li>Opening with a market order costs {d(notional)} × {pct(TAKER)} = <b>{d(f_t)}</b>.</li>
  <li>Opening with a resting limit order costs {d(notional)} × {pct(MAKER)} = <b>{d(f_m)}</b>.</li>
</ul>
<p>You pay again when you close. A round trip with market orders on both sides costs {d(f_t * 2)}, which is {(f_t * 2) / margin * 100:.1f}% of the margin you posted, before the price has moved at all.</p>

<h2>A month of trading: three order habits compared</h2>
<p>Here is the same trader making {trips} round trips of {d(notional)} in a month, with three different habits. The rebate column shows what comes back through {config['brand']}'s {r2}% rebate on Bitget.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Habit</th><th>Per round trip</th><th>Fees for {trips}</th><th>Rebate {r2}%</th><th>Net cost</th></tr></thead>
  <tbody>{rows2}</tbody>
</table></div>
<p class="src">Bitget standard futures rates {pct(MAKER)} / {pct(TAKER)}, from the <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, checked 3 Nov 2026. Funding and VIP discounts are not included. The table is arithmetic, not a forecast of your trading.</p>
<p>The gap between the first and last row is {d(worst - best)} a month on fees alone. Few people can trade only with limit orders, and nobody should skip a stop-loss to save a fee. The realistic target is the middle row: enter with limit orders when you are not in a hurry and accept the taker rate on exits.</p>
<p>A useful way to think about it is your blended rate. If half your volume is maker and half is taker, you pay about {pct(half)} on average at these rates. Every bit of volume you move from taker to maker pulls that number down.</p>

<h2>Where a rebate fits in</h2>
<p>A fee rebate does not change which rate the exchange charges you. You still pay the normal maker or taker fee at the moment you trade. The exchange then pays the referrer a commission on those fees, and a rebate service hands part of it back to you.</p>
<p>Through {config['brand']}, {r2}% of the Bitget futures fees you pay comes back in USDT every Monday. That brings the taker rate you effectively pay from {pct(TAKER)} to <b>{pct(net(TAKER, r2))}</b>, and the maker rate from {pct(MAKER)} to {pct(net(MAKER, r2))}. Because the rebate is a percentage of whatever you paid, it helps most on the taker volume you cannot avoid.</p>
<p>Rebate rates differ by exchange. Our <a href="../index.html#venues">ranking of all eleven exchanges</a> sorts them by the taker fee you pay after the rebate, and the <a href="../index.html#fees">fee calculator</a> lets you plug in your own size and number of trades. If you want the Bitget detail, including funding, our <a href="bitget-futures-fees.html">Bitget futures fees guide</a> goes further.</p>

<h2>Four habits that cut your taker share</h2>
<ul>
  <li><b>Enter with limit or post-only orders</b> when the setup is not time-critical. Waiting a few ticks often costs less than the fee difference.</li>
  <li><b>Use limit take-profits.</b> A take-profit placed in advance rests on the book, so it is usually filled as a maker.</li>
  <li><b>Trade less often, in larger steps.</b> Fees scale with notional value, so ten small scalps cost the same in fees as one position ten times the size, and usually more once you count the extra exits.</li>
  <li><b>Check your account's rate after you log in.</b> Exchanges change fee tiers and run promotions. The rate on your own fee page always takes precedence over any guide, including this one.</li>
</ul>

<h2>How to sign up and claim the {r2}% rebate on Bitget</h2>
<ol class="gd-steps">
  <li><div><b>Open a new Bitget account through our link</b><p>The referral is attached by the sign-up button on this page, so there is no code to type. It works for new accounts only.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity checks if Bitget asks for them where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>It is the account number shown on your profile in the Bitget app or website.</p></div></li>
  <li><div><b>Send "Bitget + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over.</p></div></li>
</ol>
<p style="margin-top:20px">Prefer another venue? Each exchange has its own page with the same steps, starting from the <a href="../index.html#venues">exchange list</a> or our <a href="../exchanges/bitget.html">Bitget referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, very quickly, and can wipe out your whole margin. Lower fees do not make a losing strategy profitable. Start with low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">Each exchange decides which countries it serves, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs2 = [
        ("What is the difference between maker and taker fees?",
         f"A maker order rests on the order book until someone else fills it, so it adds liquidity. A taker order fills immediately against existing orders, so it removes liquidity. Exchanges charge takers more: on a standard Bitget futures account it is {pct(MAKER)} maker against {pct(TAKER)} taker (checked 3 November 2026)."),
        ("Is a limit order always charged the maker fee?",
         "No. A limit order priced through the market, such as a buy limit above the best ask, fills at once and is charged as a taker. Use a post-only option if you want the order cancelled rather than filled as a taker."),
        ("Does a fee rebate apply to both maker and taker fees?",
         f"Yes. The rebate is a share of the trading fees you actually pay, whichever side they come from. Through {config['brand']} on Bitget it is {r2}%, which brings the effective rates to {pct(net(MAKER, r2))} maker and {pct(net(TAKER, r2))} taker. Funding payments are not trading fees and are not rebated."),
    ]
    out.append(dict(
        slug="maker-vs-taker-fees",
        venue=ex,
        title=f"Maker vs Taker Fees in Crypto Futures: What You Really Pay | {config['brand']}",
        h1="Maker vs taker fees, <em>in real dollars.</em>",
        crumb="Maker vs taker fees",
        desc=(f"Maker vs taker fees in crypto futures, with dollar examples: why takers pay up to 3x more, "
              f"how the fee is calculated, and how a {r2}% rebate lowers both."),
        lede=("Most futures traders pay the taker rate far more often than they think. Here is how each order is classified, "
              "what the difference costs in a month, and how to keep more of it."),
        published="2026-11-05", modified="2026-11-05", checked="3 Nov 2026",
        keyword="maker vs taker fees",
        body=body2, faqs=faqs2, signup=signup2,
        side_big=pct(net(TAKER, r2)), side_label=f"Bitget taker you effectively pay after the {r2}% rebate (standard {pct(TAKER)})",
    ))

    # ---- How funding fees work (perpetual futures funding explainer, Bitget used for the worked numbers) ----
    # Facts used: Bitget Trading Fees FAQ (funding exchanged every 8 hours; standard futures 0.02% / 0.06%) and
    # "Understanding Bitget's Fees" (funding = position value x funding rate), both checked 2026-11-03 (same check as above).
    # BloFin help centre "Trading Fee" (commission fee = notional value x fee rate) re-read 2026-11-10.
    # Funding rates in the tables are labelled hypothetical round numbers for arithmetic only, not exchange data.
    fx = V["bitget"]
    assert (fx["maker"], fx["taker"]) == (MAKER, TAKER), "Bitget fee in VENUES no longer matches the verified guide numbers"
    r3 = fx["rebate"]
    signup3 = link(fx, "guide-funding")
    def m(x): return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    pos3 = 10000
    margin3, lev3 = 1000, 10
    per_day = 3  # 8-hour interval
    rates = [0.01, 0.03]
    holds = [("One funding time (8 hours)", 1), ("One day", per_day), ("One week", per_day * 7), ("30 days", per_day * 30)]
    rows3 = "".join(
        f"<tr><td>{h}</td>" + "".join(f"<td>{m(pos3 * fr / 100 * n)}</td>" for fr in rates) + "</tr>"
        for h, n in holds)
    rt3 = pos3 * TAKER / 100 * 2
    rt3_net = rt3 * (1 - r3 / 100)
    wk_fund = pos3 * rates[0] / 100 * per_day * 7
    body3 = f"""
<h2>The short version</h2>
<p>A perpetual futures contract never expires, so exchanges use <b>funding</b> to keep its price close to the spot market. At fixed times, traders on one side of the market pay traders on the other side. When the funding rate is positive, longs pay shorts. When it is negative, shorts pay longs. The exchange sets the rate, but the money moves between traders.</p>
<p>The payment is the value of your position multiplied by the funding rate at that moment. It is charged only if you hold a position when funding is settled, and it is completely separate from the trading fee you pay to open and close. That last point matters for rebates: a fee rebate is a share of your trading fees, so it never covers funding.</p>
<p>This guide walks through the calculation in dollars, shows how funding compares with trading fees over different holding periods, and explains what to check on the contract page before you open a position. Where we need a real exchange, we use Bitget, whose own fee FAQ we checked on 3 November 2026.</p>

<h2>Why perpetual futures need funding</h2>
<p>A quarterly futures contract has an end date. As that date gets closer, its price is pulled toward the spot price, because on expiry the two have to meet. A perpetual has no end date, so nothing pulls it back by itself. If more traders want to be long than short, the perpetual can drift above the spot price and stay there.</p>
<p>Funding fixes that with a small, regular payment. If the perpetual trades above spot, the rate turns positive and longs pay shorts. Holding a long becomes slightly more expensive and holding a short slightly more rewarding, which nudges the two prices back together. When the perpetual trades below spot, the rate turns negative and the payment runs the other way.</p>
<p>Because the rate follows the market, it changes from one funding time to the next. A long that receives funding this week can be paying it next week.</p>

<h2>How the funding payment is calculated</h2>
<p>Bitget's fee breakdown gives the formula as <b>position value × funding rate</b>. Bitget's trading fees FAQ says funding is exchanged between long and short holders every 8 hours, which works out to three funding times a day on contracts with that interval. The contract page shows a countdown to the next one, and that countdown is the number to trust for the specific market you trade.</p>
<p>Like the trading fee, funding is worked out on the full position value, not the margin. Post {m(margin3)} of margin at {lev3}x and you hold a {m(pos3)} position, so funding is calculated on {m(pos3)}. Leverage does not change the rate, but it multiplies what the rate costs you relative to the money you actually put in.</p>
<p>Take that {m(pos3)} long and a funding rate of +0.01%. At the funding time you pay {m(pos3)} × 0.01% = <b>{m(pos3 * 0.01 / 100)}</b>, and that amount goes to traders holding shorts. If the rate had been −0.01%, you would have received {m(pos3 * 0.01 / 100)} instead. If you close the position before the funding time, nothing is charged or paid for that interval.</p>
<p class="src">Sources: <a href="{BRK_URL}" target="_blank" rel="noopener">Understanding Bitget's Fees</a> and the <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, checked 3 Nov 2026. Bitget may use a different interval on some contracts; the countdown on each contract page shows the live schedule.</p>

<h2>What funding adds up to over time</h2>
<p>A single funding payment looks tiny. The cost comes from repetition. The table below shows a {m(pos3)} position held through a run of funding times with an 8-hour interval, at two hypothetical rates. The rates are round numbers picked to make the arithmetic easy to follow. They are not a forecast, and real rates move every interval and can flip sign.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Held for</th><th>Rate +0.01% each time</th><th>Rate +0.03% each time</th></tr></thead>
  <tbody>{rows3}</tbody>
</table></div>
<p class="src">Arithmetic only: {m(pos3)} × hypothetical rate × number of funding times, assuming the rate stays the same, which it rarely does. Three funding times a day reflects the 8-hour interval in Bitget's FAQ (checked 3 Nov 2026).</p>
<p>For comparison, opening and closing that same {m(pos3)} position with market orders at Bitget's standard {pct(TAKER)} taker rate costs {m(rt3)} in trading fees. A trader who is in and out within a few hours mostly pays trading fees. A trader who holds for a week at a steady +0.01% pays {m(wk_fund)} in funding on top, which is already more than the round-trip fee. The longer you hold, the more funding decides your cost.</p>

<h2>Funding is not a trading fee, and no rebate covers it</h2>
<p>This is the point most often misunderstood. A trading fee is charged by the exchange each time an order fills, and the exchange keeps it. Funding is paid from one group of traders to another. The exchange does not earn it, so there is no referral commission on it, and nothing for a rebate service to share.</p>
<p>What a rebate does cover is the trading fee, whichever side of the market you are on. Through {config['brand']}, {r3}% of the Bitget futures fees you pay comes back in USDT every Monday. On the round trip above, that turns {m(rt3)} into {m(rt3_net)}, and brings the taker rate you effectively pay from {pct(TAKER)} to <b>{pct(net(TAKER, r3))}</b>. Funding stays exactly as the exchange calculates it.</p>
<p>So when you compare exchanges, compare trading fees after the rebate, and treat funding as a market cost that depends on the contract and the moment. Our <a href="../index.html#venues">exchange ranking</a> sorts every venue by the taker fee you pay after the rebate. If you want the detail on order types, read <a href="maker-vs-taker-fees.html">maker vs taker fees</a>, and for the full Bitget fee picture see our <a href="bitget-futures-fees.html">Bitget futures fees guide</a>.</p>

<h2>What to check before you open a position</h2>
<ul>
  <li><b>The current funding rate and its sign.</b> It is shown on the contract page next to the price. Positive means longs pay; negative means shorts pay.</li>
  <li><b>The countdown to the next funding time.</b> Opening a long a few minutes before a large positive funding time means paying it almost at once.</li>
  <li><b>How long you plan to hold.</b> For a trade of a few hours, funding is a small line. For a position held for weeks, it can become the biggest cost on the bill.</li>
  <li><b>Unusually large rates.</b> A rate many times higher than normal usually means the market is crowded on one side. That is a sign of risk, not a reason to trade.</li>
</ul>
<p>Receiving funding is not free money. A trader who opens a short only to collect positive funding still carries the full price risk of that short, and one bad move can cost far more than months of funding.</p>

<h2>How to sign up and claim the {r3}% rebate on Bitget</h2>
<ol class="gd-steps">
  <li><div><b>Open a new Bitget account through our link</b><p>The referral is attached by the sign-up button on this page, so there is no code to type. It works for new accounts only.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity checks if Bitget asks for them where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>It is the account number shown on your profile in the Bitget app or website.</p></div></li>
  <li><div><b>Send "Bitget + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your trading fees arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over.</p></div></li>
</ol>
<p style="margin-top:20px">Other venues work the same way. Start from the <a href="../index.html#venues">exchange list</a> or go straight to our <a href="../exchanges/bitget.html">Bitget referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, very quickly, and can wipe out your whole margin. Funding can add to those losses on positions you hold for a long time. Start with low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">Each exchange decides which countries it serves, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs3 = [
        ("How are funding fees calculated in crypto futures?",
         "The payment is your position value multiplied by the funding rate at the funding time, as Bitget's fee breakdown puts it. It is calculated on the full position, leverage included, not on your margin. You pay or receive it only if you hold a position when funding is settled."),
        ("Who pays funding, longs or shorts?",
         "It depends on the sign of the rate. When the funding rate is positive, longs pay shorts. When it is negative, shorts pay longs. The rate changes every interval; Bitget's fee FAQ says funding is exchanged every 8 hours (checked 3 November 2026)."),
        ("Does a fee rebate cover funding fees?",
         f"No. Funding moves between traders and the exchange does not earn it, so there is no commission to share. A rebate covers trading fees only. Through {config['brand']} on Bitget, {r3}% of your trading fees comes back, which brings the effective taker rate from {pct(TAKER)} to {pct(net(TAKER, r3))}."),
    ]
    out.append(dict(
        slug="how-funding-fees-work",
        venue=fx,
        title=f"How Funding Fees Work in Crypto Futures (With Dollar Examples) | {config['brand']}",
        h1="How funding fees work, <em>in plain numbers.</em>",
        crumb="How funding fees work",
        desc=("How funding fees work on perpetual futures: who pays whom, the position value × rate formula, "
              "what funding costs over a day, a week or a month, and why no rebate covers it."),
        lede=("Funding is the cost of holding a perpetual, and it has nothing to do with your trading fee. "
              "Here is how it is calculated, what it adds up to, and what to check before you open."),
        published="2026-11-10", modified="2026-11-10", checked="3 Nov 2026",
        keyword="how funding fees work",
        body=body3, faqs=faqs3, signup=signup3,
        side_big=pct(net(TAKER, r3)), side_label=f"Bitget taker you effectively pay after the {r3}% rebate (funding not included)",
    ))

    # ---- How futures fee rebates work (rebate explainer, Bitget used for the worked numbers) ----------
    # Fee numbers: Bitget standard futures 0.02% maker / 0.06% taker from Bitget's Trading Fees FAQ, checked
    # 2026-11-03 (same check as above). Rebate shares, payout day, minimum and claim steps are Perpline's own
    # terms from VENUES/CONFIG. No exchange commission rates are stated because we have not seen them published.
    rx = V["bitget"]
    assert (rx["maker"], rx["taker"]) == (MAKER, TAKER), "Bitget fee in VENUES no longer matches the verified guide numbers"
    r4 = rx["rebate"]
    signup4 = link(rx, "guide-rebates")
    def k(x): return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    pos4, trips4 = 10000, 40
    rt4_t = pos4 * TAKER / 100 * 2
    rt4_m = pos4 * (MAKER + TAKER) / 100
    mo4_t, mo4_m = rt4_t * trips4, rt4_m * trips4
    back4_t, back4_m = mo4_t * r4 / 100, mo4_m * r4 / 100
    vs = sorted([x for x in V.values()], key=lambda x: (-x["rebate"], x["name"]))
    rows4 = "".join(f'<tr><td><a href="../exchanges/{x["slug"]}.html">{x["name"]}</a></td><td>{x["rebate"]}%</td></tr>' for x in vs)
    lo4, hi4 = min(x["rebate"] for x in vs), max(x["rebate"] for x in vs)
    body4 = f"""
<h2>The short version</h2>
<p>A futures fee rebate is a share of the trading fees you pay, handed back to you after you trade. You open an exchange account through a rebate partner's referral link, you trade as normal at the exchange's normal rate, and the partner returns an agreed percentage of those fees to you on a schedule.</p>
<p>Nothing about the trade itself changes. The exchange charges the same fee on every fill, your orders go to the same order book, and the partner never touches your account. What changes is your cost over a month: if {r4}% of your fees come back, you have effectively paid {100 - r4}% of the listed rate.</p>
<p>This guide explains where the money comes from, works through a month of trading in dollars, and lists what to check before you trust any rebate service, including ours. For the dollar example we use Bitget, whose standard futures fees we checked on its own fee FAQ on 3 November 2026.</p>

<h2>Where the rebate money comes from</h2>
<p>Most large crypto exchanges run referral or affiliate programmes. When someone opens an account through a partner's link, the exchange pays that partner a commission out of the trading fees the new account generates. The exchange is happy to do this because the partner brought it a customer who would otherwise have signed up somewhere else.</p>
<p>A rebate service is simply a partner that passes a large part of that commission back to the trader instead of keeping it. The money is not a bonus, a loan or a promotion with conditions attached to your trading. It is a slice of fees you have already paid, returned to you by the partner, who keeps the rest as its margin.</p>
<p>That is also why the rebate is tied to the account. The referral is recorded when the account is opened through the link, so the partner can only share commission on accounts it referred. At {config['brand']} the rebate applies to new accounts opened through our links.</p>

<h2>What a rebate covers, and what it does not</h2>
<ul>
  <li><b>It covers trading fees.</b> Maker and taker fees on the futures orders you fill, whether you are long or short, winning or losing.</li>
  <li><b>It does not cover funding.</b> Funding on perpetuals moves between traders, not to the exchange, so there is no commission on it to share. Our <a href="how-funding-fees-work.html">funding fees guide</a> explains the difference in detail.</li>
  <li><b>It does not lower the fee at the moment you trade.</b> You still pay the full rate on each fill. The saving arrives afterwards, when the rebate is paid.</li>
  <li><b>It does not change your trading results.</b> A rebate trims costs. It cannot turn a losing strategy into a winning one, and it is no reason to trade more than you would anyway.</li>
</ul>

<h2>A month of trading, before and after the rebate</h2>
<p>Bitget's trading fees FAQ lists standard USDT-margined futures at <b>{pct(MAKER)} maker and {pct(TAKER)} taker</b>, charged on the value of the order rather than your margin. Here is a trader who opens and closes a {k(pos4)} position {trips4} times in a month, compared in two styles: market orders on both sides, and a resting limit order to enter with a market order to exit.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Per month</th><th>Market in, market out</th><th>Limit in, market out</th></tr></thead>
  <tbody>
    <tr><td>Fee per round trip</td><td>{k(rt4_t)}</td><td>{k(rt4_m)}</td></tr>
    <tr><td>Fees paid to Bitget ({trips4} round trips)</td><td>{k(mo4_t)}</td><td>{k(mo4_m)}</td></tr>
    <tr><td>{config['brand']} rebate ({r4}%)</td><td>+{k(back4_t)}</td><td>+{k(back4_m)}</td></tr>
    <tr class="tot"><td>Net trading cost</td><td>{k(mo4_t - back4_t)}</td><td>{k(mo4_m - back4_m)}</td></tr>
  </tbody>
</table></div>
<p class="src">Source: <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, standard rates checked 3 Nov 2026. Funding and VIP discounts are left out. The figures are arithmetic on an example, not a forecast of anyone's trading.</p>
<p>Two things stand out. First, the order type matters before any rebate does: entering with a limit order already saves {k(mo4_t - mo4_m)} a month here. Second, the rebate scales with whatever you pay. It is a percentage of the fees actually charged, so if you reach a cheaper VIP tier or use more maker orders, the rebate shrinks in dollars but your total cost still falls. The two kinds of saving stack rather than compete. Our guide to <a href="maker-vs-taker-fees.html">maker vs taker fees</a> covers the order-type side.</p>

<h2>How rebate shares compare across exchanges</h2>
<p>The share that comes back differs by exchange, because each exchange pays its partners differently. Through {config['brand']} it currently ranges from {lo4}% to {hi4}%:</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Exchange</th><th>Rebate on futures fees</th></tr></thead>
  <tbody>{rows4}</tbody>
</table></div>
<p>A bigger percentage is not automatically the better deal. What you actually pay is the exchange's fee multiplied by what is left after the rebate, so a venue with a higher base fee and a higher rebate can end up costing the same as a cheaper venue with a smaller one. Our <a href="../index.html#venues">exchange ranking</a> does that multiplication for every venue, and the <a href="../index.html#fees">fee calculator</a> lets you plug in your own size and number of trades. Liquidity, the markets listed and whether the exchange serves your country matter as much as the fee.</p>

<h2>What to check before you trust a rebate service</h2>
<ul>
  <li><b>It should never ask for your password, 2FA codes or API keys.</b> A rebate only needs your account's UID, which is a public account number. Anyone asking for more access does not need it for a rebate.</li>
  <li><b>The payout terms should be written down.</b> When you get paid, in which currency, and whether there is a minimum. Ours: every Monday, in USDT, with a 10 USDT minimum; smaller amounts roll over to the next week.</li>
  <li><b>The rates should be published per exchange.</b> You should be able to see the percentage before you sign up, not after.</li>
  <li><b>It should be clear what the partner earns.</b> A rebate service is paid by the exchange's referral commission. If that is not explained, ask.</li>
  <li><b>The fee numbers should be sourced.</b> Base fees change. A good guide links to the exchange's own fee page and says when it was checked.</li>
</ul>

<h2>How to sign up and claim a rebate with {config['brand']}</h2>
<ol class="gd-steps">
  <li><div><b>Pick an exchange and open a new account through our link</b><p>The referral is attached by the link, so for Bitget there is no code to type. It only works for a new account.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity checks if the exchange asks for them where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>It is the account number on your profile page in the exchange's app or website.</p></div></li>
  <li><div><b>Send "exchange name + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your trading fees arrives in USDT.</p></div></li>
</ol>
<p style="margin-top:20px">Each exchange has its own page with the referral link and its specific steps, for example our <a href="../exchanges/bitget.html">Bitget referral page</a>. For the full Bitget fee picture, read <a href="bitget-futures-fees.html">Bitget futures fees explained</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, very quickly, and can wipe out your whole margin. A rebate lowers your trading costs; it does not reduce that risk. Start with low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">Each exchange decides which countries it serves, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs4 = [
        ("What is a futures trading fee rebate?",
         f"It is a share of the trading fees you pay that is returned to you after you trade. You open an exchange account through a rebate partner's referral link, pay the normal fee on every order, and the partner sends back an agreed percentage. Through {config['brand']} that is {lo4}% to {hi4}% depending on the exchange, paid in USDT every Monday."),
        ("Is a fee rebate safe? Do I have to share my account?",
         "A rebate only needs your account UID, which is a public account number. You keep full control of the account, and a genuine rebate service never asks for your password, 2FA codes or API keys. The usual risks of leveraged trading still apply in full."),
        ("Does a rebate change the fee I pay on each trade?",
         f"No. The exchange charges its normal rate on every fill. The rebate is paid afterwards, so your effective cost falls. On Bitget's standard {pct(TAKER)} taker rate, a {r4}% rebate means you effectively pay {pct(net(TAKER, r4))}. Funding payments are not covered."),
    ]
    out.append(dict(
        slug="how-fee-rebates-work",
        venue=rx,
        title=f"How Crypto Futures Fee Rebates Work (Dollar Example) | {config['brand']}",
        h1="How futures fee rebates work, <em>and who pays for them.</em>",
        crumb="How fee rebates work",
        desc=(f"How crypto futures fee rebates work: where the money comes from, what they cover, a month of trades "
              f"before and after a {r4}% rebate, and what to check before you trust a rebate service."),
        lede=("A rebate is part of your trading fee, paid back to you after you trade. Here is where that money comes from, "
              "what it does and does not cover, and what it adds up to in a normal month."),
        published="2026-11-12", modified="2026-11-12", checked="3 Nov 2026",
        keyword="trading fee rebate",
        body=body4, faqs=faqs4, signup=signup4,
        side_big=pct(net(TAKER, r4)), side_label=f"Bitget taker you effectively pay after the {r4}% rebate (standard {pct(TAKER)})",
    ))

    return out


def _with_mid_cta(body, g, v, esc):
    """E3: one compact sign-up card before the 3rd <h2>, so long guides have a button between the top and the bottom steps."""
    parts = body.split("<h2")
    if len(parts) < 4:
        return body
    card = (f'<div class="gd-mid" data-place="guide-mid"><div><span class="label">{esc(v["name"])} · {v["rebate"]}% rebate</span>'
            f'<span class="fine">{esc(g["side_label"])}</span></div>'
            f'<a class="btn" href="{esc(g["signup"])}" target="_blank" rel="sponsored nofollow noopener">Sign up to {esc(v["name"])} · {v["rebate"]}% back</a></div>')
    return "<h2".join(parts[:3]) + card + "<h2" + "<h2".join(parts[3:])


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
             "image": f"{config['domain']}/assets/og/{g['slug']}.png",
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
        hd = hd.replace(f"{config['domain']}/assets/og.png", f"{config['domain']}/assets/og/{g['slug']}.png")
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
      {_with_mid_cta(g['body'], g, v, esc)}
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
