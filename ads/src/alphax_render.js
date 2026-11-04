// node ads/src/alphax_render.js [outDir]  — renders the AlphaX special creatives from alphax_banners.html
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const OUT=process.argv[2]||path.join(__dirname,'..','alphax');
const FILES={'728x90':'alphax_728x90.png','300x250':'alphax_300x250.png','160x600':'alphax_160x600.png','1080x1080':'social-1080.png','1200x627':'linkedin-1200x627.png'};
(async()=>{fs.mkdirSync(OUT,{recursive:true});const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:1200},deviceScaleFactor:1});
 for(const [size,file] of Object.entries(FILES)){
  await p.goto('file://'+path.join(__dirname,'alphax_banners.html')+`?size=${size}`);
  await p.waitForSelector('body[data-ready]');await p.waitForTimeout(100);
  const bad=await p.evaluate(()=>document.body.dataset.bad);
  await (await p.$('#ban')).screenshot({path:path.join(OUT,file)});
  console.log(size,file,'overflow:',bad);
 }
 await b.close();})();
