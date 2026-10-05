// Salin halaman /haji/ (runtime React) menjadi HTML statis mandiri untuk haji.biz.
// Prasyarat: React UMD lokal di /tmp/rpk (npm i react@18.3.1 react-dom@18.3.1), playwright global.
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright');
const fs=require('fs');
const OUT='wordpress/haji-biz/halaman-haji/';
(async()=>{
 const px=process.env.HTTPS_PROXY;
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',proxy:px?{server:px}:undefined,args:['--ignore-certificate-errors']});
 const pg=await (await b.newContext({viewport:{width:1280,height:900},ignoreHTTPSErrors:true})).newPage();
 await pg.route('https://unpkg.com/**',r=>{const f=r.request().url().includes('react-dom')?'/tmp/rpk/react-dom/umd/react-dom.production.min.js':'/tmp/rpk/react/umd/react.production.min.js'; r.fulfill({path:f,contentType:'application/javascript'});});
 await pg.goto('https://www.elharamainwisata.com/haji/',{waitUntil:'networkidle',timeout:90000});
 await pg.waitForTimeout(2500);
 const data=await pg.evaluate(async()=>{
  const sleep=ms=>new Promise(r=>setTimeout(r,ms));
  const find=t=>[...document.querySelectorAll('button')].find(x=>x.innerText.trim()===t);
  const groups={itin:['Silver','Gold','Gold Arbain','Platinum'],inc:['Sudah Termasuk','Belum Termasuk & Ketentuan']};
  const res={};
  for(const [g,names] of Object.entries(groups)){
    res[g]=[];
    for(const n of names){
      const btn=find(n); btn.click(); await sleep(400);
      const row=find(n).parentElement;
      res[g].push({n,row:row.outerHTML,content:row.nextElementSibling.outerHTML});
    }
    // kembalikan ke tab pertama
    find(names[0]).click(); await sleep(300);
  }
  const rowI=find('Silver').parentElement, rowT=find('Sudah Termasuk').parentElement;
  rowI.setAttribute('data-g','itin'); rowI.nextElementSibling.setAttribute('data-gc','itin');
  rowT.setAttribute('data-g','inc'); rowT.nextElementSibling.setAttribute('data-gc','inc');
  const css=[...document.querySelectorAll('head style')].map(s=>s.textContent).filter(t=>!/sc-placeholder|x-dc\{|html,body\{height/.test(t));
  const ld=[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent);
  return {res,css,html:document.getElementById('dc-root').innerHTML,ld};
 });
 fs.writeFileSync('/tmp/haji_capture.json',JSON.stringify(data));
 console.log('css',data.css.length,'html',data.html.length,'ld',data.ld.length);
 await b.close();
})().catch(e=>{console.log('ERR',e.message.slice(0,300));process.exit(1)});
