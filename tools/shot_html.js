// node tools/shot_html.js in.html out.png [in2.html out2.png ...]  (1200x630)
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i += 2) {
    const pg = await b.newPage({ viewport: { width: 1200, height: 630 } });
    await pg.goto('file://' + require('path').resolve(a[i]));
    await pg.waitForTimeout(400);
    await pg.screenshot({ path: a[i + 1] });
    await pg.close();
  }
  await b.close();
})();
