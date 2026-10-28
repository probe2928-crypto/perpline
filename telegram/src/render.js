// node telegram/src/render.js [outDir] — rebate-post.png + pinned-banner.png
const {chromium}=require('playwright');const path=require('path');
const OUT=process.argv[2]||path.join(__dirname,'..');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const [img,file] of [['post','rebate-post.png'],['pinned','pinned-banner.png']]){
 await p.goto('file://'+path.join(__dirname,'telegram.html')+'?img='+img);await p.waitForSelector('body[data-ready]');await p.waitForTimeout(100);
 await (await p.$('#art')).screenshot({path:path.join(OUT,file)});}
await b.close();console.log('done');})();
