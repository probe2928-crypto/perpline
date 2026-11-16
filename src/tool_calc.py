"""Perpline · Tools — /tools/futures-fee-calculator.html (2026-11-16 전략 회의 결정 1).
홈 #fees 계산기와 같은 공식(포지션 × 요율 × 2 × 왕복 수, 리베이트 반영)을 검색용 독립 페이지로.
숫자는 전부 VENUES에서 온다(새로 만든 숫자 없음). 홈·start.html은 건드리지 않는다(E1·E2 실험 중).
레퍼럴 코드는 화면에 쓰지 않는다(FEEDBACK 10/29) — 가입은 link()로만."""
import json

SLUG = "tools/futures-fee-calculator.html"


def build_tool_calc(head, header, footer, esc, common_js, config, fab, venues, ranked, net, pct, link, tg_dm):
    rk = ranked(venues)
    known = [v for v in rk if v["taker"] is not None]
    js_venues = json.dumps([{k: v[k] for k in ("name", "maker", "taker", "rebate")} for v in known])
    # cheapest after rebate (taker) — 정적 표, 같은 VENUES 숫자
    by_net = sorted(known, key=lambda v: (net(v["taker"], v["rebate"]), v["taker"]))
    rows = "".join(
        f'<li class="tc-row"><span class="tc-n">{i + 1:02d}</span><a class="tc-name" href="../exchanges/{v["slug"]}.html">{esc(v["name"])}</a>'
        f'<span class="tc-f"><span class="label">Taker</span><b class="num">{pct(v["taker"])}</b></span>'
        f'<span class="tc-f"><span class="label">Rebate</span><b class="num">{v["rebate"]}%</b></span>'
        f'<span class="tc-f"><span class="label">You pay</span><b class="num">{pct(net(v["taker"], v["rebate"]))}</b></span>'
        f'<a class="btn line tc-go" href="{esc(link(v, "tool-calc"))}" target="_blank" rel="sponsored nofollow noopener">Sign up</a></li>'
        for i, v in enumerate(by_net[:5]))
    canonical = f"{config['domain']}/{SLUG}"
    title = f"Crypto Futures Fee Calculator — Compare {len(known)} Exchanges After Rebate | {config['brand']}"
    desc = (f"Enter your position size and trades per month to see what futures fees cost on {len(known)} exchanges, "
            "before and after a fee rebate. Market or limit orders. Funding not included.")
    faqs = [
        ("How are futures trading fees calculated?",
         "The fee is your position size (margin times leverage) multiplied by the exchange's fee rate. You pay it once when you open and again when you close, so one round trip costs about twice the rate on the full position."),
        ("Why does leverage make fees bigger?",
         "Fees are charged on the position, not on your margin. 1,000 USDT of margin at 10x is a 10,000 USDT position, and the fee is taken on 10,000."),
        ("Market or limit order: which rate applies?",
         "A market order takes liquidity and pays the taker rate. A resting limit order that gets filled adds liquidity and usually pays the lower maker rate."),
        ("What does the rebate column mean?",
         f"When you sign up through a {config['brand']} link, part of the referral commission is paid back to you in USDT. The calculator subtracts that share from the fee. Rebates are paid by {config['brand']}, not by the exchange."),
        ("Does this include funding fees?",
         "No. Funding is paid between traders every few hours and depends on the market, so it is left out. See the funding guide for how it works."),
    ]
    ld = [
        {"@context": "https://schema.org", "@type": "WebApplication", "name": "Crypto futures fee calculator",
         "url": canonical, "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@type": "Organization", "name": config["brand"]}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": config["brand"], "item": config["domain"] + "/"},
            {"@type": "ListItem", "position": 2, "name": "Futures fee calculator", "item": canonical}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
    ]
    extra = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    css = """<style>
.tc-hero{padding-block:clamp(48px,7vw,96px) clamp(28px,4vw,44px);border-bottom:1px solid var(--hair)}
.tc-hero h1{font-size:clamp(40px,6vw,80px);line-height:1;max-width:16ch;margin:16px 0 18px}
.tc-hero .lede{max-width:58ch}
.tc-sec{padding-block:clamp(40px,6vw,72px);border-bottom:1px solid var(--hair)}
.tc-sec h2{font-size:clamp(28px,3.2vw,40px);line-height:1.1;margin:0 0 18px}
.tc-list{list-style:none;margin:0;padding:0;border-top:1px solid var(--ink)}
.tc-row{display:grid;grid-template-columns:44px minmax(0,1.4fr) repeat(3,minmax(0,1fr)) auto;gap:16px;align-items:center;padding:18px 0;border-bottom:1px solid var(--hair)}
.tc-n{font-family:var(--f-num,inherit);font-size:13px;color:var(--mute,#6b6b6b)}
.tc-name{font-family:var(--display);font-size:24px;color:var(--ink);text-decoration:none}
.tc-f{display:flex;flex-direction:column;gap:4px}.tc-f b{font-size:18px;font-weight:500}
.tc-go{white-space:nowrap}
@media (max-width:760px){.tc-row{grid-template-columns:32px repeat(3,minmax(0,1fr));gap:12px 14px}.tc-n{grid-row:1;grid-column:1}.tc-name{grid-row:1;grid-column:2/5}.tc-row>:nth-child(3){grid-row:2;grid-column:2}.tc-row>:nth-child(4){grid-row:2;grid-column:3}.tc-row>:nth-child(5){grid-row:2;grid-column:4}.tc-go{grid-row:3;grid-column:2/5;justify-self:start}}
.tc-how p{font-size:18px;font-weight:300;line-height:1.7;max-width:68ch}.tc-how p+p{margin-top:14px}
.tc-how code{font-size:16px}
</style>"""
    body = f"""<!--BODY-->{header('../')}
<main>
  <section class="tc-hero"><div class="wrap">
    <span class="label">Outil · Fee calculator</span>
    <h1>What your futures trading <em>really costs.</em></h1>
    <p class="lede">Type your position size and how often you trade. The bars show the monthly fee on {len(known)} exchanges at standard rates, before and after a {config['brand']} rebate. Rates checked {esc(config['fees_checked'])}; your live account rate applies.</p>
  </div></section>

  <section class="tc-sec" id="fees" aria-label="Fee calculator"><div class="wrap">
    <div class="calc">
      <div class="controls">
        <div class="field"><label class="label" for="notional">Position size, USDT</label><input id="notional" type="number" inputmode="decimal" min="0" step="100" value="10000"><span class="hint">Margin × leverage. 1,000 at 10× is 10,000.</span></div>
        <div class="field"><span class="label" id="otLabel">Order type</span>
          <div class="seg" role="group" aria-labelledby="otLabel"><button type="button" id="otTaker" aria-pressed="true">Market order</button><button type="button" id="otMaker" aria-pressed="false">Limit order</button></div></div>
        <div class="field"><label class="label" for="trades">Round trips per month</label><input id="trades" type="number" inputmode="numeric" min="1" step="1" value="20"></div>
        <label class="check" for="withReb"><input type="checkbox" id="withReb" checked> Include {config['brand']} rebate</label>
      </div>
      <div><div class="bars" id="bars" aria-live="polite"></div><p class="fine" id="calcNote" style="margin-top:16px"></p></div>
    </div>
  </div></section>

  <section class="tc-sec" aria-labelledby="cheapH"><div class="wrap">
    <span class="label">Le classement</span>
    <h2 id="cheapH">Lowest taker fee after rebate</h2>
    <ol class="tc-list" data-place="tool-calc-list">{rows}</ol>
    <p class="fine" style="margin-top:16px">Standard (non-VIP) USDT-margined perpetual rates, checked {esc(config['fees_checked'])}. “You pay” is the taker rate minus the rebate share. Sign-up links are referral links; no password or API key is ever needed.</p>
  </div></section>

  <section class="tc-sec tc-how" aria-labelledby="howH"><div class="wrap">
    <span class="label">La méthode</span>
    <h2 id="howH">How the numbers are worked out</h2>
    <p>Monthly fee = position size × fee rate × 2 × round trips. The “× 2” is there because you pay once to open and once to close. With the rebate switched on, the fee is multiplied by (1 − rebate share).</p>
    <p>Example at standard rates: a 10,000 USDT position, closed and reopened 20 times a month with market orders, on an exchange charging 0.05% taker is 10,000 × 0.0005 × 2 × 20 = 200 USDT in fees. A 40% rebate returns 80 of that.</p>
    <p>For the details behind each input, read <a href="../guides/maker-vs-taker-fees.html">maker vs taker fees</a>, <a href="../guides/how-fee-rebates-work.html">how fee rebates work</a> and <a href="../guides/futures-break-even-price.html">your break-even price after fees</a>.</p>
    <div class="faq" style="margin-top:32px">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faqs)}</div>
  </div></section>
</main>
{footer('../')}
{fab}
<script>window.HOME="../index.html"; window.LANG="en";
{common_js}
const VENUES = {js_venues};
let mode="taker";
function calc(){{
  const n=Math.max(0,parseFloat($("notional").value)||0), t=Math.max(1,parseInt($("trades").value)||1), reb=$("withReb").checked;
  const money=x=>"$"+x.toLocaleString("en-US",{{minimumFractionDigits:2,maximumFractionDigits:2}});
  const whole=x=>x.toLocaleString("en-US",{{maximumFractionDigits:0}});
  const data=VENUES.filter(v=>v[mode]!=null).map(v=>{{ const g=n*(v[mode]/100)*2*t; return {{name:v.name,g,net:reb?g*(1-v.rebate/100):g}}; }}).sort((a,b)=>a.net-b.net);
  const max=Math.max(...data.map(d=>d.g),0.0001); const box=$("bars"); box.textContent="";
  data.forEach(d=>{{
    const row=document.createElement("div"); row.className="bar";
    row.innerHTML='<span class="n"></span><div class="track"><div class="fill"></div><div class="fill reb"></div></div><span class="v"></span>';
    row.querySelector(".n").textContent=d.name;
    const fills=row.querySelectorAll(".fill");
    fills[0].style.width=(d.g/max*100)+"%"; fills[0].style.opacity=reb?.18:1;
    fills[1].style.width=reb?(d.net/max*100)+"%":"0";
    row.querySelector(".v").textContent=money(d.net);
    box.appendChild(row);
  }});
  const saved=data.reduce((s,d)=>s+(d.g-d.net),0)/Math.max(data.length,1);
  $("calcNote").textContent = reb
    ? `${{t}} round trips a month at $${{whole(n)}}, after rebate. The faint line is the fee before rebate; on average the rebate saves ${{money(saved)}} a month. Funding not included.`
    : `${{t}} round trips a month at $${{whole(n)}}, before rebate. Funding not included.`;
}}
["notional","trades","withReb"].forEach(id=>$(id).addEventListener("input",calc));
$("otTaker").addEventListener("click",()=>{{mode="taker";$("otTaker").setAttribute("aria-pressed","true");$("otMaker").setAttribute("aria-pressed","false");calc();}});
$("otMaker").addEventListener("click",()=>{{mode="maker";$("otMaker").setAttribute("aria-pressed","true");$("otTaker").setAttribute("aria-pressed","false");calc();}});
calc();
btcPill();</script>"""
    return head(title, desc, canonical, extra + css) + body, canonical
