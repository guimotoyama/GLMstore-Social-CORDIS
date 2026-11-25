const { chromium } = require('playwright');
const fs = require('fs');
const DIR = __dirname;
const FPS = 30, DUR = 22, TOTAL = FPS * DUR;
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + DIR + '/cena-reel.html');
  await page.waitForTimeout(1400);
  fs.mkdirSync(DIR + '/frames', { recursive: true });
  for (let i = 0; i < TOTAL; i++) {
    const t = i / FPS;
    const f = DIR + '/frames/f' + String(i).padStart(4, '0') + '.png';
    if (fs.existsSync(f)) continue;
    await page.evaluate(tt => window.renderFrame(tt), t);
    await page.screenshot({ path: f });
  }
  console.log('FRAMES_OK total=' + TOTAL + ' em ' + DIR + '/frames');
  await browser.close();
})();
