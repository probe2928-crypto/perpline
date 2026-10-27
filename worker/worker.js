// Perpline API — Cloudflare Worker
//   POST /cs           support form  -> your Telegram DM
//   GET  /go/<slug>    referral click -> counted, then redirected to the exchange
//   GET  /stats?key=   click report (last 30 days)
//   cron (daily)       yesterday's clicks -> your Telegram DM
//
// Settings > Variables and Secrets:
//   TG_BOT_TOKEN   (Secret)  token from @BotFather
//   TG_CHAT_ID     (Secret)  your chat id with the bot
//   STATS_KEY      (Secret)  any long random string, used to open /stats
//   ALLOWED_ORIGIN (Text)    https://your-domain.com
// Settings > Bindings: KV namespace, variable name CLICKS
// Settings > Triggers: Cron "0 0 * * *"  (09:00 KST daily summary)

const REFS = {
  "btcc": "https://partner.btcc.com/kr/c/DDHOR6",
  "okx": "https://www.okx.com/join/96335797",
  "gate": "https://www.gate.com/share/vfffufhw",
  "bingx": "https://bingx.com/invite/8PFSGN/",
  "orangex": "https://www.orangex.com/register?i=4htatgs2",
  "bitget": "https://partner.bitget.com/bg/PJHUWG",
  "bitunix": "https://www.bitunix.com/register?vipCode=Lbya",
  "blofin": "https://blofin.com/register?breferral_code=9mqzvd",
  "deepcoin": "https://s.deepcoin.com/jdhaafj",
  "biconomy": "https://www.biconomy.com/sign-up?r_user_id=W999H2024",
  "crypfine": "https://www.crypfine.com/auth/NDVTRSK"
};

const MAX_LEN = 2000;
const hits = new Map();
const day = (d = new Date()) => d.toISOString().slice(0, 10);

async function tg(env, text) {
  return fetch(`https://api.telegram.org/bot${env.TG_BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: env.TG_CHAT_ID, text, parse_mode: "HTML", disable_web_page_preview: true }),
  });
}

async function countsFor(env, date) {
  const out = {};
  let cursor;
  do {
    const r = await env.CLICKS.list({ prefix: `c:${date}:`, cursor });
    for (const k of r.keys) {
      const [, , slug, src] = k.name.split(":");
      const n = parseInt((await env.CLICKS.get(k.name)) || "0", 10);
      out[slug] = out[slug] || { total: 0, src: {} };
      out[slug].total += n;
      out[slug].src[src] = (out[slug].src[src] || 0) + n;
    }
    cursor = r.list_complete ? null : r.cursor;
  } while (cursor);
  return out;
}

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    const allowed = env.ALLOWED_ORIGIN || "";
    const cors = {
      "Access-Control-Allow-Origin": allowed || "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Accept",
      "Vary": "Origin",
    };
    const json = (obj, status = 200) =>
      new Response(JSON.stringify(obj), { status, headers: { ...cors, "Content-Type": "application/json" } });

    // ---- referral click ----
    if (req.method === "GET" && url.pathname.startsWith("/go/")) {
      const slug = url.pathname.slice(4).replace(/\/$/, "").toLowerCase();
      const dest = REFS[slug];
      if (!dest) return Response.redirect(allowed || "https://t.me", 302);
      const src = (url.searchParams.get("src") || "direct").replace(/[^a-z0-9_-]/gi, "").slice(0, 24) || "direct";
      if (env.CLICKS) {
        const key = `c:${day()}:${slug}:${src}`;
        ctx.waitUntil((async () => {
          const n = parseInt((await env.CLICKS.get(key)) || "0", 10);
          await env.CLICKS.put(key, String(n + 1), { expirationTtl: 60 * 60 * 24 * 120 });
        })());
      }
      return new Response(null, { status: 302, headers: { Location: dest, "Cache-Control": "no-store", "Referrer-Policy": "no-referrer-when-downgrade" } });
    }

    // ---- stats page ----
    if (req.method === "GET" && url.pathname === "/stats") {
      if (!env.STATS_KEY || url.searchParams.get("key") !== env.STATS_KEY) return new Response("Not found", { status: 404 });
      const days = Math.min(90, Math.max(1, parseInt(url.searchParams.get("days") || "30", 10)));
      const totals = {}, daily = [];
      for (let i = 0; i < days; i++) {
        const d = day(new Date(Date.now() - i * 864e5));
        const c = await countsFor(env, d);
        let sum = 0;
        for (const [s, v] of Object.entries(c)) { totals[s] = (totals[s] || 0) + v.total; sum += v.total; }
        daily.push([d, sum]);
      }
      const rows = Object.keys(REFS).map(s => [s, totals[s] || 0]).sort((a, b) => b[1] - a[1]);
      const all = rows.reduce((a, r) => a + r[1], 0);
      const html = `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Perpline clicks</title>
<style>body{font:15px/1.5 system-ui;margin:24px;max-width:720px}table{border-collapse:collapse;width:100%;margin:12px 0 32px}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}td.n{text-align:right;font-variant-numeric:tabular-nums}.bar{height:6px;background:#1F2FA0}</style>
<h1>Referral clicks · last ${days} days</h1><p>Total: <b>${all}</b></p>
<table><tr><th>Exchange</th><th>Clicks</th><th style="width:40%"></th></tr>${rows.map(([s, n]) => `<tr><td>${s}</td><td class="n">${n}</td><td><div class="bar" style="width:${all ? (n / rows[0][1]) * 100 : 0}%"></div></td></tr>`).join("")}</table>
<h2>By day</h2><table><tr><th>Date (UTC)</th><th>Clicks</th></tr>${daily.map(([d, n]) => `<tr><td>${d}</td><td class="n">${n}</td></tr>`).join("")}</table>`;
      return new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
    }

    // ---- support form ----
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (req.method === "POST" && (url.pathname === "/cs" || url.pathname === "/")) {
      const origin = req.headers.get("Origin") || "";
      if (allowed && origin !== allowed) return json({ ok: false, error: "origin" }, 403);
      const ip = req.headers.get("CF-Connecting-IP") || "unknown";
      const now = Date.now();
      const recent = (hits.get(ip) || []).filter(t => now - t < 600000);
      if (recent.length >= 5) return json({ ok: false, error: "rate_limited" }, 429);
      recent.push(now); hits.set(ip, recent);

      let d;
      try { d = await req.json(); } catch { return json({ ok: false, error: "bad_json" }, 400); }
      if (d.website) return json({ ok: true });
      const clip = s => String(s || "").slice(0, MAX_LEN).trim();
      const msg = clip(d.message), topic = clip(d.topic), page = clip(d.page);
      const user = clip(d.telegram).replace(/^@/, "");
      if (!/^[A-Za-z0-9_]{5,32}$/.test(user) || msg.length < 10) return json({ ok: false, error: "invalid" }, 400);
      const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      const country = req.headers.get("CF-IPCountry") || "?";
      const r = await tg(env,
        `🆕 <b>Perpline CS</b>\n<b>Topic:</b> ${esc(topic)}\n<b>From:</b> @${esc(user)}  →  https://t.me/${esc(user)}\n<b>Country:</b> ${esc(country)}\n\n${esc(msg)}\n\n<i>${esc(page)}</i>`);
      if (!r.ok) return json({ ok: false, error: "telegram" }, 502);
      return json({ ok: true });
    }

    return new Response("Not found", { status: 404 });
  },

  // daily summary to Telegram
  async scheduled(event, env, ctx) {
    if (!env.CLICKS) return;
    const d = day(new Date(Date.now() - 864e5));
    const c = await countsFor(env, d);
    const rows = Object.entries(c).sort((a, b) => b[1].total - a[1].total);
    const total = rows.reduce((a, [, v]) => a + v.total, 0);
    const lines = rows.map(([s, v]) => `• ${s}: <b>${v.total}</b>  (${Object.entries(v.src).map(([k, n]) => `${k} ${n}`).join(", ")})`);
    ctx.waitUntil(tg(env, `📊 <b>Perpline clicks · ${d}</b>\nTotal: <b>${total}</b>\n${lines.join("\n") || "No clicks yesterday."}`));
  },
};
