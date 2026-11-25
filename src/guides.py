"""Perpline · Guides — long-form English fee guides for search (guides/<slug>.html).
Rules: only fee numbers checked on the exchange's own pages (source link + date in the text),
no Korea/US targeting, no return promises or price calls. Referral links and rebates come from VENUES."""
import json

# footer links (slug, anchor text) — keep in sync with _guides()
LINKS = [("bitget-futures-fees", "Bitget futures fees explained"), ("maker-vs-taker-fees", "Maker vs taker fees in futures"), ("how-funding-fees-work", "How funding fees work"), ("how-fee-rebates-work", "How futures fee rebates work"), ("futures-break-even-price", "Futures break-even price after fees"), ("crypto-scalping-fees", "Crypto scalping fees per trade"), ("bitget-uid", "How to find your Bitget UID"), ("okx-futures-fees", "OKX futures fees explained"), ("okx-vs-bitget-futures-fees", "OKX vs Bitget futures fees"), ("okx-uid", "How to find your OKX UID"), ("bingx-futures-fees", "BingX futures fees explained")]

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

<h2>Bitget spot fees vs futures fees</h2>
<p>If you searched for "Bitget trading fees", you may have seen two different numbers. They belong to two different products. Bitget's own fee FAQ lists a standard <b>spot</b> fee of 0.1% for both makers and takers, and a standard <b>futures</b> fee of {pct(MAKER)} maker and {pct(TAKER)} taker.</p>
<div class="tbl"><table>
  <thead><tr><th></th><th>Maker</th><th>Taker</th></tr></thead>
  <tbody>
    <tr><td>Spot (standard)</td><td>0.1%</td><td>0.1%</td></tr>
    <tr><td>USDT-M futures (standard)</td><td>{pct(MAKER)}</td><td>{pct(TAKER)}</td></tr>
  </tbody>
</table></div>
<p class="src">From Bitget's trading fees FAQ (<a href="{FAQ_URL}" rel="nofollow noopener" target="_blank">bitget.com</a>), checked 23 Nov 2026. VIP levels can lower both, and any BGB discount is listed on Bitget's live fee schedule. The rate shown in your account applies.</p>
<p>The futures percentage looks smaller, but it is charged on the full position value, leverage included. A 10x position on $1,000 of margin pays fees on $10,000. That is why the monthly table above matters more than the headline rate. The {config['brand']} rebate covers futures trading fees only; it does not apply to spot trades.</p>

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
        title=f"Bitget Trading Fees 2026: Futures, Spot & a {r}% Rebate | {config['brand']}",
        h1="Bitget futures fees, <em>explained in dollars.</em>",
        crumb="Bitget futures fees",
        desc=(f"Bitget fees: futures {pct(MAKER)} maker / {pct(TAKER)} taker, spot 0.1%. What a month of trades really costs, "
              f"how funding differs, and how a {r}% rebate cuts futures taker to {pct(eff_t)}."),
        lede=(f"The standard rate is {pct(MAKER)} maker and {pct(TAKER)} taker. Here is what that adds up to in a normal month, "
              f"where funding fits in, and how to get {r}% of it back."),
        published="2026-11-03", modified="2026-11-23", checked="23 Nov 2026",
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

    # ---- Break-even price after fees (Bitget standard rates for the worked numbers) -------------------
    # Fee numbers: Bitget standard futures 0.02% maker / 0.06% taker from Bitget's Trading Fees FAQ, checked
    # 2026-11-03 (same check as above). "fee = order value x fee rate" from Bitget's fee calculation guide and
    # BloFin's help centre (read 2026-11-05). Funding every 8 hours from the same Bitget FAQ. Everything else is
    # arithmetic. The $70,000 entry is an illustrative round number, not a price call.
    bx = V["bitget"]
    assert (bx["maker"], bx["taker"]) == (MAKER, TAKER), "Bitget fee in VENUES no longer matches the verified guide numbers"
    r5 = bx["rebate"]
    signup5 = link(bx, "guide-break-even")
    entry, size5 = 70000, 10000
    def be_long(fi, fo): return entry * (1 + fi / 100) / (1 - fo / 100)
    def be_short(fi, fo): return entry * (1 - fi / 100) / (1 + fo / 100)
    def mv(x): return abs(x - entry) / entry * 100
    def p2(x): return f"${x:,.2f}"
    def pm(x): return f"{x:.3f}".rstrip("0").rstrip(".") + "%"
    eT, eM = net(TAKER, r5), net(MAKER, r5)
    cases = [("Market in, market out", TAKER, TAKER, eT, eT),
             ("Limit in, market out", MAKER, TAKER, eM, eT),
             ("Limit in, limit out", MAKER, MAKER, eM, eM)]
    rows5 = "".join(
        f"<tr><td>{nm}</td><td>{p2(be_long(a, b_))}</td><td>{pm(mv(be_long(a, b_)))}</td><td>{pm(mv(be_long(c, d_)))}</td></tr>"
        for nm, a, b_, c, d_ in cases)
    bl_tt, bs_tt = be_long(TAKER, TAKER), be_short(TAKER, TAKER)
    rt5 = size5 * TAKER / 100 * 2
    levs = [5, 10, 20, 50]
    rows5b = "".join(f"<tr><td>{L}x</td><td>${size5 / L:,.0f}</td><td>{p2(rt5)}</td><td>{rt5 / (size5 / L) * 100:.1f}%</td></tr>" for L in levs)
    fund_ill = 0.01
    body5 = f"""
<h2>The short version</h2>
<p>Your break-even price is the exit price at which a futures trade ends at exactly zero after fees. It is never your entry price. You pay a fee to open and another to close, so the market has to move in your favour by at least the cost of both before the trade starts to make money.</p>
<p>On Bitget's standard futures rates ({pct(MAKER)} maker, {pct(TAKER)} taker, checked on Bitget's own fee FAQ on 3 November 2026), a long opened and closed with market orders needs the price to rise about <b>{pm(mv(bl_tt))}</b> just to cover fees. That sounds tiny. For a scalper aiming at a few tenths of a percent, it can be a third of the target or more. This guide shows the formula, works it through in dollars, and shows how order type, leverage, funding and a fee rebate each move the number.</p>
<p class="src">Fee rates: <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, checked 3 Nov 2026. Your logged-in fee page always takes precedence over any guide.</p>

<h2>The formula, without the jargon</h2>
<p>Futures fees are charged on the value of the order, not on your margin. Bitget's <a href="https://www.bitget.com/academy/Fee-Structure-and-Fee-Calculations-on-Bitget" target="_blank" rel="noopener">fee calculation guide</a> puts it as order value times fee rate, and <a href="{BLOFIN_FEE_URL}" target="_blank" rel="noopener">BloFin's help centre</a> writes the same thing as notional value times fee rate. The closing fee is charged on the value at the exit price, which is why the break-even price is slightly more than entry plus two fees.</p>
<p>For a long position, with an opening fee rate <i>f<sub>open</sub></i> and a closing fee rate <i>f<sub>close</sub></i>:</p>
<p><b>Break-even = entry × (1 + f<sub>open</sub>) ÷ (1 − f<sub>close</sub>)</b></p>
<p>For a short, the signs flip: <b>entry × (1 − f<sub>open</sub>) ÷ (1 + f<sub>close</sub>)</b>. A quick mental shortcut is that the price has to move by roughly the two fee rates added together. With market orders on Bitget that is {pct(TAKER)} + {pct(TAKER)}, or about 0.12%.</p>

<h2>A worked example in dollars</h2>
<p>Take an illustrative entry price of {p2(entry)} for BTC and a {d(size5)} position. This is a round number for the arithmetic, not a view on where the price is heading.</p>
<ul>
  <li><b>Long, market in and market out:</b> break-even is {p2(bl_tt)}, a move of {p2(bl_tt - entry)} above entry.</li>
  <li><b>Short, market in and market out:</b> break-even is {p2(bs_tt)}, a move of {p2(entry - bs_tt)} below entry.</li>
</ul>
<p>In fee terms, that position costs about {d(size5 * TAKER / 100)} to open and a little more than that to close, around {p2(rt5)} in total. Every dollar of price movement before break-even is just paying the exchange.</p>

<h2>How order type changes your break-even</h2>
<p>Because the formula uses the fee rate on each leg, the cheapest way to lower your break-even is to pay the maker rate on one or both sides. The table shows a long from {p2(entry)} on Bitget's standard rates, then the same trade with {config['brand']}'s {r5}% rebate counted in.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Order habit (long)</th><th>Break-even price</th><th>Move needed</th><th>Move needed after {r5}% rebate</th></tr></thead>
  <tbody>{rows5}</tbody>
</table></div>
<p class="src">Bitget standard futures rates {pct(MAKER)} / {pct(TAKER)}, checked 3 Nov 2026. Funding and VIP discounts not included. Arithmetic only, not a forecast.</p>
<p>The rebate column is an effective figure. On the day you trade, Bitget charges its normal fee and your exchange screen shows the normal numbers. The rebate comes back afterwards, in USDT every Monday, so over a month your real break-even sits at the lower figure. For a trader who closes a lot of positions at small gains, that difference adds up.</p>
<p>A limit order only gets the maker rate if it rests on the book. A buy limit placed above the best ask fills at once and is charged as a taker. Our <a href="maker-vs-taker-fees.html">maker vs taker guide</a> covers this in more detail.</p>

<h2>Leverage does not move the price, but it moves the pain</h2>
<p>Leverage does not change the fee rate or the percentage move you need to break even. It changes how large that cost is compared with the margin you put up. Here is the same {d(size5)} market-in, market-out round trip at different leverage settings.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Leverage</th><th>Margin posted</th><th>Round-trip fees</th><th>Fees as % of margin</th></tr></thead>
  <tbody>{rows5b}</tbody>
</table></div>
<p>At 50x, fees alone take a noticeable bite out of your margin on every round trip, before the market has done anything. High leverage also puts your liquidation price much closer to entry, and each exchange sets its own margin rules for that. Fees are one more reason to treat high leverage with care, not a reason to use it.</p>

<h2>Funding moves it too, if you hold</h2>
<p>Perpetual futures carry funding payments between longs and shorts. Bitget's fee FAQ says funding is exchanged every 8 hours, and the payment is position value times the funding rate. If you hold through a funding time while your side is paying, your break-even moves against you by about that rate. As an illustration only, a funding rate of {pm(fund_ill)} on the {d(size5)} position would cost {p2(size5 * fund_ill / 100)} per settlement. When your side is receiving, it moves in your favour.</p>
<p>Funding goes from trader to trader, not to the exchange, so no rebate covers it. Our guide on <a href="how-funding-fees-work.html">how funding fees work</a> explains how to read the rate and countdown before you open.</p>

<h2>Four ways to bring your break-even closer</h2>
<ul>
  <li><b>Enter with a limit or post-only order</b> when the trade is not urgent. On Bitget's standard rates that cuts the opening leg from {pct(TAKER)} to {pct(MAKER)}.</li>
  <li><b>Set take-profits as limit orders.</b> A resting take-profit is usually filled as a maker. Keep stop-losses as they are: protection matters more than the fee.</li>
  <li><b>Trade fewer, more deliberate positions.</b> Each round trip resets the break-even hurdle. Many small scalps pay it many times.</li>
  <li><b>Get part of every fee back.</b> A rebate lowers the effective rate on every leg you cannot avoid paying as a taker. Through {config['brand']}, {r5}% of Bitget futures fees comes back, which brings the taker rate you effectively pay to {pct(eT)}. Compare all venues in our <a href="../index.html#venues">exchange ranking</a> or put your own numbers into the <a href="../index.html#fees">fee calculator</a>.</li>
</ul>

<h2>How to sign up and claim the {r5}% rebate on Bitget</h2>
<ol class="gd-steps">
  <li><div><b>Open a new Bitget account through our link</b><p>Use the sign-up button on this page. The referral is attached by the link, so there is no code to type. It works for new accounts only.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity checks if Bitget asks for them where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>It is the account number on your profile in the Bitget app or website.</p></div></li>
  <li><div><b>Send "Bitget + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your trading fees arrives in USDT.</p></div></li>
</ol>
<p style="margin-top:20px">The full Bitget picture is in <a href="bitget-futures-fees.html">Bitget futures fees explained</a>, and the account steps are on our <a href="../exchanges/bitget.html">Bitget referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, very quickly, and can wipe out your whole margin. Knowing your break-even price does not make a trade safe, and a rebate lowers costs without lowering that risk. Use low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">Each exchange decides which countries it serves, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs5 = [
        ("How do I calculate the break-even price on a futures trade?",
         "For a long, break-even = entry × (1 + opening fee rate) ÷ (1 − closing fee rate). For a short, it is entry × (1 − opening fee rate) ÷ (1 + closing fee rate). As a shortcut, the price has to move by roughly the two fee rates added together before the trade covers its fees."),
        ("Does leverage change my break-even price?",
         "No. Fees are charged on the position's value, so the percentage move you need is the same at 2x or 50x. What leverage changes is how large those fees are compared with your margin, and how close your liquidation price is to entry."),
        ("Does a fee rebate lower my break-even price?",
         f"Not on the exchange screen, because the exchange still charges its normal fee when you trade. It lowers your effective break-even over time, because part of each fee comes back later. With a {r5}% rebate on Bitget's standard {pct(TAKER)} taker rate, you effectively pay {pct(eT)} per leg. Funding payments are not covered."),
    ]
    out.append(dict(
        slug="futures-break-even-price",
        venue=bx,
        title=f"Futures Break-Even Price After Fees: Formula & Examples | {config['brand']}",
        h1="Your futures break-even price, <em>after fees.</em>",
        crumb="Futures break-even price",
        desc=(f"How to calculate the break-even price on crypto futures after maker and taker fees, with dollar examples, "
              f"leverage, funding, and how a {r5}% rebate lowers the move you need."),
        lede=("Fees mean a trade has to move before it makes a cent. Here is the formula, a worked example in dollars, "
              "and what order type, leverage, funding and a rebate do to the number."),
        published="2026-11-14", modified="2026-11-14", checked="3 Nov 2026",
        keyword="futures break even price",
        body=body5, faqs=faqs5, signup=signup5,
        side_big=pm(mv(be_long(eT, eT))), side_label=f"Bitget market-in, market-out break-even move after the {r5}% rebate (standard {pm(mv(bl_tt))})",
    ))

    # ---- Crypto scalping fees (fee drag on many small trades, Bitget standard rates for the worked numbers) ----
    # Fee numbers: Bitget standard futures 0.02% maker / 0.06% taker from Bitget's Trading Fees FAQ, checked
    # 2026-11-03 (same check as above). "fee = order value x fee rate" from Bitget's fee calculation guide and
    # BloFin's help centre (read 2026-11-05). Funding every 8 hours from the same Bitget FAQ. Target moves,
    # position size and trade counts are illustrative round numbers, not a strategy or a forecast.
    sx = V["bitget"]
    assert (sx["maker"], sx["taker"]) == (MAKER, TAKER), "Bitget fee in VENUES no longer matches the verified guide numbers"
    r6 = sx["rebate"]
    signup6 = link(sx, "guide-scalping")
    def s6(x): return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    def pp(x): return f"{x:.3f}".rstrip("0").rstrip(".") + "%"
    habits6 = [("Market in, market out", TAKER + TAKER), ("Limit in, market out", MAKER + TAKER), ("Limit in, limit out", MAKER + MAKER)]
    targets6 = [0.2, 0.3, 0.5, 1.0]
    rows6a = "".join(
        f"<tr><td>{pp(t)}</td>" + "".join(f"<td>{rt / t * 100:.0f}%</td>" for _, rt in habits6) + "</tr>"
        for t in targets6)
    size6, per_day6, days6 = 5000, 15, 20
    trips6 = per_day6 * days6
    vol6 = size6 * 2 * trips6
    rows6b = "".join(
        f"<tr><td>{name}</td><td>{s6(size6 * rt / 100)}</td><td>{s6(size6 * rt / 100 * trips6)}</td>"
        f"<td>+{s6(size6 * rt / 100 * trips6 * r6 / 100)}</td><td>{s6(size6 * rt / 100 * trips6 * (1 - r6 / 100))}</td></tr>"
        for name, rt in habits6)
    rt_tt6 = TAKER * 2
    rt_tt6_net = net(TAKER, r6) * 2
    t_ex6 = 0.3
    month_tt6 = size6 * rt_tt6 / 100 * trips6
    body6 = f"""
<h2>The short version</h2>
<p>Scalping means taking many small trades and aiming for small price moves on each one. That style has one cost that grows faster than any other: trading fees. The fee rate per trade is the same whether you hold for thirty seconds or three days, so the more often you open and close, the more of your gross result goes to the exchange.</p>
<p>This guide puts numbers on that. It shows how much of a small target move the fees take, what a month of scalping costs in dollars, how the order type you use changes the bill, and where a fee rebate fits. We use Bitget's standard USDT-margined futures rates ({pct(MAKER)} maker, {pct(TAKER)} taker), which we checked on Bitget's own fee FAQ on 3 November 2026. The arithmetic works the same way on any exchange in our <a href="../index.html#venues">fee ranking</a>.</p>
<p class="src">Source: <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, checked 3 Nov 2026. Your logged-in fee rate always takes precedence over any guide.</p>

<h2>Why fees hit scalpers harder</h2>
<p>Futures fees are charged on the full value of each order. Bitget's <a href="https://www.bitget.com/academy/Fee-Structure-and-Fee-Calculations-on-Bitget" target="_blank" rel="noopener">fee calculation guide</a> puts it as order value times fee rate, and BloFin's help centre uses the same formula. You pay once to open and once to close, so the cost of a round trip is the two rates added together.</p>
<p>On Bitget's standard rates, a round trip with market orders on both sides costs {pp(rt_tt6)} of the position value. That sounds tiny. But a scalper is not aiming for 10% moves. If your target on a trade is a {pp(t_ex6)} move in your favour, fees of {pp(rt_tt6)} take roughly <b>{rt_tt6 / t_ex6 * 100:.0f}% of that target</b> before anything else happens. A swing trader aiming for 5% barely notices the same fee. A scalper feels it on every trade.</p>
<p>The table shows how much of a winning trade's target move goes to fees, for three order habits. The smaller the target, the bigger the share.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Target move</th><th>Market in, market out ({pp(habits6[0][1])})</th><th>Limit in, market out ({pp(habits6[1][1])})</th><th>Limit in, limit out ({pp(habits6[2][1])})</th></tr></thead>
  <tbody>{rows6a}</tbody>
</table></div>
<p class="src">Share of the target move taken by round-trip fees at Bitget's standard {pct(MAKER)} / {pct(TAKER)} rates (checked 3 Nov 2026). Approximate, because the closing fee is charged on the closing value. Target moves are illustrative, not a strategy.</p>
<p>Losing trades are worse still. A stopped-out scalp loses the price move and pays both fees on top. Fees never cancel out between winners and losers; every trade adds to them.</p>

<h2>A month of scalping, in dollars</h2>
<p>Take a trader who opens a {s6(size6)} position (margin times leverage) {per_day6} times a day and trades {days6} days a month. That is {trips6} round trips and about {s6(vol6)} of traded volume, counting both the open and the close. Here is what the fees come to with each habit, and what comes back through {config['brand']}'s {r6}% rebate on Bitget.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Habit</th><th>Per round trip</th><th>Fees for {trips6}</th><th>Rebate {r6}%</th><th>Net cost</th></tr></thead>
  <tbody>{rows6b}</tbody>
</table></div>
<p class="src">Bitget standard futures rates {pct(MAKER)} / {pct(TAKER)}, from the <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, checked 3 Nov 2026. Funding and VIP discounts are not included. Arithmetic only, not a forecast of anyone's trading.</p>
<p>Leverage does not change these numbers. Fees follow the position value, so a {s6(size6)} position costs the same whether you back it with $500 at 10x or $2,500 at 2x. What leverage changes is how big the fees look next to your margin. Our <a href="futures-break-even-price.html">break-even guide</a> works through that, and the <a href="../tools/futures-fee-calculator.html">fee calculator</a> lets you enter your own size and trade count.</p>

<h2>The order type matters more than the exchange</h2>
<p>At these rates, a taker fill costs three times a maker fill. For someone who trades {per_day6} times a day, moving entries from market orders to resting limit orders cuts the monthly bill by a third in the example above, before any rebate. A few habits help:</p>
<ul>
  <li><b>Use post-only orders for entries.</b> A post-only order is cancelled rather than filled as a taker, so you only ever pay the maker rate on it. A plain limit order priced through the market still fills as a taker.</li>
  <li><b>Place take-profits in advance.</b> A take-profit resting on the book is usually filled as a maker.</li>
  <li><b>Accept the taker rate on stops.</b> Stop-losses that trigger market orders are taker trades, and skipping a stop to save a fee is a bad trade. Plan for that cost rather than avoiding it.</li>
  <li><b>Count your trades.</b> Many scalpers find that a handful of impulsive re-entries each day make up a large part of their fee bill. Fewer, better trades cost less.</li>
</ul>
<p>Our <a href="maker-vs-taker-fees.html">maker vs taker guide</a> explains how an order ends up on each side in more detail.</p>

<h2>Funding usually matters less, but check it</h2>
<p>Perpetual futures also carry funding payments. Bitget's FAQ says funding is exchanged between long and short holders every 8 hours, and it is charged only on positions that are open when funding is settled. A scalper who is flat at those times often pays little or none. If a trade runs over a funding time, though, the payment is worked out on the full position value, like the fee. Check the countdown on the contract page before you hold through it. The <a href="how-funding-fees-work.html">funding guide</a> has the details.</p>

<h2>Where a fee rebate fits</h2>
<p>A rebate does not change what the exchange charges when you trade. It returns part of the fee afterwards. Because it is a percentage of whatever you paid, it is worth most to the people who pay the most fees, and that is usually scalpers.</p>
<p>Through {config['brand']}, {r6}% of the Bitget futures fees you pay comes back in USDT every Monday. That brings the taker rate you effectively pay from {pct(TAKER)} to <b>{pct(net(TAKER, r6))}</b>, and a market-in, market-out round trip from {pp(rt_tt6)} to {pp(rt_tt6_net)}. On the {pp(t_ex6)} target above, the fee share drops from about {rt_tt6 / t_ex6 * 100:.0f}% to about {rt_tt6_net / t_ex6 * 100:.0f}%. In the monthly example, the market-order habit returns {s6(month_tt6 * r6 / 100)} of the {s6(month_tt6)} paid.</p>
<p>If you are choosing a venue for frequent trading, compare the taker rate left after the rebate, not the headline rate alone. Our <a href="../index.html#venues">exchange ranking</a> sorts all eleven venues that way. Fees are not the only thing that matters for scalping, so also look at how liquid the markets you trade are, and read each exchange's own fee schedule for VIP tiers.</p>

<h2>How to sign up and claim the {r6}% rebate on Bitget</h2>
<ol class="gd-steps">
  <li><div><b>Open a new Bitget account through our link</b><p>The referral is attached by the sign-up button on this page, so there is no code to type. It works for new accounts only.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity checks if Bitget asks for them where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>It is the account number shown on your profile in the Bitget app or website.</p></div></li>
  <li><div><b>Send "Bitget + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your trading fees arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over.</p></div></li>
</ol>
<p style="margin-top:20px">The full fee picture for this exchange is in <a href="bitget-futures-fees.html">Bitget futures fees explained</a>, and the account steps are on our <a href="../exchanges/bitget.html">Bitget referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Scalping leveraged futures is fast and unforgiving. Losses can add up quickly and can wipe out your whole margin, and lower fees do not make a losing approach profitable. Use low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">Each exchange decides which countries it serves, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs6 = [
        ("How much do fees cost when scalping crypto futures?",
         f"Each round trip costs the opening plus the closing fee rate on the position value. On Bitget's standard rates ({pct(MAKER)} maker, {pct(TAKER)} taker, checked 3 November 2026), that is {pp(rt_tt6)} with market orders both ways and {pp(MAKER * 2)} with limit orders both ways. On a {pp(t_ex6)} target move, market-order fees take roughly {rt_tt6 / t_ex6 * 100:.0f}% of the gain."),
        ("How can scalpers lower their trading fees?",
         f"Enter with post-only limit orders so you pay the maker rate, rest take-profits on the book, cut unnecessary trades, and open your account through a fee-rebate partner. Through {config['brand']}, {r6}% of Bitget futures fees comes back in USDT every Monday, which brings the effective taker rate to {pct(net(TAKER, r6))}."),
        ("Does leverage increase my scalping fees?",
         "Not the rate. Fees are charged on the position value, so the same position size costs the same at any leverage. Higher leverage lets you open a bigger position with the same margin, and the fee on that bigger position is larger compared with your margin."),
    ]
    out.append(dict(
        slug="crypto-scalping-fees",
        venue=sx,
        title=f"Crypto Scalping Fees: What Futures Fees Cost Per Trade | {config['brand']}",
        h1="Scalping crypto futures: <em>what the fees take.</em>",
        crumb="Crypto scalping fees",
        desc=(f"How trading fees eat into crypto futures scalping: share of each target move, a month of trades in dollars, "
              f"maker vs taker habits, and how a {r6}% rebate cuts the bill."),
        lede=("When each trade aims for a small move, fees decide a lot. Here is how much they take per trade and per month, "
              "and what order type, funding and a rebate change."),
        published="2026-11-17", modified="2026-11-17", checked="3 Nov 2026",
        keyword="crypto scalping fees",
        body=body6, faqs=faqs6, signup=signup6,
        side_big=pct(net(TAKER, r6)), side_label=f"Bitget taker you effectively pay after the {r6}% rebate (standard {pct(TAKER)})",
    ))

    # ---- Bitget UID: find it and use it to claim a rebate (2026-11-19, 서이오) -------------------------
    # UID steps verified 2026-11-19 on Bitget's own support article "How to Check Your Bitget Account UID"
    # (dated 2026-01-30). Fee numbers: Bitget standard futures 0.02% / 0.06%, verified 2026-11-03 (see above).
    ux = V["bitget"]
    assert (ux["maker"], ux["taker"]) == (MAKER, TAKER), "Bitget fee in VENUES no longer matches the verified guide numbers"
    r7 = ux["rebate"]
    UID_URL = "https://www.bitget.com/support/articles/12560603808647"
    signup7 = link(ux, "guide-bitget-uid")
    def s7(x): return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    size7, trips7 = 5000, 30
    rt7_t, rt7_m = size7 * TAKER / 100 * 2, size7 * (MAKER + TAKER) / 100
    rows7 = "".join(
        f"<tr><td>{name}</td><td>{s7(rt)}</td><td>{s7(rt * trips7)}</td><td>+{s7(rt * trips7 * r7 / 100)}</td><td>{s7(rt * trips7 * (1 - r7 / 100))}</td></tr>"
        for name, rt in [("Market in, market out", rt7_t), ("Limit in, market out", rt7_m)])
    body7 = f"""
<h2>The short version</h2>
<p>Your Bitget UID is the user identification number Bitget creates for your account when you sign up. On the website it appears when you hover over the profile icon in the top-right corner. In the app, tap the profile icon at the top left of the Home page, then <b>Profile</b>. In both places you can tap or click the number to copy it.</p>
<p>That is the whole answer if you are in a hurry. The rest of this guide covers why a fee-rebate service asks for your UID, what you should and should not send with it, and what the rebate is worth in dollars on Bitget's standard futures fees, so you can decide whether claiming one is worth five minutes.</p>
<p class="src">Source: <a href="{UID_URL}" target="_blank" rel="noopener">How to Check Your Bitget Account UID</a> (Bitget Support Center, dated 30 Jan 2026), checked 19 Nov 2026. Bitget redesigns its menus from time to time; if a button has moved, the support article is the place to check.</p>

<h2>What a UID is, and what it is not</h2>
<p>Bitget describes the UID as a user identification number that is generated automatically at sign-up. Each account has exactly one, and its support team uses it to identify the account for customer support and other account-related services.</p>
<p>It is not your email address or your phone number, and you cannot pick it. Bitget's support article is clear that the UID cannot be changed. If you open a second account, that account gets a different UID. This matters for rebates: a rebate is tied to the specific account that was opened through a referral link, so the UID you send has to be that account's UID.</p>

<h2>How to find your Bitget UID on the website</h2>
<ol class="gd-steps">
  <li><div><b>Log in to Bitget in your browser</b><p>Use the account you want the rebate on.</p></div></li>
  <li><div><b>Hover over the profile icon</b><p>It sits in the top-right corner. Bitget calls it "My Profile". Your UID appears in the menu that opens.</p></div></li>
  <li><div><b>Click to copy it</b><p>Clicking the number copies it. You can also open your Dashboard (the profile page of your account) and copy the UID from there.</p></div></li>
</ol>

<h2>How to find your Bitget UID in the app</h2>
<ol class="gd-steps">
  <li><div><b>Open the Bitget app and log in</b><p>Make sure you are on the right account if you have more than one.</p></div></li>
  <li><div><b>Tap the profile icon</b><p>On the Home page, it is in the top-left corner.</p></div></li>
  <li><div><b>Tap "Profile"</b><p>Your UID is shown on the screen. Tap it to copy.</p></div></li>
</ol>
<p style="margin-top:20px">Paste it somewhere and check it before you send it. A single wrong digit points to someone else's account, and a rebate cannot be matched to your trades until the number is right.</p>

<h2>Why a rebate service asks for your UID</h2>
<p>When you open a Bitget account through a referral link, Bitget records that account under the referrer and pays the referrer a commission on the trading fees the account generates. A fee-rebate service passes part of that commission back to you. The UID is how the two sides are matched: it lets us find your account in the referral records and work out how much of your fees to return. Our guide to <a href="how-fee-rebates-work.html">how fee rebates work</a> goes through where the money comes from in more detail.</p>
<p>That also explains the one rule that catches people out. The referral is attached when the account is created. An account you opened earlier without our link is not in our referral records, so sending its UID will not start a rebate. The rebate on this page is for a <b>new</b> Bitget account opened through the sign-up button here.</p>

<h2>What to send, and what never to send</h2>
<p>A UID identifies an account. On its own it does not let anyone log in, trade or withdraw. Those actions need your password, your two-factor codes or an API key. Sending a UID to claim a rebate is normal, but keep the rest to yourself:</p>
<ul>
  <li><b>Send:</b> the exchange name and your UID, for example "Bitget 1234567890" (with your own number).</li>
  <li><b>Never send:</b> your password, 2FA or email verification codes, API keys, seed phrases, or screenshots that show any of these.</li>
  <li><b>Be wary of:</b> anyone who contacts you first and asks for your UID plus anything else. We only reply to messages you start, and we never ask for login details.</li>
</ul>

<h2>What the rebate is worth on Bitget</h2>
<p>On a standard Bitget account, USDT-margined perpetual futures cost {pct(MAKER)} for maker orders and {pct(TAKER)} for taker orders. Those are the rates in Bitget's own <a href="{FAQ_URL}" target="_blank" rel="noopener">trading fees FAQ</a>, which we checked on 3 November 2026. The fee is charged on the full position value, once to open and once to close.</p>
<p>Here is a trader who opens a {s7(size7)} position (margin times leverage) {trips7} times in a month, with two common order habits, and what comes back through {config['brand']}'s {r7}% rebate on Bitget.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Habit</th><th>Per round trip</th><th>Fees for {trips7}</th><th>Rebate {r7}%</th><th>Net cost</th></tr></thead>
  <tbody>{rows7}</tbody>
</table></div>
<p class="src">Bitget standard futures rates {pct(MAKER)} / {pct(TAKER)}, from the <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, checked 3 Nov 2026. Funding and VIP discounts are not included. The table is arithmetic, not a forecast of anyone's trading. Your logged-in fee rate always takes precedence.</p>
<p>Put simply, the {r7}% rebate brings the taker rate you effectively pay from {pct(TAKER)} to <b>{pct(net(TAKER, r7))}</b>, and the maker rate from {pct(MAKER)} to {pct(net(MAKER, r7))}. You still pay Bitget's normal fee when you trade; the rebate comes back afterwards. Funding payments go between traders rather than to the exchange, so they are not rebated. For the full fee picture, read <a href="bitget-futures-fees.html">Bitget futures fees explained</a>, or enter your own numbers in the <a href="../tools/futures-fee-calculator.html">fee calculator</a>.</p>

<h2>How to sign up and claim the {r7}% rebate on Bitget</h2>
<ol class="gd-steps">
  <li><div><b>Open a new Bitget account through our link</b><p>Use the sign-up button on this page. The referral is attached by the link, so there is no code to type. It only works for a new account.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity checks if Bitget asks for them where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>Website: hover over the profile icon at the top right. App: profile icon at the top left, then Profile.</p></div></li>
  <li><div><b>Send "Bitget + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your trading fees arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over to the next week.</p></div></li>
</ol>
<p style="margin-top:20px">Trading somewhere else? Every exchange we list has its own page with the same steps. Start from the <a href="../index.html#venues">exchange ranking</a>, which sorts all eleven venues by the taker fee left after the rebate, or go straight to our <a href="../exchanges/bitget.html">Bitget referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, quickly, and can wipe out your whole margin. A fee rebate lowers your costs; it does not make a losing strategy profitable. Start with low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">Bitget decides which countries it serves, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs7 = [
        ("Where do I find my Bitget UID?",
         "On the Bitget website, log in and hover over the profile icon in the top-right corner; the UID appears and you can click to copy it, or copy it from your Dashboard. In the app, tap the profile icon at the top left of the Home page, then Profile. These steps are from Bitget's support article, checked 19 November 2026."),
        ("Is it safe to share my Bitget UID?",
         "A UID identifies your account, and on its own it does not let anyone log in, trade or withdraw. Sharing it to claim a rebate or get support is normal. Never share your password, 2FA or email codes, API keys or seed phrase with anyone, including a rebate service."),
        ("Can I get a rebate on a Bitget account I already have?",
         f"Not through {config['brand']}. The referral is attached when an account is created, so the rebate works only for a new Bitget account opened through our link. On that account, {r7}% of the futures fees you pay comes back in USDT every Monday."),
    ]
    out.append(dict(
        slug="bitget-uid",
        venue=ux,
        title=f"How to Find Your Bitget UID (App & Web) and Claim a {r7}% Rebate | {config['brand']}",
        h1="Your Bitget UID: <em>where to find it, and what it gets you.</em>",
        crumb="Find your Bitget UID",
        desc=(f"Find your Bitget UID in the app or on the website in three taps, what is safe to share, "
              f"and how sending it gets {r7}% of your futures fees back each week."),
        lede=("Website: hover over the profile icon, top right. App: profile icon, top left, then Profile. "
              f"Here is what a UID is for, what never to send with it, and what claiming a {r7}% rebate is worth."),
        published="2026-11-19", modified="2026-11-19", checked="3 Nov 2026",
        keyword="bitget uid",
        body=body7, faqs=faqs7, signup=signup7,
        side_big=pct(net(TAKER, r7)), side_label=f"Bitget taker you effectively pay after the {r7}% rebate (standard {pct(TAKER)})",
    ))

    # ---- OKX futures fees (2026-11-20, 서이오) ---------------------------------------------------------
    # Verified 2026-11-20 on OKX's own help centre:
    #  - "How are futures trading fees calculated on OKX?" (updated 2026-08-26): "If the fee level is lv1, then the taker
    #    fee rate is 0.05%, and the maker fee rate is 0.02%", formula contract value x contracts x price x rate.
    #  - "Trading Fee Rules FAQ" (OKX Singapore, updated 2026-09-09): Regular/VIP levels by asset amount or 30-day volume,
    #    formula and worked example (100 BTCUSDT contracts x 0.01 BTC x 20,000 = taker 10 USDT / maker 4 USDT),
    #    liquidation charged at the current taker rate, expiry settlement 0.01%.
    #  - "Perpetual funding fee mechanism" (updated 2026-10-28): every 8 hours (00:00, 08:00, 16:00 UTC) by default,
    #    can switch to 1/2/4 hours; OKX charges no service fee on funding.
    #  - "How do I find my user ID (UID)?" (updated 2026-08-25): web and app steps.
    o = V["okx"]
    O_MAKER, O_TAKER = 0.02, 0.05
    assert (o["maker"], o["taker"]) == (O_MAKER, O_TAKER), "OKX fee in VENUES no longer matches the verified guide numbers"
    r8 = o["rebate"]
    OKX_CALC = "https://www.okx.com/en-us/help/how-to-calculate-the-contract-transaction-fee"
    OKX_RULES = "https://www.okx.com/en-sg/help/trading-fee-rules-faq"
    OKX_FUND = "https://www.okx.com/en-us/help/iv-introduction-to-perpetual-swap-funding-fee"
    OKX_UID = "https://www.okx.com/en-ae/help/how-do-i-find-my-user-id-uid"
    signup8 = link(o, "guide-okx-fees")
    def s8(x): return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    pos8, n8 = 10000, 20
    rt8_t = pos8 * O_TAKER / 100 * 2
    rt8_m = pos8 * (O_MAKER + O_TAKER) / 100
    rt8_mm = pos8 * O_MAKER / 100 * 2
    rows8 = "".join(
        f"<tr><td>{name}</td><td>${rt:,.2f}</td><td>${rt * n8:,.2f}</td><td>+${rt * n8 * r8 / 100:,.2f}</td><td>${rt * n8 * (1 - r8 / 100):,.2f}</td></tr>"
        for name, rt in [("Market in, market out", rt8_t), ("Limit in, market out", rt8_m), ("Limit in, limit out", rt8_mm)])
    ex_notional = 100 * 0.01 * 20000
    body8 = f"""
<h2>The short version</h2>
<p>At OKX's entry fee level (Lv1, the "Regular" tier most accounts start on), perpetual and expiry futures cost <b>{pct(O_MAKER)} for maker orders and {pct(O_TAKER)} for taker orders</b>. That is the rate OKX's own help centre uses when it explains how futures fees are calculated, which we checked on 20 November 2026. Higher VIP levels pay less.</p>
<p>The fee is charged on the full value of the position, not on your margin, and you pay it twice: once to open and once to close. On a {s8(pos8)} position that is {s8(pos8 * O_TAKER / 100)} per side as a taker. This guide turns those percentages into a monthly dollar figure, separates trading fees from funding, and shows what a {r8}% rebate through {config['brand']} does to the rate you end up paying.</p>
<p class="src">Sources: <a href="{OKX_CALC}" target="_blank" rel="noopener">How are futures trading fees calculated on OKX?</a> (OKX help centre, updated 26 Aug 2026) and <a href="{OKX_RULES}" target="_blank" rel="noopener">Trading Fee Rules FAQ</a> (updated 9 Sep 2026), both checked 20 Nov 2026. OKX runs regional entities with their own terms, so the rate on your logged-in fee page is the one that applies to you.</p>

<h2>How OKX sets your fee level</h2>
<p>OKX splits accounts into two groups: Regular and VIP. According to its trading fee rules, VIP levels are based on your asset balance or your trading volume over the past 30 days, and you get whichever of the two gives the better rate. The volume that counts covers spot, perpetual and expiry futures, options and spreads together.</p>
<p>For most people this is academic. VIP thresholds are set for large accounts, and if you trade a few thousand dollars at a time you are on the Regular tier and will stay there. That makes the entry rate the number to plan around, and it is why order type and rebates matter more to an ordinary trader than chasing a VIP level.</p>

<h2>Maker or taker on OKX</h2>
<p>A <b>taker</b> order fills straight away against orders already on the book: every market order, and any limit order priced to fill at once. A <b>maker</b> order rests on the book first and fills later when someone trades against it. On OKX the taker rate is two and a half times the maker rate ({pct(O_TAKER)} against {pct(O_MAKER)}).</p>
<p>Two details catch people out. Stop-losses that trigger as market orders are taker fills. And if a position is forcibly liquidated, OKX's fee rules say the liquidation is charged at the taker rate of your current tier, on top of the loss itself. Our <a href="maker-vs-taker-fees.html">maker vs taker guide</a> goes through the difference in more depth.</p>

<h2>How the fee is calculated</h2>
<p>OKX's formula for USDT-margined perpetuals is: fee rate × number of contracts × contract size × fill price. Each contract stands for a fixed amount of the coin, so the part after the fee rate is simply the dollar value of what you traded.</p>
<p>OKX's own worked example uses 100 BTCUSDT perpetual contracts, each worth 0.01 BTC, with bitcoin at 20,000 USDT. That is a position worth {s8(ex_notional)}. As a taker the fee is {s8(ex_notional)} × {pct(O_TAKER)} = <b>{s8(ex_notional * O_TAKER / 100)}</b>; as a maker it is {s8(ex_notional)} × {pct(O_MAKER)} = <b>{s8(ex_notional * O_MAKER / 100)}</b>. The fee is taken in USDT when the order fills.</p>
<p>Leverage does not change the rate. It changes how large a position you can open with the same margin, and the fee follows the position. A {s8(1000)} margin at 10× opens a {s8(pos8)} position and pays fees on {s8(pos8)}, not on {s8(1000)}. If you want to see where that leaves your break-even, read <a href="futures-break-even-price.html">futures break-even price after fees</a>.</p>

<h2>What a month on OKX costs, before and after the rebate</h2>
<p>Here is a trader who opens and closes a {s8(pos8)} position {n8} times in a month, with three different order habits, and what comes back through {config['brand']}'s {r8}% rebate on OKX.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Habit</th><th>Per round trip</th><th>Fees for {n8}</th><th>Rebate {r8}%</th><th>Net cost</th></tr></thead>
  <tbody>{rows8}</tbody>
</table></div>
<p class="src">OKX Lv1 futures rates {pct(O_MAKER)} maker / {pct(O_TAKER)} taker from the <a href="{OKX_CALC}" target="_blank" rel="noopener">OKX help centre</a>, checked 20 Nov 2026. Funding and VIP discounts are not included. The table is arithmetic, not a forecast of anyone's trading.</p>
<p>The rebate brings the taker rate you effectively pay from {pct(O_TAKER)} to <b>{pct(net(O_TAKER, r8))}</b>, and the maker rate from {pct(O_MAKER)} to {pct(net(O_MAKER, r8))}. You still pay OKX's normal fee when you trade. The rebate is paid back to you afterwards by {config['brand']}, in USDT, every Monday. To try your own size and trade count, use the <a href="../tools/futures-fee-calculator.html">fee calculator</a>.</p>

<h2>Funding is not a trading fee</h2>
<p>Perpetual futures also carry funding, and it shows up on the same statement, so it is easy to lump in with fees. It is a different thing. OKX's funding page says funding is exchanged every 8 hours by default, at 00:00, 08:00 and 16:00 UTC, and that some contracts switch to every 1, 2 or 4 hours when the rate hits its cap or floor. When the rate is positive, longs pay shorts; when it is negative, shorts pay longs. The amount is position value × funding rate.</p>
<p>OKX says it charges no service fee on funding, because the money goes from trader to trader. That is also why no rebate applies to it. If you hold positions across several funding times, check the current rate and countdown on the contract page before you open. Our <a href="how-funding-fees-work.html">funding fees guide</a> explains how the rate moves.</p>
<p class="src">Source: <a href="{OKX_FUND}" target="_blank" rel="noopener">Perpetual funding fee mechanism</a> (OKX help centre, updated 28 Oct 2026), checked 20 Nov 2026. Expiry futures also carry a separate 0.01% settlement fee at expiry, per OKX's <a href="{OKX_RULES}" target="_blank" rel="noopener">fee rules</a>.</p>

<h2>Three ways to pay less on OKX</h2>
<ul>
  <li><b>Enter with limit orders.</b> A resting limit entry moves that leg from {pct(O_TAKER)} to {pct(O_MAKER)}. Over twenty round trips on {s8(pos8)}, that alone is the gap between the first two rows of the table above.</li>
  <li><b>Trade less often, in the same size.</b> Fees scale with the number of round trips. Ten well-chosen trades cost half as much as twenty rushed ones.</li>
  <li><b>Get part of every fee back.</b> Open your OKX account through a fee-rebate partner and a share of the commission comes back to you. Through {config['brand']} it is {r8}% on OKX, paid weekly in USDT. Our guide to <a href="how-fee-rebates-work.html">how fee rebates work</a> explains where the money comes from.</li>
</ul>

<h2>How to sign up and claim the {r8}% rebate on OKX</h2>
<ol class="gd-steps">
  <li><div><b>Open a new OKX account through our link</b><p>Use the sign-up button on this page. The referral is attached by the link, so there is no code to type. It only works for a new account.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity verification if OKX asks for it where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>Website: hover over the profile option to see your user ID, or open Profile &gt; Personal info and use the copy button. App: open the menu to reach the User Center; your UID is in the Profile section with a Copy option.</p></div></li>
  <li><div><b>Send "OKX + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your trading fees arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over to the next week.</p></div></li>
</ol>
<p class="src">UID steps from <a href="{OKX_UID}" target="_blank" rel="noopener">How do I find my user ID (UID)?</a> (OKX help centre, updated 25 Aug 2026), checked 20 Nov 2026. Step-by-step with what is safe to send: <a href="okx-uid.html">how to find your OKX UID</a>.</p>
<p style="margin-top:20px">Comparing venues first? The <a href="../index.html#venues">exchange ranking</a> sorts every exchange we list by the taker fee left after the rebate. For the account itself, see our <a href="../exchanges/okx.html">OKX referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, quickly, and can wipe out your whole margin. A fee rebate lowers your costs; it does not make a losing strategy profitable. Start with low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">OKX decides which countries it serves and runs separate regional entities, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs8 = [
        ("What are OKX's futures trading fees?",
         f"At OKX's entry fee level (Lv1), futures cost {pct(O_MAKER)} for maker orders and {pct(O_TAKER)} for taker orders, charged on the full position value when you open and again when you close. That is the rate in OKX's help centre, checked 20 November 2026. VIP levels pay less, and the rate on your logged-in fee page always applies."),
        ("How do I get a discount on OKX futures fees?",
         f"Use limit orders to pay the maker rate, reach a VIP level through assets or 30-day volume, or open a new account through a fee-rebate partner. Through {config['brand']}, {r8}% of the OKX futures fees you pay comes back in USDT every Monday, which brings the effective taker rate to {pct(net(O_TAKER, r8))}."),
        ("Is the OKX funding fee part of the trading fee?",
         "No. Funding is exchanged between long and short holders, every 8 hours by default (00:00, 08:00 and 16:00 UTC), and OKX says it takes no service fee on it. Because it does not go to the exchange, it is not covered by a fee rebate."),
    ]
    out.append(dict(
        slug="okx-futures-fees",
        venue=o,
        title=f"OKX Futures Fees 2026: Maker, Taker, Funding & a {r8}% Rebate | {config['brand']}",
        h1="OKX futures fees, <em>worked out in dollars.</em>",
        crumb="OKX futures fees",
        desc=(f"OKX futures fees are {pct(O_MAKER)} maker / {pct(O_TAKER)} taker at Lv1. What a month of trades costs, "
              f"how funding differs, and how a {r8}% rebate cuts taker to {pct(net(O_TAKER, r8))}."),
        lede=(f"The entry rate is {pct(O_MAKER)} maker and {pct(O_TAKER)} taker, charged on the whole position. "
              f"Here is what that comes to in a normal month, where funding fits in, and how to get {r8}% of it back."),
        published="2026-11-20", modified="2026-11-20", checked="20 Nov 2026",
        keyword="okx futures fees",
        body=body8, faqs=faqs8, signup=signup8,
        side_big=pct(net(O_TAKER, r8)), side_label=f"OKX taker you effectively pay after the {r8}% rebate (Lv1 {pct(O_TAKER)})",
    ))

    # ---- OKX vs Bitget futures fees (2026-11-23, 서이오) ------------------------------------------------
    # No new fee numbers: reuses only the rates already verified on the exchanges' own pages —
    #  OKX Lv1 0.02%/0.05%, VIP by assets or 30-day volume, liquidation at taker rate, funding 8h default
    #  (OKX help centre, checked 2026-11-20, see block above) and Bitget standard 0.02%/0.06%, VIP by volume/assets/BGB,
    #  funding every 8 hours (Bitget Trading Fees FAQ, checked 2026-11-03, see first block).
    #  Re-reading both pages on 2026-11-23 failed (fetch not approved in the scheduled run), so the text keeps the original check dates.
    #  Bitget UID steps re-read 2026-11-23 on "How to Check Your Bitget Account UID" (page dated 2026-01-30).
    bx, ox = V["bitget"], V["okx"]
    assert (bx["maker"], bx["taker"]) == (MAKER, TAKER) and (ox["maker"], ox["taker"]) == (O_MAKER, O_TAKER)
    rb9, ro9 = bx["rebate"], ox["rebate"]
    sign_o9, sign_b9 = link(ox, "guide-okx-vs-bitget"), link(bx, "guide-okx-vs-bitget")
    def s9(x): return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    pos9, n9 = 10000, 20
    habits9 = [("Market in, market out", O_TAKER * 2, TAKER * 2),
               ("Limit in, market out", O_MAKER + O_TAKER, MAKER + TAKER),
               ("Limit in, limit out", O_MAKER * 2, MAKER * 2)]
    rows9 = "".join(
        f"<tr><td>{h}</td><td>{s9(pos9 * o_ / 100 * n9)}</td><td>{s9(pos9 * o_ / 100 * n9 * (1 - ro9 / 100))}</td>"
        f"<td>{s9(pos9 * b_ / 100 * n9)}</td><td>{s9(pos9 * b_ / 100 * n9 * (1 - rb9 / 100))}</td></tr>"
        for h, o_, b_ in habits9)
    gap9 = pos9 * (TAKER - O_TAKER) / 100 * 2 * n9
    body9 = f"""
<h2>The short version</h2>
<p>On the entry fee tier, OKX and Bitget charge the same for maker orders on perpetual futures, <b>{pct(O_MAKER)}</b>. The difference is on the taker side: <b>{pct(O_TAKER)} on OKX against {pct(TAKER)} on Bitget</b>. If most of your fills are market orders, OKX is the cheaper of the two by one basis point per side. If you mostly work with resting limit orders, the two cost the same.</p>
<p>That is a small gap on a single trade and a real one over a month. A trader who opens and closes a {s9(pos9)} position {n9} times with market orders pays {s9(gap9)} more on Bitget than on OKX, before any rebate. Below we put both exchanges side by side in dollars, cover what changes the rate (VIP levels, order type, liquidations), and show what a fee rebate through {config['brand']} leaves you paying on each.</p>
<p class="src">Sources: OKX Lv1 rates from <a href="{OKX_CALC}" target="_blank" rel="noopener">How are futures trading fees calculated on OKX?</a> and the <a href="{OKX_RULES}" target="_blank" rel="noopener">OKX Trading Fee Rules FAQ</a>, checked 20 Nov 2026. Bitget standard rates from the <a href="{FAQ_URL}" target="_blank" rel="noopener">Bitget Trading Fees FAQ</a>, checked 3 Nov 2026. The rate on your own logged-in fee page always takes precedence.</p>

<h2>Side by side: the rates that matter</h2>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Entry tier, USDT perpetuals</th><th>OKX (Lv1)</th><th>Bitget (standard)</th></tr></thead>
  <tbody>
    <tr><td>Maker fee</td><td>{pct(O_MAKER)}</td><td>{pct(MAKER)}</td></tr>
    <tr><td>Taker fee</td><td>{pct(O_TAKER)}</td><td>{pct(TAKER)}</td></tr>
    <tr><td>Market round trip on {s9(pos9)}</td><td>{s9(pos9 * O_TAKER / 100 * 2)}</td><td>{s9(pos9 * TAKER / 100 * 2)}</td></tr>
    <tr><td>How VIP levels are set</td><td>Assets or 30-day volume, whichever is better</td><td>Volume, assets or BGB holdings</td></tr>
    <tr><td>Default funding interval</td><td>Every 8 hours</td><td>Every 8 hours</td></tr>
    <tr><td>{config['brand']} rebate</td><td>{ro9}%</td><td>{rb9}%</td></tr>
    <tr class="tot"><td>Taker you effectively pay</td><td>{pct(net(O_TAKER, ro9))}</td><td>{pct(net(TAKER, rb9))}</td></tr>
  </tbody>
</table></div>
<p class="src">Fee rows from each exchange's own help centre (dates above). Rebate rows are {config['brand']}'s rates. The last row is the taker fee minus the rebate, not a rate either exchange quotes.</p>
<p>Both exchanges charge the fee on the full value of the position, not on the margin you put up, and both charge it twice: once to open and once to close. Leverage does not change the rate. It changes how big a position the same margin can open, and the fee follows the position. A {s9(1000)} margin at 10× pays fees on {s9(pos9)}.</p>

<h2>What a month costs on each, before and after the rebate</h2>
<p>Same trader, same habits, two exchanges: {n9} round trips a month on a {s9(pos9)} position. The three rows are three ways of placing the orders.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Habit</th><th>OKX fees</th><th>OKX net ({ro9}%)</th><th>Bitget fees</th><th>Bitget net ({rb9}%)</th></tr></thead>
  <tbody>{rows9}</tbody>
</table></div>
<p class="src">OKX Lv1 {pct(O_MAKER)} / {pct(O_TAKER)} (checked 20 Nov 2026), Bitget standard {pct(MAKER)} / {pct(TAKER)} (checked 3 Nov 2026). Funding and VIP discounts not included. The table is arithmetic, not a forecast of anyone's trading.</p>
<p>Two things stand out. First, the order habit moves the bill far more than the choice of exchange: going from market-in-market-out to limit-in-limit-out cuts the monthly cost by more than half on either venue. Second, once both legs are limit orders the two exchanges cost exactly the same, because the maker rates match. The OKX advantage only exists on taker fills.</p>
<p>To try your own size and trade count on both exchanges at once, use the <a href="../tools/futures-fee-calculator.html">futures fee calculator</a>.</p>

<h2>What changes your rate on each exchange</h2>
<p><b>VIP levels.</b> OKX's fee rules say VIP levels depend on your asset balance or your trading volume over the past 30 days, and you get whichever gives the better rate. Bitget says its rates fall as you move up VIP levels based on trading volume, assets or BGB holdings. Either way, the thresholds are aimed at large accounts. If you trade a few thousand dollars at a time, plan around the entry rates in the table, and read the current thresholds on each exchange's own fee page rather than on third-party lists.</p>
<p><b>Order type.</b> A taker order fills straight away against the book: every market order, and a limit order priced to fill at once. A maker order rests on the book until someone trades against it. Stop-losses that trigger as market orders are taker fills on both exchanges, so even a patient trader pays the taker rate on some exits. Our <a href="maker-vs-taker-fees.html">maker vs taker guide</a> explains the difference in more depth.</p>
<p><b>Liquidation.</b> OKX's fee rules say a forced liquidation is charged at the taker rate of your current tier, on top of the loss. That is one more reason to size positions so a single move cannot liquidate you.</p>

<h2>Funding is not part of the comparison</h2>
<p>Perpetual futures on both exchanges also carry funding, a payment between long and short holders that keeps the contract price close to the spot price. OKX exchanges funding every 8 hours by default, at 00:00, 08:00 and 16:00 UTC, and some contracts switch to every 1, 2 or 4 hours when the rate hits its cap or floor. Bitget's FAQ also gives 8 hours. When the rate is positive, longs pay shorts; when negative, shorts pay longs.</p>
<p>Funding goes from trader to trader, so neither exchange keeps it and no rebate applies to it. The rate depends on the contract and the moment, not on which exchange's fee schedule is cheaper, so it does not belong in a fee comparison. Check the live rate and countdown on the contract page before you hold through a funding time. Our <a href="how-funding-fees-work.html">funding fees guide</a> explains how the rate moves.</p>
<p class="src">Funding sources: <a href="{OKX_FUND}" target="_blank" rel="noopener">OKX perpetual funding fee mechanism</a> (checked 20 Nov 2026) and <a href="{BRK_URL}" target="_blank" rel="noopener">Understanding Bitget's Fees</a> (checked 3 Nov 2026).</p>

<h2>Which one fits how you trade</h2>
<ul>
  <li><b>Mostly market orders, short holds.</b> OKX's lower taker rate is the one number that separates the two. After rebates the effective taker is {pct(net(O_TAKER, ro9))} on OKX and {pct(net(TAKER, rb9))} on Bitget.</li>
  <li><b>Mostly limit orders.</b> Fees are a tie at {pct(O_MAKER)} per side, so choose on what else matters to you: the contracts you trade, the app, and which entity serves your country.</li>
  <li><b>Already using one of them.</b> Switching exchanges to save one basis point is rarely worth the hassle. Moving more of your entries to limit orders saves more on either.</li>
</ul>
<p>None of this is a recommendation to trade. It is a comparison of what trading costs if you already do. For the full picture on each venue, see our <a href="okx-futures-fees.html">OKX futures fees guide</a> and <a href="bitget-futures-fees.html">Bitget futures fees guide</a>, or the <a href="../index.html#venues">ranking of all eleven exchanges</a> by the taker fee left after the rebate.</p>

<h2>How to sign up and claim the rebate</h2>
<ol class="gd-steps">
  <li><div><b>Open a new account through our link</b><p><a href="{sign_o9}" target="_blank" rel="sponsored nofollow noopener">OKX ({ro9}% back)</a> or <a href="{sign_b9}" target="_blank" rel="sponsored nofollow noopener">Bitget ({rb9}% back)</a>. The referral is attached by the link, so there is no code to type. It only works for a new account.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity verification if the exchange asks for it where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>OKX website: hover over the profile option, or open Profile &gt; Personal info and use the copy button. Bitget website: hover over the My Profile icon in the top-right corner and click to copy. In either app, open your profile from the home screen and the UID is shown with a copy option.</p></div></li>
  <li><div><b>Send "exchange name + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your trading fees arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over to the next week.</p></div></li>
</ol>
<p class="src">UID steps from <a href="{OKX_UID}" target="_blank" rel="noopener">OKX: How do I find my user ID (UID)?</a> (checked 20 Nov 2026) and <a href="{UID_URL}" target="_blank" rel="noopener">Bitget: How to Check Your Bitget Account UID</a> (checked 23 Nov 2026). More on each account: <a href="../exchanges/okx.html">OKX referral page</a> · <a href="../exchanges/bitget.html">Bitget referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, quickly, and can wipe out your whole margin. A lower fee or a rebate reduces your costs; it does not make a losing strategy profitable. Start with low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">OKX and Bitget each decide which countries they serve, and OKX runs separate regional entities, so check the terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs9 = [
        ("Is OKX or Bitget cheaper for futures?",
         f"On the entry tier, maker orders cost the same on both ({pct(O_MAKER)}). Taker orders cost {pct(O_TAKER)} on OKX and {pct(TAKER)} on Bitget, so OKX is cheaper if you mostly use market orders. Rates checked on each exchange's help centre (OKX 20 Nov 2026, Bitget 3 Nov 2026); your logged-in fee page always applies."),
        ("What do I pay after a rebate on OKX and Bitget?",
         f"Through {config['brand']}, {ro9}% of OKX futures fees and {rb9}% of Bitget futures fees come back in USDT every Monday. That brings the effective taker rate to {pct(net(O_TAKER, ro9))} on OKX and {pct(net(TAKER, rb9))} on Bitget. You still pay the normal fee when you trade; the rebate is paid afterwards."),
        ("Does the funding fee differ between OKX and Bitget?",
         "Funding is not a trading fee. On both exchanges it is exchanged between long and short holders, every 8 hours by default, and the exchange does not keep it. The rate depends on the contract and market conditions, so check it on the contract page. No rebate applies to funding."),
    ]
    out.append(dict(
        slug="okx-vs-bitget-futures-fees",
        venue=ox,
        title=f"OKX vs Bitget Futures Fees 2026: Maker, Taker & Rebates Compared | {config['brand']}",
        h1="OKX vs Bitget futures fees, <em>side by side.</em>",
        crumb="OKX vs Bitget futures fees",
        desc=(f"OKX vs Bitget futures fees: both {pct(O_MAKER)} maker, taker {pct(O_TAKER)} vs {pct(TAKER)}. Monthly cost in dollars "
              f"for three order habits, and what a {ro9}% rebate leaves you paying."),
        lede=(f"Maker fees are a tie. Taker fees are not: {pct(O_TAKER)} on OKX, {pct(TAKER)} on Bitget. "
              f"Here is what that difference comes to in a month, and what each costs after a rebate."),
        published="2026-11-23", modified="2026-11-23", checked="20 Nov 2026 (OKX) · 3 Nov 2026 (Bitget)",
        keyword="okx vs bitget fees",
        body=body9, faqs=faqs9, signup=sign_o9,
        side_big=pct(net(O_TAKER, ro9)), side_label=f"OKX taker you effectively pay after the {ro9}% rebate (Bitget: {pct(net(TAKER, rb9))})",
    ))

    # ---- OKX UID: find it and use it to claim a rebate (2026-11-24, 서이오) ------------------------------
    # No new numbers. UID steps and fees reuse only what was verified 2026-11-20 on OKX's own help centre (block above):
    #  "How do I find my user ID (UID)?" (updated 2026-08-25): web = hover over the profile option, or Profile > Personal info
    #  + copy button; app = menu > User Center, UID in the Profile section with Copy.
    #  Lv1 0.02% / 0.05%, liquidation at current taker rate, VIP by assets or 30-day volume, funding 8h, regional entities.
    #  Re-reading the UID page on 2026-11-24 failed (fetch not approved in the scheduled run), so the text keeps 20 Nov 2026.
    ou = V["okx"]
    assert (ou["maker"], ou["taker"]) == (O_MAKER, O_TAKER), "OKX fee in VENUES no longer matches the verified guide numbers"
    r10 = ou["rebate"]
    signup10 = link(ou, "guide-okx-uid")
    def s10(x): return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    size10, trips10 = 5000, 30
    habits10 = [("Market in, market out", O_TAKER * 2), ("Limit in, market out", O_MAKER + O_TAKER), ("Limit in, limit out", O_MAKER * 2)]
    rows10 = "".join(
        f"<tr><td>{h}</td><td>${size10 * rt / 100:,.2f}</td><td>${size10 * rt / 100 * trips10:,.2f}</td>"
        f"<td>+${size10 * rt / 100 * trips10 * r10 / 100:,.2f}</td><td>${size10 * rt / 100 * trips10 * (1 - r10 / 100):,.2f}</td></tr>"
        for h, rt in habits10)
    mo10_t = size10 * O_TAKER / 100 * 2 * trips10
    body10 = f"""
<h2>The short version</h2>
<p>Your OKX UID is the user ID number attached to your account. On the OKX website, hover over the profile option at the top of the page and the UID is shown there. You can also open <b>Profile &gt; Personal info</b> and use the copy button next to it. In the OKX app, open the menu to reach the <b>User Center</b>; the UID sits in the Profile section with a <b>Copy</b> option.</p>
<p>If that is all you came for, you are done. The rest of this page is for people who were asked for their UID by a fee-rebate service and want to know three things first: why the number is needed, what is safe to send alongside it, and whether the rebate is worth the two minutes on OKX's actual fees.</p>
<p class="src">Source: <a href="{OKX_UID}" target="_blank" rel="noopener">How do I find my user ID (UID)?</a> (OKX help centre, updated 25 Aug 2026), checked 20 Nov 2026. OKX runs separate regional entities and updates its menus from time to time, so if a button has moved on your version, that help article is the place to look.</p>

<h2>How to find your OKX UID on the website</h2>
<ol class="gd-steps">
  <li><div><b>Log in at okx.com</b><p>Use the account you actually trade on. If you have more than one, check you are in the right one before you copy anything.</p></div></li>
  <li><div><b>Hover over the profile option</b><p>It is in the top bar. Your user ID appears in the panel that opens.</p></div></li>
  <li><div><b>Or open Profile &gt; Personal info</b><p>The UID is listed on that page with a copy button beside it. Copying beats retyping a long number by hand.</p></div></li>
</ol>

<h2>How to find your OKX UID in the app</h2>
<ol class="gd-steps">
  <li><div><b>Open the OKX app and log in</b><p>Same rule: be sure you are on the account you want the rebate on.</p></div></li>
  <li><div><b>Open the menu and go to User Center</b><p>This is where OKX keeps your account details.</p></div></li>
  <li><div><b>Find the Profile section and tap Copy</b><p>Your UID is shown there. Tap Copy and paste it somewhere to check it.</p></div></li>
</ol>
<p style="margin-top:20px">Before sending it anywhere, read the pasted number once against the screen. One wrong digit belongs to a different account, and a rebate cannot be matched to your trades until the number is right.</p>

<h2>Why a rebate service asks for it</h2>
<p>When an account is opened through a referral link, OKX records it under the referrer and shares part of the trading fees that account pays. A fee-rebate service such as {config['brand']} passes a slice of that share back to the trader. The UID is the link between the two records: it lets us find your account in the referral report and work out how much of your fees to return each week. Our guide to <a href="how-fee-rebates-work.html">how fee rebates work</a> goes through where the money comes from.</p>
<p>The same mechanism explains the most common disappointment. The referral is fixed when the account is created. An OKX account you opened earlier without our link is not in our referral report, so sending its UID will not start a rebate. The rebate described here is for a <b>new</b> OKX account opened through the sign-up button on this page.</p>

<h2>What to send, and what never to send</h2>
<p>A UID tells someone which account you mean. It is not a key to that account: logging in, trading and withdrawing need your password, your two-factor codes or an API key. So sending a UID to claim a rebate or to get support is routine. Everything else stays with you.</p>
<ul>
  <li><b>Send:</b> the exchange and the number, for example "OKX 1234567890" with your own UID.</li>
  <li><b>Never send:</b> passwords, 2FA or email verification codes, API keys, seed phrases, or screenshots that show any of them.</li>
  <li><b>Be suspicious of:</b> anyone who messages you first, or who asks for your UID together with anything else. We reply only to conversations you start, and we never ask for login details.</li>
</ul>

<h2>What the rebate is worth on OKX</h2>
<p>At OKX's entry fee level (Lv1), futures cost {pct(O_MAKER)} for maker orders and {pct(O_TAKER)} for taker orders, according to OKX's own explanation of <a href="{OKX_CALC}" target="_blank" rel="noopener">how futures trading fees are calculated</a>. The fee is charged on the full position value, not your margin, once when you open and again when you close. VIP levels pay less, but OKX sets them by asset balance or 30-day trading volume, at levels aimed at large accounts.</p>
<p>Here is a trader who opens and closes a {s10(size10)} position (margin times leverage) {trips10} times in a month, with three order habits, and what comes back through {config['brand']}'s {r10}% rebate on OKX.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Habit</th><th>Per round trip</th><th>Fees for {trips10}</th><th>Rebate {r10}%</th><th>Net cost</th></tr></thead>
  <tbody>{rows10}</tbody>
</table></div>
<p class="src">OKX Lv1 futures rates {pct(O_MAKER)} / {pct(O_TAKER)} from the <a href="{OKX_CALC}" target="_blank" rel="noopener">OKX help centre</a> and <a href="{OKX_RULES}" target="_blank" rel="noopener">Trading Fee Rules FAQ</a>, checked 20 Nov 2026. Funding and VIP discounts not included. The table is arithmetic, not a forecast of anyone's trading. The rate on your logged-in fee page always applies.</p>
<p>The habit that pays most in fees also gets the most back: on the market-in, market-out row, {s10(mo10_t)} of fees returns {s10(mo10_t * r10 / 100)} in a month. In rate terms, the rebate brings the taker fee you effectively pay from {pct(O_TAKER)} to <b>{pct(net(O_TAKER, r10))}</b>, and the maker fee from {pct(O_MAKER)} to {pct(net(O_MAKER, r10))}. You still pay OKX's normal fee when you trade; the rebate is paid afterwards, in USDT, every Monday.</p>
<p>Two things the rebate does not touch. Funding moves between long and short holders, every 8 hours by default on OKX, and OKX says it takes no service fee on it, so there is nothing to share back. And if a position is forcibly liquidated, OKX charges that at your taker rate on top of the loss; a rebate on the fee does nothing about the loss. For the full fee picture, read <a href="okx-futures-fees.html">OKX futures fees explained</a>, or put your own numbers in the <a href="../tools/futures-fee-calculator.html">fee calculator</a>.</p>

<h2>How to sign up and claim the {r10}% rebate on OKX</h2>
<ol class="gd-steps">
  <li><div><b>Open a new OKX account through our link</b><p>Use the sign-up button on this page. The referral is attached by the link, so there is no code to type. It only works for a new account.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication and complete identity verification if OKX asks for it where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>Website: hover over the profile option, or Profile &gt; Personal info and the copy button. App: menu, User Center, Profile section, Copy.</p></div></li>
  <li><div><b>Send "OKX + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your trading fees arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over to the next week.</p></div></li>
</ol>
<p style="margin-top:20px">Still choosing an exchange? The <a href="../index.html#venues">exchange ranking</a> sorts every venue we list by the taker fee left after the rebate, and <a href="okx-vs-bitget-futures-fees.html">OKX vs Bitget futures fees</a> puts the two side by side. For the account itself, see our <a href="../exchanges/okx.html">OKX referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you more than you expect, quickly, and can wipe out your whole margin. A fee rebate lowers your costs; it does not make a losing strategy profitable. Start with low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">OKX decides which countries it serves and runs separate regional entities, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice, and {config['brand']} earns a referral commission, part of which it shares with you as the rebate.</p>
</div>
"""
    faqs10 = [
        ("Where do I find my OKX UID?",
         "On the OKX website, log in and hover over the profile option to see your user ID, or open Profile > Personal info and use the copy button. In the app, open the menu, go to User Center, and copy the UID from the Profile section. These steps are from OKX's help centre, checked 20 November 2026."),
        ("Is it safe to share my OKX UID?",
         "A UID identifies your account; on its own it does not let anyone log in, trade or withdraw. Sharing it to claim a rebate or get support is normal. Never share your password, 2FA or email codes, API keys or seed phrase with anyone, including a rebate service."),
        ("Can I get a rebate on an OKX account I already have?",
         f"Not through {config['brand']}. The referral is attached when an account is created, so the rebate works only for a new OKX account opened through our link. On that account, {r10}% of the futures fees you pay comes back in USDT every Monday."),
    ]
    out.append(dict(
        slug="okx-uid",
        venue=ou,
        title=f"How to Find Your OKX UID (App & Web) and Claim a {r10}% Fee Rebate | {config['brand']}",
        h1="Your OKX UID: <em>where it is, and what it gets you.</em>",
        crumb="Find your OKX UID",
        desc=(f"Find your OKX UID on the website or in the app in a few taps, what is safe to send with it, "
              f"and how it gets {r10}% of your OKX futures fees back every week."),
        lede=("Website: hover over the profile option, or Profile > Personal info. App: menu, User Center, Profile. "
              f"Here is why a rebate service needs it, what never to send with it, and what {r10}% back is worth."),
        published="2026-11-24", modified="2026-11-24", checked="20 Nov 2026",
        keyword="okx uid",
        body=body10, faqs=faqs10, signup=signup10,
        side_big=pct(net(O_TAKER, r10)), side_label=f"OKX taker you effectively pay after the {r10}% rebate (Lv1 {pct(O_TAKER)})",
    ))

    # ---- BingX futures fees (2026-11-25, 서이오) -------------------------------------------------------
    # Verified 2026-11-25 on BingX's own support centre:
    #  "Perpetual Futures | Fee Schedule" (bingx.com/en/support/articles/360046487573): Taker 0.05%, Maker 0.02%,
    #   "VIP users can enjoy trading fee discount" (no VIP table on that page), funding settled 00:00/08:00/16:00 (UTC+8)
    #   = 16:00/00:00/08:00 UTC, longs pay shorts when positive, rate clamped between -0.3% and 0.3%,
    #   liquidation when Margin Rate <= Maintenance Margin Rate (0.5%) + Taker Fee Rate.
    #  "BingX Tutorial | How to Find My UID?" (articles/11257209092367): web = hover the profile icon top right, UID in dropdown,
    #   copy icon; app = tap 'Profile' icon upper left, UID beside avatar, copy icon.
    #  bingx.com/support/costs showed no fee table in fetched HTML — not used.
    B_MAKER, B_TAKER = 0.02, 0.05
    B_FEE = "https://bingx.com/en/support/articles/360046487573-perpetual-futures-fee-schedule"
    B_UID = "https://bingx.com/en/support/articles/11257209092367"
    bg = V["bingx"]
    assert (bg["maker"], bg["taker"]) == (B_MAKER, B_TAKER), "BingX fee in VENUES no longer matches the verified guide numbers"
    r11 = bg["rebate"]
    signup11 = link(bg, "guide-bingx-fees")
    def s11(x):
        x = round(x, 2)
        return f"${x:,.0f}" if x == int(x) else f"${x:,.2f}"
    pos11, n11 = 10000, 20
    habits11 = [("Market in, market out", B_TAKER * 2), ("Limit in, market out", B_MAKER + B_TAKER), ("Limit in, limit out", B_MAKER * 2)]
    rows11 = "".join(
        f"<tr><td>{h}</td><td>{s11(pos11 * rt / 100)}</td><td>{s11(pos11 * rt / 100 * n11)}</td>"
        f"<td>+{s11(pos11 * rt / 100 * n11 * r11 / 100)}</td><td>{s11(pos11 * rt / 100 * n11 * (1 - r11 / 100))}</td></tr>"
        for h, rt in habits11)
    mo11 = pos11 * B_TAKER / 100 * 2 * n11
    fund11 = pos11 * 0.01 / 100
    body11 = f"""
<h2>The short version</h2>
<p>BingX's published rate for perpetual futures is <b>{pct(B_MAKER)} for maker orders</b> (orders that rest on the book) and <b>{pct(B_TAKER)} for taker orders</b> (orders that fill straight away). Those are the numbers on BingX's own fee schedule page, which also says VIP users get a discount on top. Everyone else pays the two rates above.</p>
<p>Percentages that small are easy to wave away, so this page turns them into dollars: what one trade costs, what a normal month costs for three different order habits, how funding is different from a trading fee, and what is left to pay after a {r11}% fee rebate through {config['brand']}. Short version of the last part: the taker rate you effectively pay drops to <b>{pct(net(B_TAKER, r11))}</b>.</p>
<p class="src">Source: <a href="{B_FEE}" target="_blank" rel="noopener">BingX: Perpetual Futures | Fee Schedule</a>, checked 25 Nov 2026. The rate on your logged-in BingX account always takes precedence over anything written here, including this page.</p>

<h2>How the fee on a BingX futures trade adds up</h2>
<p>Perpetual futures fees are worked out on the value of the position, not on the margin you put down. A {s11(1000)} margin at 10× leverage controls a {s11(pos11)} position, and the fee is charged on the {s11(pos11)}. Leverage does not change the rate. It changes how big a position the same deposit can open, and the fee grows with the position.</p>
<p>You pay twice: once when you open and once when you close. So a round trip on a {s11(pos11)} position with market orders both ways costs {s11(pos11 * B_TAKER / 100)} to open and {s11(pos11 * B_TAKER / 100)} to close, {s11(pos11 * B_TAKER / 100 * 2)} in total. If the price barely moves, that {s11(pos11 * B_TAKER / 100 * 2)} is the whole result of the trade, and it comes out of your margin.</p>
<div class="gd-scroll"><table class="gd-tbl">
  <thead><tr><th>Order habit</th><th>One round trip ({s11(pos11)})</th><th>{n11} round trips</th><th>{r11}% rebate back</th><th>Net month</th></tr></thead>
  <tbody>{rows11}</tbody>
</table></div>
<p class="src">BingX standard rates {pct(B_MAKER)} maker / {pct(B_TAKER)} taker (checked 25 Nov 2026). Funding and VIP discounts not included. The table is plain arithmetic on those two rates, not a forecast of anyone's trading.</p>
<p>The habit matters more than anything else on the page. Swapping market orders for resting limit orders on both legs cuts the monthly bill from {s11(mo11)} to {s11(pos11 * B_MAKER / 100 * 2 * n11)} before any rebate. Most traders land somewhere in the middle row: patient on the way in, a market order or a triggered stop on the way out. Our <a href="maker-vs-taker-fees.html">maker vs taker guide</a> goes through when a limit order still counts as a taker fill.</p>

<h2>VIP discounts</h2>
<p>BingX's fee schedule says VIP users can get a trading fee discount and points to its separate fee page for the levels. We have not reproduced those thresholds here because we could not confirm the current table on BingX's own pages on the day we checked. If you trade a few thousand dollars at a time, the standard {pct(B_MAKER)} / {pct(B_TAKER)} is the rate to plan around. If your volume is large, read the live VIP table on BingX after you log in and compare it with a rebate, since the two are calculated differently.</p>

<h2>Funding is not a trading fee</h2>
<p>Holding a perpetual futures position through certain times also means paying or receiving funding. BingX settles funding three times a day, at 00:00, 08:00 and 16:00 in UTC+8 (that is 16:00, 00:00 and 08:00 UTC), and only on positions that are open at that moment. When the funding rate is positive, longs pay shorts; when it is negative, shorts pay longs. BingX's formula caps the rate between −0.3% and 0.3% per settlement.</p>
<p>The payment is the rate times your position value. As a purely illustrative figure, a rate of 0.01% on a {s11(pos11)} position would be {s11(fund11)} for that settlement. The live rate on the contract page is the only one that counts, and it changes. Because funding moves between traders and does not go to BingX as a fee, no rebate applies to it. Our <a href="how-funding-fees-work.html">funding fees guide</a> explains why the rate moves the way it does.</p>
<p><b>One more cost to know about.</b> BingX's fee page lists liquidation as happening when your margin rate falls to the maintenance margin rate (0.5%) plus the taker fee rate. In plain terms, the fee to close the position is already counted in where liquidation sits, which is one more reason to keep leverage low enough that a single move cannot reach it.</p>
<p class="src">Funding and liquidation wording from <a href="{B_FEE}" target="_blank" rel="noopener">BingX: Perpetual Futures | Fee Schedule</a>, checked 25 Nov 2026.</p>

<h2>Where BingX sits against other exchanges</h2>
<p>A {pct(B_TAKER)} taker rate matches OKX's entry level and is a little under the {pct(V['bitget']['taker'])} Bitget charges on its standard tier. Maker orders cost {pct(B_MAKER)} at all three. After the {config['brand']} rebate, BingX's effective taker rate is {pct(net(B_TAKER, r11))}. If you want to compare every venue we list by the fee that is left after the rebate, use the <a href="../index.html#venues">exchange ranking</a> or put your own size and trade count into the <a href="../tools/futures-fee-calculator.html">futures fee calculator</a>.</p>
<p>A cheaper fee is not a reason to move. If you already trade somewhere and know the platform, a basis point is rarely worth the switch. Moving more of your entries to limit orders saves more on any exchange.</p>

<h2>How to sign up and claim the {r11}% rebate</h2>
<ol class="gd-steps">
  <li><div><b>Open a new BingX account through our link</b><p><a href="{signup11}" target="_blank" rel="sponsored nofollow noopener">Sign up to BingX ({r11}% back)</a>. The referral is attached by the link, so there is nothing to type. It only works for a new account, not one you already have.</p></div></li>
  <li><div><b>Secure and verify the account</b><p>Turn on two-factor authentication, and complete identity verification if BingX asks for it where you live.</p></div></li>
  <li><div><b>Copy your UID</b><p>Website: hover over the profile icon in the top-right corner; the UID is in the dropdown with a copy icon next to it. App: tap the Profile icon in the upper-left corner; the UID is beside your avatar, with a copy icon on the right.</p></div></li>
  <li><div><b>Send "BingX + your UID" on Telegram</b><p>Message <a href="{tg_dm}" target="_blank" rel="noopener">@{config['telegram_dm']}</a>. We confirm within 24 hours. Never send a password, 2FA code or API key. We will never ask for them.</p></div></li>
  <li><div><b>Get paid every Monday</b><p>Last week's rebate on your BingX futures fees arrives in USDT. The minimum payout is 10 USDT; smaller amounts roll over to the next week.</p></div></li>
</ol>
<p class="src">UID steps from <a href="{B_UID}" target="_blank" rel="noopener">BingX Tutorial: How to Find My UID?</a>, checked 25 Nov 2026. More on the account: <a href="../exchanges/bingx.html">BingX referral page</a>.</p>

<div class="gd-risk">
  <h2>Before you trade</h2>
  <p>Leveraged futures can lose you money quickly and can wipe out your whole margin. A lower fee or a rebate reduces your costs; it does not make a losing strategy profitable, and it is not income. Start with low leverage and only trade money you can afford to lose.</p>
  <p style="margin-top:12px">BingX decides which countries it serves, so check its terms for where you live. This site is not for residents of the Republic of Korea or the United States, or of any place where the exchange is not allowed to serve you. Nothing here is investment advice. {config['brand']} earns a referral commission from BingX and shares part of it with you as the rebate.</p>
</div>
"""
    faqs11 = [
        ("What are BingX's futures trading fees?",
         f"BingX's fee schedule for perpetual futures lists {pct(B_MAKER)} for maker orders and {pct(B_TAKER)} for taker orders, checked 25 November 2026. The fee is charged on the position value when you open and again when you close. VIP users can get a discount, and the rate shown in your logged-in account always applies."),
        ("How do I get a discount on BingX futures fees?",
         f"Use limit orders that rest on the book to pay the maker rate instead of the taker rate, reach a VIP level, or open a new account through a fee-rebate partner. Through {config['brand']}, {r11}% of the BingX futures fees you pay comes back in USDT every Monday, which brings the effective taker rate to {pct(net(B_TAKER, r11))}."),
        ("Is the BingX funding fee covered by the rebate?",
         "No. Funding is paid between long and short holders, settled at 00:00, 08:00 and 16:00 UTC+8 on open positions, and it does not go to BingX as a trading fee. Only trading fees are rebated."),
    ]
    out.append(dict(
        slug="bingx-futures-fees",
        venue=bg,
        title=f"BingX Futures Fees 2026: Maker, Taker, Funding & a {r11}% Rebate | {config['brand']}",
        h1="BingX futures fees, <em>in plain dollars.</em>",
        crumb="BingX futures fees",
        desc=(f"BingX futures fees are {pct(B_MAKER)} maker / {pct(B_TAKER)} taker. What a trade and a month cost, "
              f"how funding works, and how a {r11}% rebate cuts taker to {pct(net(B_TAKER, r11))}."),
        lede=(f"{pct(B_MAKER)} maker and {pct(B_TAKER)} taker, charged on the whole position, twice per trade. "
              f"Here is what that comes to in a normal month, where funding fits, and how to get {r11}% of it back."),
        published="2026-11-25", modified="2026-11-25", checked="25 Nov 2026",
        keyword="bingx futures fees",
        body=body11, faqs=faqs11, signup=signup11,
        side_big=pct(net(B_TAKER, r11)), side_label=f"BingX taker you effectively pay after the {r11}% rebate (standard {pct(B_TAKER)})",
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
                {"@type": "ListItem", "position": 2, "name": "Guides", "item": f"{config['domain']}/guides/"},
                {"@type": "ListItem", "position": 3, "name": g["crumb"], "item": canonical}]},
        ]
        ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
        v = g["venue"]
        hd = head(g["title"], g["desc"], canonical, ld_html).replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">', 1)
        hd = hd.replace(f"{config['domain']}/assets/og.png", f"{config['domain']}/assets/og/{g['slug']}.png")
        page = hd + f"""<style>{CSS}</style><!--BODY-->{header('../')}
<main>
  <div class="wrap"><nav class="crumbs" aria-label="Breadcrumb" style="font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding-block:18px"><a href="../index.html" style="text-decoration:none">{config['brand']}</a> / <a href="./" style="text-decoration:none">Guides</a> / {esc(g['crumb'])}</nav></div>
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
        <a href="../tools/futures-fee-calculator.html">Fee calculator: your monthly cost</a>
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


HUB_CSS = """
.gh-list{list-style:none;margin:0;padding:0;border-top:1px solid var(--ink);counter-reset:g}
.gh-list li{counter-increment:g;border-bottom:1px solid var(--hair)}
.gh-list a{display:grid;grid-template-columns:56px minmax(0,1fr) auto;gap:6px 18px;align-items:baseline;padding-block:26px;text-decoration:none;color:inherit}
.gh-list a::before{content:counter(g,upper-roman);font-family:var(--display);font-style:italic;font-size:24px;color:var(--tone);line-height:1.2}
.gh-list h2{font-size:clamp(24px,3vw,34px);line-height:1.12;margin:0;grid-column:2}
.gh-list p{grid-column:2;margin:6px 0 0;font-size:16px;font-weight:300;line-height:1.6;color:var(--muted);max-width:62ch}
.gh-list .when{grid-column:3;grid-row:1;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
.gh-list a:hover h2{text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
@media (max-width:640px){.gh-list a{grid-template-columns:40px minmax(0,1fr)}.gh-list .when{grid-column:2;grid-row:auto;margin-top:8px}}
.gh-tools{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px 40px;margin-top:56px}
"""


def build_hub(head, header, footer, esc, common_js, config, fab, venues, pct, net, link, tg_dm):
    """guides/index.html — one crawlable index of every guide (newest first) + the calculator. 2026-11-18 strategy meeting."""
    V = {v["slug"]: v for v in venues}
    gs = sorted(_guides(V, pct, net, link, config, tg_dm), key=lambda g: g["published"], reverse=True)
    canonical = f"{config['domain']}/guides/"
    title = f"Crypto Futures Fee Guides: Maker/Taker, Funding, Rebates | {config['brand']}"
    desc = ("Plain-English guides to what crypto futures trading really costs: maker vs taker fees, funding, "
            "break-even price, scalping costs and how fee rebates work, with dollar examples.")
    import datetime as _dt
    def _d(iso):
        d = _dt.date.fromisoformat(iso); return f"{d.day} {d.strftime('%b')} {d.year}"
    ld = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Crypto futures fee guides", "description": desc, "url": canonical,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": f"{config['domain']}/guides/{g['slug']}.html", "name": g["h1"].replace("<em>", "").replace("</em>", "")}
             for i, g in enumerate(gs)]}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": config["brand"], "item": config["domain"] + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": canonical}]},
    ]
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    items = "".join(
        f'<li><a href="{g["slug"]}.html"><h2>{esc(g["h1"].replace("<em>", "").replace("</em>", ""))}</h2>'
        f'<span class="when">{_d(g["published"])}</span><p>{esc(g["desc"])}</p></a></li>' for g in gs)
    hd = head(title, desc, canonical, ld_html).replace(f"{config['domain']}/assets/og.png", f"{config['domain']}/assets/og/guides.png")
    page = hd + f"""<style>{CSS}{HUB_CSS}</style><!--BODY-->{header('../')}
<main>
  <div class="wrap"><nav class="crumbs" aria-label="Breadcrumb" style="font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding-block:18px"><a href="../index.html" style="text-decoration:none">{config['brand']}</a> / Guides</nav></div>
  <section class="gd-hero"><div class="wrap">
    <span class="label">Guides · {len(gs)} so far</span>
    <h1>What futures trading <em>really</em> costs.</h1>
    <p class="lede">Fees are the one cost of trading you can see before you place the order. These guides work through it in dollars: maker or taker, funding, where you break even, and what a rebate gives back. Every fee number is checked on the exchange's own page, with the date in the text.</p>
  </div></section>
  <div class="wrap" style="padding-block:clamp(40px,6vw,80px)">
    <ol class="gh-list">{items}</ol>
    <div class="gh-tools">
      <div class="gd-card"><span class="label">Tool</span><a href="../tools/futures-fee-calculator.html">Futures fee calculator: your monthly cost on 9 exchanges, before and after rebate</a></div>
      <div class="gd-card"><span class="label">Compare</span><a href="../index.html#venues">All exchanges ranked by fee after rebate</a></div>
    </div>
    <p class="fine" style="margin-top:40px;color:var(--muted)">Education only, not financial advice. Not for residents of Korea or the US.</p>
  </div>
</main>
{footer('../')}
{fab}
<script>window.HOME="../index.html"; window.LANG="en";
{common_js}
btcPill();</script>"""
    return page, canonical
