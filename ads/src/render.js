// node ads/src/render.js [outDir]  — renders every banner from banners.html
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const OUT=process.argv[2]||path.join(__dirname,'..','banners');
const SIZES=['160x600','250x250','300x250','300x600','320x100','336x280','728x90','970x90']; // 320x50 & 468x60 carry no number
const TONES=['ivory','klein','noir'];
const GIFS=['300x250','728x90','160x600'];
(async()=>{fs.mkdirSync(OUT,{recursive:true});const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1});
 const shot=async(tone,size,frame,file)=>{await p.goto('file://'+path.join(__dirname,'banners.html')+`?tone=${tone}&size=${size}&frame=${frame}`);
   await p.waitForSelector('body[data-ready]');await p.waitForTimeout(80);await (await p.$('#ban')).screenshot({path:file});};
 for(const t of TONES)for(const s of SIZES)await shot(t,s,0,path.join(OUT,`perpline_${t}_${s}.png`));
 for(const s of GIFS)for(const f of [0,1,2])await shot('ivory',s,f,path.join(OUT,`.f_${s}_${f}.png`));
 await b.close();
 const {execFileSync}=require('child_process');
 for(const s of GIFS){execFileSync('python3',['-c',`
from PIL import Image
fr=[Image.open('${OUT}/.f_${s}_%d.png'%i).convert('RGB') for i in range(3)]
pal=[f.quantize(colors=128,method=Image.Quantize.MEDIANCUT) for f in fr]
pal[0].save('${OUT}/perpline_ivory_${s}_animated.gif',save_all=True,append_images=pal[1:],duration=[2600,2200,2200],loop=0,optimize=True)
`]);for(const f of [0,1,2])fs.unlinkSync(path.join(OUT,`.f_${s}_${f}.png`));}
 console.log('done',OUT);})();
