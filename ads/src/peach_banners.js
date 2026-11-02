// Peach 소재(광고 랜딩 11/2 개편과 같은 메시지) — node ads/src/peach_banners.js <newsreader woff2 폴더>
// 출력: ads/banners/perpline_peach_<WxH>.png
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const FD=process.argv[2];const out=path.join(__dirname,'..','banners');
const f=n=>'data:font/woff2;base64,'+fs.readFileSync(path.join(FD,n)).toString('base64');
const sizes=[[300,250],[336,280],[250,250],[728,90],[970,90],[468,60],[320,50],[320,100],[300,600],[160,600]];
function html(w,h){const shape=h<=100?((h<=60||w<400)?'strip':'wide'):(w/h<0.6?'tall':'box');
const s=Math.min(w,h);
return `<!doctype html><meta charset=utf-8><style>
@font-face{font-family:N;src:url(${f('newsreader-latin-500-normal.woff2')})}
@font-face{font-family:N;font-style:italic;src:url(${f('newsreader-latin-500-italic.woff2')})}
*{margin:0;box-sizing:border-box}html,body{width:${w}px;height:${h}px;overflow:hidden}
body{background:#F8E4D6;color:#111;font-family:Inter,sans-serif;position:relative;border:1px solid #E7CDBB}
.b{position:absolute;inset:0;display:flex}
.brand{font-size:11px;letter-spacing:.32em;font-weight:500}
h1{font-family:N;font-weight:500;line-height:.98;letter-spacing:-.01em}
h1 em{color:#1F2FA0}
.sub{color:#5a4d44}
.cta{background:#1F2FA0;color:#fff;font-weight:600;display:inline-flex;align-items:center;justify-content:center;white-space:nowrap}
.fine{color:#7a6b60;font-size:9px;letter-spacing:.02em}
/* box */
.box{flex-direction:column;justify-content:space-between;padding:${Math.round(s*.08)}px}
.box h1{font-size:${Math.round(s*.15)}px}.box .sub{font-size:${Math.round(s*.048)}px;margin-top:${Math.round(s*.04)}px}
.box .row{display:flex;align-items:flex-end;justify-content:space-between;gap:8px}
.box .cta{font-size:${Math.round(s*.048)}px;padding:${Math.round(s*.04)}px ${Math.round(s*.055)}px}
/* tall */
.tall{flex-direction:column;justify-content:space-between;padding:${Math.round(w*.11)}px}
.tall h1{font-size:${Math.round(w*(w<200?.2:.15))}px}.tall .sub{font-size:${Math.round(w*(w<200?.075:.05))}px;margin-top:14px}
.tall .cta{font-size:${Math.round(w*(w<200?.072:.05))}px;padding:12px 8px;width:100%}.tall .fine{margin-top:10px;text-align:center}
/* wide */
.wide{align-items:center;justify-content:space-between;padding:0 ${Math.round(h*.25)}px;gap:${Math.round(h*.3)}px}
.wide h1{font-size:${Math.round(h*(w<400?.26:.34))}px;white-space:nowrap}.wide .sub{font-size:${Math.round(h*.13)}px;margin-top:4px;white-space:nowrap}
.wide .cta{font-size:${Math.max(11,Math.round(h*.14))}px;padding:${Math.round(h*.14)}px ${Math.round(h*.2)}px}
.wide .brand{writing-mode:horizontal-tb}
/* strip */
.strip{align-items:center;justify-content:space-between;padding:0 ${Math.round(Math.min(h*.25,16))}px;gap:8px}
.strip h1{font-size:${Math.round(Math.min(h*.36,w*.07))}px;white-space:nowrap}
.strip .cta{font-size:${Math.round(Math.min(h*.22,14))}px;padding:${Math.round(Math.min(h*.16,12))}px ${Math.round(Math.min(h*.22,14))}px}
</style><div class="b ${shape}">${
shape==='box'?`<div><div class=brand>PERPLINE</div></div><div><h1>Futures fees,<br><em>60% back.</em></h1><p class=sub>Open BTCC through Perpline · paid every Monday in USDT</p></div><div class=row><span class=fine>Not for US &amp; Korea<br>residents · 18+</span><span class=cta>Get 60% back →</span></div>`
:shape==='tall'?`<div class=brand style="font-size:${w<200?9:11}px">PERPLINE</div><div><h1>Futures fees, <em>60% back.</em></h1><p class=sub>Open BTCC through Perpline. Paid every Monday in USDT.</p></div><div><span class=cta>Get 60% back →</span><p class=fine>Not for US &amp; Korea residents · 18+</p></div>`
:shape==='wide'?`${w>=500?'<div class=brand>PERPLINE</div>':''}<div style="flex:1"><h1>Futures fees, <em>60% back.</em></h1>${w>=900?'<p class=sub>Open BTCC through Perpline · paid every Monday in USDT · Not for US &amp; Korea residents · 18+</p>':''}</div><span class=cta>Get 60% back →</span>`
:`<h1>Fees, <em>60% back.</em></h1><span class=cta>Get 60% back →</span>`}</div>`;}
(async()=>{const b=await chromium.launch();for(const [w,h] of sizes){const p=await b.newPage({viewport:{width:w,height:h}});
await p.setContent(html(w,h));await p.waitForTimeout(150);
const of=await p.evaluate(()=>[...document.querySelectorAll('h1,.cta,.sub')].some(e=>{const r=e.getBoundingClientRect();return r.right>innerWidth+0.5||r.bottom>innerHeight+0.5}));
const file=path.join(out,`perpline_peach_${w}x${h}.png`);await p.screenshot({path:file});
console.log(w+'x'+h,of?'OVERFLOW':'ok',fs.statSync(file).size);}await b.close();})();
