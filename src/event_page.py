"""Perpline · Monthly member draw — official rules page (event/index.html).
Plan, legal and tax notes: chainbrief ops/events/PLAN.md. Visibility is controlled by event/event-config.js (enabled:false = the page
only says there is no draw running). Update ROUND each month; bump RULES_VERSION (and versions.rules in event-config.js) when rules change."""

RULES_VERSION = "2026-11-02"
ROUND = {
    "id": "pl-2026-12", "month": "December 2026",
    "period": "1 December 2026, 00:00 to 31 December 2026, 23:59 (KST, UTC+9)",
    "draw": "the first Bitcoin block mined after 21:00 KST on 4 January 2027",
    "announce": "5 January 2027",
    "claim": "14 days after notice (by 19 January 2027)",
}

CSS = """
[data-event-hide] [data-event-main]{visibility:hidden}
.ev-hero{padding-block:clamp(56px,8vw,104px) clamp(32px,4vw,48px)}
.ev-hero h1{font-size:clamp(44px,6.4vw,88px);max-width:12ch}
.ev-hero .lede{margin-top:22px}
.ev-top{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(28px,5vw,64px);align-items:start;padding-bottom:clamp(56px,7vw,96px)}
@media (max-width:860px){.ev-top{grid-template-columns:1fr}}
.ev-spec{margin:0;border-top:1px solid var(--ink)}
.ev-spec div{display:grid;grid-template-columns:8.5em 1fr;gap:4px 18px;padding:16px 0;border-bottom:1px solid var(--hair)}
.ev-spec dt{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding-top:3px}
.ev-spec dd{margin:0;font-weight:500;line-height:1.45}
.ev-spec dd small{display:block;font-weight:300;color:var(--muted);font-size:14px;margin-top:3px}
.ev-rules{border-top:1px solid var(--hair);padding-block:clamp(56px,7vw,96px)}
.ev-rules h2{font-size:clamp(34px,4vw,52px);margin-bottom:28px}
.ev-rules ol{margin:0;padding-left:1.3em;display:grid;gap:14px;max-width:70ch;font-weight:300;line-height:1.7}
.ev-rules ol b{font-weight:500}
.ev-rules a{text-decoration:underline;text-underline-offset:3px}
.ev-rules .fine{margin-top:32px;font-size:13px;color:var(--muted);max-width:70ch}
@media (max-width:560px){.ev-spec div{grid-template-columns:1fr}}
"""


def build_event(head, header, footer, esc, common_js, config, tg_dm, fab):
    r = ROUND
    pre = config["domain"] + "/"
    spec = [
        ("Prize", "20 USDT each", "or the same value in SOL or ETH, winner's choice"),
        ("Winners", "3 every month", "one entry per person, random public draw"),
        ("Entry period", r["period"], "a new round opens on the 1st of each month"),
        ("Draw", "Block-hash draw", "seeded by " + r["draw"]),
        ("Cost", "Free", "no deposit, trade or purchase needed"),
    ]
    spec_html = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}<small>{esc(s)}</small></dd></div>" for k, v, s in spec)
    rules = [
        ("Sponsor", f"{config['brand']} (operated from the Republic of Korea). This draw is not run, endorsed or funded by any exchange or token issuer."),
        ("Who can enter", "Signed-in Perpline members aged 18 or over (or the age of majority where they live) who live in one of the countries listed in the entry form. "
         "Residents of the Republic of Korea, the United States, Quebec and any country not listed cannot enter. Void where prohibited. Perpline staff and their families cannot enter."),
        ("How to enter", "Sign in and press Enter on this page. One entry per person and per account each round. No purchase, deposit, trade, referral sign-up or social share is required, "
         "and opting in to marketing email has no effect on your chances."),
        ("Prize", "Each winner receives 20 USDT, or SOL or ETH worth 20 USDT at the payout-day price. Prizes cannot be exchanged for cash or other assets. Approximate value: USD 20 each, USD 60 per round."),
        ("Draw", f"For every entry we compute SHA-256(seed:entry number), where the seed is the hash of {esc(r['draw'])}. The three lowest values win. "
         "We publish the seed and the total number of entries so anyone can check the result. Accounts that won in the last 90 days are skipped."),
        ("Winners", f"Announced on {esc(r['announce'])} on this page (partly hidden email, e.g. ab***@g***.com) and by email to each winner. This email is about the draw you entered."),
        ("Claiming", f"Winners sign in within {esc(r['claim'])} and give the coin, network, wallet address and receiving exchange. Residents of Canada must also answer a short maths question. "
         "We send the prize within 7 days. Unclaimed prizes are forfeited and not redrawn."),
        ("Fair play", "Only email-verified accounts can enter. Multiple accounts (including email aliases), disposable email, automated entries or a wallet already used by another winner void the entry and any prize."),
        ("Taxes", "Winners are responsible for any tax in their own country. If Korean law requires tax reporting or withholding on a prize, we may ask the winner for their legal name and ID number before paying."),
        ("Transfers", "Coins sent to an address or network the winner entered incorrectly cannot be recovered. We pay the network fee."),
        ("Changes", "If we must change or stop the draw we will post it here first; rounds already entered follow the rules in force when they opened."),
        ("Contact", f'<a href="{tg_dm}" target="_blank" rel="noopener">@{esc(config["telegram_dm"])}</a> on Telegram.'),
    ]
    rules_html = "".join(f"<li><b>{esc(k)}.</b> {v}</li>" for k, v in rules)
    body = f"""<!--BODY-->{header(pre)}<main data-event-main>
<section class="ev-hero"><div class="wrap">
  <h1>Twenty USDT, three winners, every month.</h1>
  <p class="lede">Perpline members can enter one free draw each month. No deposit, no trading, no purchase. Winners choose USDT, SOL or ETH.</p>
</div></section>
<div class="wrap ev-top">
  <dl class="ev-spec">{spec_html}</dl>
  <div data-event-entry></div>
</div>
<section class="ev-rules" id="rules" aria-labelledby="rulesH"><div class="wrap">
  <h2 id="rulesH">Official rules</h2>
  <ol>{rules_html}</ol>
  <p class="fine">Entry data (account email already on file, country, entry time) is used only for this draw, shared with no one and deleted 30 days after the winners are announced;
  winners' claim details are deleted 30 days after payout, keeping only the transaction hash, amount and date. Rules version {RULES_VERSION}.</p>
</div></section>
</main>{footer(pre)}{fab}<script>{common_js}btcPill();</script>"""
    title = f"Monthly member draw · Official rules | {config['brand']}"
    return head(title, "Perpline members can enter one free monthly draw for 20 USDT. Official rules.", pre + "event/") + f"<style>{CSS}</style>" + body
