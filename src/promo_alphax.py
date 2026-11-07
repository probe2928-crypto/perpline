"""Perpline · AlphaX special (promos/alphax.html) + the slim promo strip used on index.html and start.html.
Facts checked 5 Nov 2026 on AlphaX's Rewards Hub and its 15 Jul 2026 zero-fee press release. Use only those facts:
every reward on this page is a trading/position VOUCHER, not cash, and the zero-fee offer is limited-time and regional.
The sign-up link is Sejun's own AlphaX invite. AlphaX is not in VENUES (no Perpline fee rebate), so the growth kit's
'claim your rebate' bar never shows for it."""

REF = "https://www.alphax.com/partner/7lxP6X"
HUB = "https://www.alphax.com/en-us/activity/reward-center"
PR = "https://beincrypto.com/alphax-rolls-out-global-zero-fee-trading/"
CHECKED = "5 Nov 2026"
SLUG = "promos/alphax.html"
REL = 'target="_blank" rel="sponsored nofollow noopener"'

CSS = """
.px-hero{position:relative;overflow:hidden;background:var(--t2);border-bottom:1px solid var(--hair)}
.px-hero > .fx{position:absolute;inset:0;width:100%;height:100%;display:block;pointer-events:none;opacity:.7}
.px-hero .wrap{position:relative;z-index:1;padding-block:clamp(40px,5vw,72px) clamp(40px,6vw,72px);display:flex;flex-direction:column;gap:24px;align-items:flex-start}
.px-tag{display:inline-flex;align-items:center;gap:10px;font-size:11.5px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--tone)}
.px-tag i{font-style:normal;background:var(--tone);color:var(--tone-ink);padding:5px 10px;letter-spacing:.18em}
.px-hero h1{font-size:clamp(44px,5.4vw,78px);max-width:21ch}
.px-hero h1 em{color:var(--tone)}
.px-figs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));width:100%;border-top:1px solid var(--ink);border-bottom:1px solid var(--hair)}
.px-figs div{padding:22px 18px 22px 0;display:flex;flex-direction:column;gap:8px}
.px-figs div + div{padding-left:22px;border-left:1px solid var(--hair)}
.px-figs b{font-family:var(--display);font-weight:400;font-size:clamp(40px,4.6vw,64px);line-height:.9;color:var(--tone);font-variant-numeric:lining-nums}
.px-figs b small{font-size:.38em;margin-left:4px;color:var(--ink)}
.px-figs span{font-size:13.5px;color:var(--muted);line-height:1.45}
.px-figs span strong{color:var(--ink);font-weight:500}
.px-cta{display:flex;flex-wrap:wrap;gap:14px 22px;align-items:center}
.px-cta .btn{min-height:56px;padding-inline:34px;font-size:13px}
.px-cta .alt{font-size:14px;text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:1px}
.px-honest{font-size:14px;color:var(--ink);max-width:62ch;border-left:2px solid var(--tone);padding:2px 0 2px 12px}
.px-honest b{font-weight:500}
.px-kr{font-size:12.5px;letter-spacing:.08em;color:var(--muted)}
.px-sec{padding-block:clamp(56px,8vw,104px);border-bottom:1px solid var(--hair)}
.px-sec.a{background:var(--t1)} .px-sec.b{background:var(--t3)} .px-sec.c{background:var(--t4)} .px-sec.d{background:var(--t5)}
.px-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px 56px;align-items:end;margin-bottom:40px}
.px-head .label{display:block;margin-bottom:14px}
.px-head h2{font-size:clamp(34px,4.6vw,60px)}
.px-head p{color:var(--muted);font-weight:300;max-width:52ch}
@media (max-width:820px){.px-head{grid-template-columns:1fr}}
.px-tbl{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;border-top:1px solid var(--ink)}
.px-tbl th,.px-tbl td{text-align:left;padding:18px 14px 18px 0;border-bottom:1px solid var(--hair);vertical-align:top}
.px-tbl thead th{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:500;padding-block:12px}
.px-tbl td.t{font-family:var(--display);font-size:clamp(20px,2vw,26px);line-height:1.15}
.px-tbl td.c{color:var(--muted);font-weight:300;font-size:15.5px}
.px-tbl td.r,.px-tbl th.r{text-align:right;padding-right:0;white-space:nowrap}
.px-tbl td.r b{font-family:var(--display);font-weight:400;font-size:30px;color:var(--tone);line-height:1}
.px-tbl td.r small{display:block;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-top:6px}
.px-tbl tr.tot td{border-bottom:1px solid var(--ink);font-weight:500}
.px-tbl tr.tot td.r b{font-size:40px}
@media (max-width:640px){
 .px-tbl thead{display:none}
 .px-tbl tr{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 14px;padding-block:16px;border-bottom:1px solid var(--hair)}
 .px-tbl tr.tot{border-bottom:1px solid var(--ink)}
 .px-tbl td,.px-tbl tr.tot td{padding:0;border:0}
 .px-tbl td.t{grid-column:1}.px-tbl td.r{grid-column:2;grid-row:1 / span 2;align-self:start}.px-tbl td.c{grid-column:1;font-size:14.5px}
}
.px-duo{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;margin-top:48px;border-top:1px solid var(--ink)}
.px-duo article{padding:30px 32px 6px 0;display:flex;flex-direction:column;gap:14px}
.px-duo article + article{padding-left:32px;border-left:1px solid var(--hair)}
.px-duo h3{font-size:clamp(24px,2.4vw,30px)}
.px-duo .big{font-family:var(--display);font-size:clamp(52px,6vw,80px);line-height:.85;color:var(--tone);font-variant-numeric:lining-nums}
.px-duo .big small{font-size:.32em;color:var(--ink);margin-left:6px}
.px-duo p{color:var(--muted);font-weight:300;font-size:15.5px}
.px-tiers{display:flex;flex-wrap:wrap;gap:8px}
.px-tiers span{font-size:13px;border:1px solid var(--hair);background:var(--paper);padding:6px 10px;font-variant-numeric:tabular-nums}
@media (max-width:820px){.px-duo{grid-template-columns:1fr}.px-duo article{padding-right:0}.px-duo article + article{padding-left:0;border-left:0;border-top:1px solid var(--hair);margin-top:24px}}
.px-fee{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(28px,5vw,72px);align-items:center}
@media (max-width:860px){.px-fee{grid-template-columns:1fr}}
.px-fee .zero{font-family:var(--display);font-size:clamp(120px,18vw,240px);line-height:.8;color:var(--tone);letter-spacing:-.03em}
.px-fee .zero small{font-size:.3em;color:var(--ink);font-style:italic;margin-left:8px}
.px-fee p{font-size:18px;font-weight:300;line-height:1.7}
.px-fee p + p{margin-top:14px}
.px-fee .src{font-size:13.5px;color:var(--muted)}
.px-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--ink)}
.px-steps li{padding:26px 24px 28px 0;display:flex;flex-direction:column;gap:10px}
.px-steps li + li{padding-left:24px;border-left:1px solid var(--hair)}
.px-steps .n{font-family:var(--display);font-style:italic;font-size:44px;line-height:1;color:var(--tone)}
.px-steps b{font-weight:500}
.px-steps p{color:var(--muted);font-weight:300;font-size:15.5px}
@media (max-width:900px){.px-steps{grid-template-columns:1fr}.px-steps li{padding-right:0}.px-steps li + li{padding-left:0;border-left:0;border-top:1px solid var(--hair)}}
.px-fine{margin:0;padding:0 0 0 1.2em;display:grid;gap:12px;max-width:78ch;font-weight:300;line-height:1.65}
.px-fine b{font-weight:500}
.px-risk{margin-top:44px;padding:26px 28px;border:1px solid var(--ink);background:var(--paper);display:grid;gap:12px;max-width:860px}
.px-risk h3{font-size:26px}
.px-risk p{font-size:15.5px;font-weight:300}
.px-risk p b{font-weight:500}
.px-risk .kr{color:var(--down);font-weight:500}
.px-end{background:var(--tone);color:var(--tone-ink);padding-block:clamp(56px,8vw,96px)}
.px-end .wrap{display:flex;flex-direction:column;gap:20px;align-items:flex-start}
.px-end h2{font-size:clamp(36px,5vw,64px);max-width:18ch}
.px-end p{opacity:.85;max-width:56ch;font-weight:300}
.px-end .btn{background:var(--tone-ink);border-color:var(--tone-ink);color:var(--tone);min-height:56px;padding-inline:34px;font-size:13px}
.px-end .btn:hover{background:transparent;color:var(--tone-ink)}
.px-end .fine{color:var(--tone-ink);opacity:.75}
@media (max-width:640px){
 .px-hero .wrap{padding-block:30px 36px;gap:18px}
 .px-hero h1{font-size:36px}
 .px-hero .lede{font-size:15.5px}
 .px-figs{grid-template-columns:1fr 1fr}
 .px-figs div{padding:16px 10px 16px 0}
 .px-figs div + div{padding-left:14px}
 .px-figs div:nth-child(3){grid-column:1 / -1;padding-left:0;border-left:0;border-top:1px solid var(--hair)}
 .px-figs b{font-size:46px}
 .px-cta{width:100%;flex-direction:column;align-items:stretch}
 .px-cta .btn{width:100%;justify-content:center;font-size:15px;letter-spacing:.04em;text-transform:none}
 .px-cta .alt{align-self:center}
 .px-end .btn{width:100%;font-size:15px;letter-spacing:.04em;text-transform:none}
 .px-risk{padding:20px}
}
"""

STRIP_CSS = """<style>
.px-strip{display:block;background:var(--t2);color:var(--ink);text-decoration:none;border-bottom:1px solid var(--hair)}
.px-strip .wrap{display:flex;align-items:center;justify-content:center;gap:10px 16px;flex-wrap:wrap;padding-block:11px;text-align:center}
.px-strip i{font-style:normal;font-size:10.5px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;background:var(--tone);color:var(--tone-ink);padding:4px 9px}
.px-strip span{font-size:14px;letter-spacing:.02em}
.px-strip span b{font-family:var(--display);font-weight:400;font-size:18px;color:var(--tone);letter-spacing:0}
.px-strip u{font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:1px;white-space:nowrap}
.px-strip s{text-decoration:none}
.px-strip:hover u{color:var(--tone)}
@media (max-width:640px){.px-strip .wrap{flex-wrap:nowrap;gap:10px;padding-block:8px;justify-content:flex-start;text-align:left}.px-strip s{display:none}.px-strip i{flex:none;font-size:9.5px;padding:3px 6px;letter-spacing:.14em}.px-strip span{font-size:12px;line-height:1.35;flex:1 1 auto;min-width:0}.px-strip span b{font-size:14px}.px-strip u{flex:none;font-size:10.5px;letter-spacing:.14em}}
</style>"""


def promo_strip(domain, place):
    """Slim strip that opens AlphaX sign-up directly with referral code 7lxP6X (Sejun 2026-11-05: every AlphaX link goes straight to sign-up)."""
    return (STRIP_CSS + f'<a class="px-strip" href="{REF}" target="_blank" rel="sponsored nofollow noopener" data-place="{place}">'
            '<div class="wrap"><i>AlphaX<s> special</s></i>'
            '<span><b>0%</b> maker/taker · up to <b>15,000+ USDT</b> in welcome vouchers</span>'
            '<u>Sign up<s> · code 7lxP6X</s></u></div></a>')


def build_promo(head, header, footer, esc, common_js, config, fab, tg_dm, fx_js=""):
    pre = config["domain"] + "/"
    canonical = pre + SLUG
    btn = lambda label, cls="btn tone", place="": f'<a class="{cls}" href="{REF}" {REL}>{esc(label)}</a>'
    tasks = [
        ("Register and bind your phone", "Create a new AlphaX account and bind a phone number.", 200),
        ("First deposit", "Make your first on-chain deposit of at least 50 USDT.", 50),
        ("First futures trade", "Place any futures trade over 1 USDT. The position must stay open for at least 1 minute.", 200),
        ("Bind X, follow and share", "Link your X account, follow AlphaX and share the post the task asks for.", 100),
    ]
    rows = "".join(f'<tr><td class="t">{esc(t)}</td><td class="c">{esc(c)}</td><td class="r"><b class="num">{a}</b><small>USDT in vouchers</small></td></tr>'
                   for t, c, a in tasks)
    rows += ('<tr class="tot"><td class="t">New-user tasks, all four</td><td class="c">Within 14 days of sign-up, once per account.</td>'
             f'<td class="r"><b class="num">{sum(a for *_, a in tasks)}</b><small>USDT in vouchers</small></td></tr>')
    dep = "".join(f"<span>{t} USDT</span>" for t in ("100", "500", "3,000", "5,000", "10,000"))
    pnl = "".join(f"<span>{t} USDT</span>" for t in ("10", "50", "100", "500", "1,000", "3,000"))
    fine = [
        ("Vouchers, not cash.", "Every reward on this page is a trading or position voucher credited by AlphaX. It is not cash. How a voucher can be used, and how much of any result can be withdrawn, follow the rules of each task on AlphaX."),
        ("New users only.", "The new-user tasks are for new AlphaX accounts, must be completed within 14 days of sign-up, and can be claimed once per account."),
        ("On-chain deposits only.", "Only on-chain deposits count toward the deposit tasks and the cumulative deposit tiers."),
        ("Futures positions.", "A futures position must be held for at least 1 minute to count."),
        ("Payout timing.", "AlphaX says rewards are paid within up to 3 business days."),
        ("Zero fees.", "0% maker and 0% taker fees apply for a limited time and only in eligible regions. Check AlphaX's fee page before you trade."),
        ("AlphaX's rules apply.", f'AlphaX runs and pays these rewards under its own terms, which it can change or end. Read the current rules in the <a href="{HUB}" target="_blank" rel="noopener">AlphaX Rewards Hub</a>. {esc(config["brand"])} does not pay or guarantee them.'),
    ]
    fine_html = "".join(f"<li><b>{esc(k)}</b> {v}</li>" for k, v in fine)
    title = f"AlphaX Special: 0% Maker/Taker Fees + Up to 15,000+ USDT Welcome Rewards (Vouchers) | {config['brand']}"
    desc = ("AlphaX special on Perpline: 0% maker/taker fees for a limited time in eligible regions, and up to 15,000+ USDT in welcome "
            "rewards paid as trading vouchers, not cash. Tasks, conditions and how to claim.")
    og = pre + "ads/alphax/linkedin-1200x627.png"
    hd = head(title, desc, canonical).replace(f'content="{pre}assets/og.png"', f'content="{og}"')
    body = f"""<style>{CSS}</style><!--BODY-->{header('../')}
<main>
  <section class="px-hero" aria-labelledby="pxH">
    <canvas class="fx" data-fx="silk" aria-hidden="true"></canvas>
    <div class="wrap">
      <span class="px-tag"><i>Special</i> {esc(config['brand'])} × AlphaX</span>
      <h1 id="pxH">AlphaX special: <em>0% fees</em> and up to 15,000+ USDT in welcome vouchers.</h1>
      <p class="lede">Open a new AlphaX account through {esc(config['brand'])}, finish a few simple tasks in the AlphaX Rewards Hub and collect trading vouchers. Fees are 0% for makers and takers for a limited time in eligible regions.</p>
      <div class="px-figs">
        <div><b class="num">0%</b><span><strong>Maker fee</strong> · limited time, eligible regions</span></div>
        <div><b class="num">0%</b><span><strong>Taker fee</strong> · limited time, eligible regions</span></div>
        <div><b class="num">15,000+<small>USDT</small></b><span><strong>Welcome rewards, in vouchers, not cash.</strong> New-user tasks alone: up to 550 USDT in vouchers.</span></div>
      </div>
      <div class="px-cta" data-place="promo-hero">{btn("Claim on AlphaX")}<a class="alt" href="#get">See every task</a></div>
      <p class="px-honest"><b>Read this first:</b> the rewards are trading and position vouchers, not cash. What you can withdraw, and how vouchers can be used, follow each task's rules on AlphaX.</p>
      <p class="px-kr">Not for residents of the Republic of Korea or the United States · 18+ · Terms checked {CHECKED}</p>
    </div>
  </section>

  <section class="px-sec a" id="get" aria-labelledby="getH">
    <div class="wrap">
      <div class="px-head"><div><span class="label">What you get</span><h2 id="getH">Four tasks, <em>up to 550 USDT</em> in vouchers.</h2></div>
        <p>AlphaX's Rewards Hub headline is "Welcome Rewards 15,000+ USDT". The new-user tasks below add up to 550 USDT, paid in vouchers, not cash. Two bigger programmes sit on top of them.</p></div>
      <table class="px-tbl">
        <thead><tr><th>Task</th><th>Condition</th><th class="r">Reward</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <div class="px-duo">
        <article>
          <span class="label">Deposit More, Earn More</span>
          <b class="big num">18,600<small>USDT</small></b>
          <h3>Up to 18,600 USDT in position vouchers.</h3>
          <p>Unlocked by your cumulative on-chain deposits. In vouchers, not cash. Deposit tiers:</p>
          <div class="px-tiers">{dep}</div>
        </article>
        <article>
          <span class="label">Futures |PNL| Challenge</span>
          <b class="big num">4,660<small>USDT</small></b>
          <h3>Up to 4,660 USDT in position vouchers.</h3>
          <p>Unlocked by your futures profit. In vouchers, not cash. Profit tiers:</p>
          <div class="px-tiers">{pnl}</div>
        </article>
      </div>
      <div class="px-cta" style="margin-top:44px" data-place="promo-tasks">{btn("Claim on AlphaX")}<a class="alt" href="{HUB}" target="_blank" rel="noopener">Open the AlphaX Rewards Hub</a></div>
    </div>
  </section>

  <section class="px-sec b" id="fees" aria-labelledby="feeH">
    <div class="wrap px-fee">
      <div class="zero num">0%<small>fees</small></div>
      <div>
        <span class="label">Zero-fee trading</span>
        <h2 id="feeH" style="font-size:clamp(30px,3.6vw,46px);margin:14px 0 20px">0% maker / 0% taker, for a limited time.</h2>
        <p>AlphaX announced a limited-time zero-fee initiative for makers and takers in eligible regions, covering crypto spot, crypto futures and TradFi perpetuals.</p>
        <p><b>0% maker / 0% taker fees for a limited time in eligible regions — check AlphaX's fee page before you trade.</b></p>
        <p class="src">Source: AlphaX press release, 15 July 2026, via <a href="{PR}" target="_blank" rel="noopener">BeInCrypto</a>.</p>
      </div>
    </div>
  </section>

  <section class="px-sec c" id="how" aria-labelledby="howH">
    <div class="wrap">
      <div class="px-head"><div><span class="label">How to claim</span><h2 id="howH">Four steps, <em>14 days.</em></h2></div>
        <p>The clock starts when you sign up. Finish the new-user tasks within 14 days.</p></div>
      <ol class="px-steps">
        <li><span class="n">1</span><b>Open a new AlphaX account</b><p>Use a Claim on AlphaX button on this page. Sign up with your email; the invite is already in the link.</p></li>
        <li><span class="n">2</span><b>Bind your phone</b><p>Bind a phone number and open the Rewards Hub to see your tasks and deadline.</p></li>
        <li><span class="n">3</span><b>Deposit and trade</b><p>Make an on-chain deposit of at least 50 USDT, then a futures trade over 1 USDT held for at least 1 minute. Check the fee page first.</p></li>
        <li><span class="n">4</span><b>Collect your vouchers</b><p>AlphaX credits them within up to 3 business days. They are vouchers, not cash; use and withdrawal follow each task's rules.</p></li>
      </ol>
      <div class="px-cta" style="margin-top:40px" data-place="promo-steps">{btn("Claim on AlphaX")}</div>
    </div>
  </section>

  <section class="px-sec d" id="fine" aria-labelledby="fineH">
    <div class="wrap">
      <div class="px-head"><div><span class="label">Fine print</span><h2 id="fineH">Conditions, <em>in plain words.</em></h2></div>
        <p>Summarised from the AlphaX Rewards Hub on {CHECKED}. If anything here differs from AlphaX's own page, AlphaX's page applies.</p></div>
      <ul class="px-fine">{fine_html}</ul>
      <div class="px-risk" role="note" aria-labelledby="riskH">
        <h3 id="riskH">Before you trade</h3>
        <p><b>Leveraged trading can lose you all of your margin</b>, quickly. Vouchers lower your costs or add trading size; they are not cash and they do not make a losing trade profitable. Only trade money you can afford to lose. Nothing here is financial advice.</p>
        <p class="kr">Not for residents of the Republic of Korea or the United States.</p>
        <p>AlphaX decides which countries it serves and which regions get zero fees; check its terms for where you live. {esc(config['brand'])} earns a referral commission when you sign up through the links on this page.</p>
      </div>
    </div>
  </section>

  <section class="px-end" aria-labelledby="endH">
    <div class="wrap">
      <span class="label" style="color:inherit;opacity:.8">AlphaX special</span>
      <h2 id="endH">0% fees and up to 15,000+ USDT in welcome vouchers.</h2>
      <p>Vouchers, not cash. Zero fees for a limited time in eligible regions. New accounts only, tasks within 14 days.</p>
      <div data-place="promo-end">{btn("Claim on AlphaX", "btn")}</div>
      <p class="fine">Referral link · {esc(config['brand'])} earns a commission · Not for KR / US residents · 18+</p>
    </div>
  </section>
</main>
{footer('../')}
{fab}
<script>window.HOME="../index.html"; window.LANG="en";
{common_js}
{fx_js}
btcPill();</script>"""
    return hd + body, canonical
