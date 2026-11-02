/* Perpline monthly sign-up draw — plan & legal notes: chainbrief ops/events/PLAN.md
   enabled:true = public. Turn on only after (1) site sign-in is live, (2) ops/events/schema.sql is run and the round row is 'open',
   (3) the Korean tax adviser has confirmed the non-resident prize treatment (PLAN.md §2). Local preview: ?event_preview=1 */
window.SITE_EVENT = {
  enabled: false,
  site: "perpline",
  lang: "en",
  kind: "draw",
  id: "pl-2026-12",
  rulesUrl: document.currentScript ? document.currentScript.src.replace(/event-config\.js.*$/, "") : "event/",
  versions: { rules: "2026-11-02", consent: "ev-2026-11-02", marketing: "2026-11-02" },
  width: "1180px",
  theme: { ink: "var(--ink)", paper: "var(--paper)", accent: "var(--ink)", muted: "var(--muted)", line: "var(--hair)", wash: "var(--wash)", radius: "0px",
           font: "var(--sans)", display: "var(--display)", dw: "400" },
  banner: {
    mount: "#venues",
    where: "beforebegin",
    figure: "3 × 20",
    figureNote: "USDT · drawn monthly",
    title: "Free monthly draw for Perpline members",
    body: "Create a free account and enter once a month. No deposit, no trading, no purchase. Winners pick USDT, SOL or ETH.",
    cta: "How it works",
    label: "Monthly member draw"
  },
  entry: {
    title: "Enter the December draw",
    loginNote: "Entries are for signed-in members. Creating an account is free.",
    afterNote: "We draw on 4 January and email the three winners on 5 January.",
    countries: [
      ["AR","Argentina"],["AU","Australia"],["AT","Austria"],["BD","Bangladesh"],["BE","Belgium"],["CA","Canada (excluding Quebec)"],["CL","Chile"],
      ["CO","Colombia"],["CZ","Czechia"],["EG","Egypt"],["FR","France"],["DE","Germany"],["GR","Greece"],["IN","India"],["ID","Indonesia"],
      ["IE","Ireland"],["JP","Japan"],["KE","Kenya"],["MY","Malaysia"],["MX","Mexico"],["MA","Morocco"],["NL","Netherlands"],
      ["NZ","New Zealand"],["NG","Nigeria"],["PK","Pakistan"],["PE","Peru"],["PL","Poland"],["PT","Portugal"],["RO","Romania"],["SA","Saudi Arabia"],
      ["SG","Singapore"],["ZA","South Africa"],["ES","Spain"],["SE","Sweden"],["CH","Switzerland"],["TW","Taiwan"],["TH","Thailand"],["TR","Türkiye"],
      ["UA","Ukraine"],["AE","United Arab Emirates"],["GB","United Kingdom"],["VN","Vietnam"]
    ],
    attest: [
      { label: "I am 18 or older (or the age of majority where I live) and I do not live in an excluded country" },
      { label: 'I have read and agree to the <a href="#rules" style="text-decoration:underline;text-underline-offset:3px">official rules</a>' },
      { label: "I agree to the use of my entry data for this draw",
        detail: "<b>Purpose</b> running the draw, contacting winners, fraud checks<br><b>Data</b> your account email (already on file), country of residence, entry time<br><b>Kept</b> deleted 30 days after winners are announced (winners: 30 days after the prize is sent)<br><b>Shared</b> with no one<br>You can say no; you just can't enter. Your account is not affected." }
    ],
    marketing: ["email"]
  }
};
(function () {
  var C = window.SITE_EVENT, local = /^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  if (!C.enabled && !(local && /[?&]event_preview=1(&|$)/.test(location.search)) && !document.documentElement.hasAttribute("data-event-page")) return;
  var s = document.createElement("script"); s.src = (document.currentScript && document.currentScript.src || "").replace(/event-config\.js.*$/, "event.js"); s.defer = true; document.head.appendChild(s);
})();
