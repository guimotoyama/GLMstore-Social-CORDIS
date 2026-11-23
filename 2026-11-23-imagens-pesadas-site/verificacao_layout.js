// Reel layout probe: measures the device box vs every text band at each timestamp.
// Catches text sitting on the device screen and clearance that only holds at rest.
//
// Usage:
//   NODE_PATH="<pw>/node_modules" node check_layout.js reel.html "0.5,2,8,18,24" [selectors.json]
//
// selectors.json (optional):
//   { "device": ".frame",
//     "bands": { "top": "#headline,#kicker,#counter", "bottom": "#card,#summary,#brandbar" } }
// Defaults to the GLMstore scene. Drop the file to use your own.
//
// Prints one JSON line per timestamp. `warns` lists any device<->band pair whose
// horizontal ranges overlap and whose vertical clearance is < 25px (or negative = overlap).
// Elements at opacity <= 0.05 are treated as hidden and skipped.

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const HTML = process.argv[2] || 'reel.html';
const TIMES = (process.argv[3] || '0.5,8,18,24').split(',').map(Number);
const SELFILE = process.argv[4];
const SEL = SELFILE && fs.existsSync(SELFILE)
  ? JSON.parse(fs.readFileSync(SELFILE, 'utf8'))
  : { device: '.frame', bands: { top: '#headline,#kicker,#counter', bottom: '#card,#summary,#brandbar' } };

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file:///' + path.resolve(HTML).replace(/\\/g, '/'));
  await page.waitForTimeout(600);
  await page.waitForFunction(() => {
    const v = document.querySelector('video');
    return !v || (v.readyState >= 1 && v.videoWidth > 0);
  }, { timeout: 30000 }).catch(() => {});
  await page.evaluate(async () => {
    const v = document.querySelector('video');
    if (!v) return;
    v.muted = true;
    try { await v.play(); } catch (e) {}
    await new Promise(r => setTimeout(r, 400));
    try { v.pause(); } catch (e) {}
  });
  await page.waitForTimeout(300);

  for (const t of TIMES) {
    await page.evaluate(tt => { if (window.renderFrame) window.renderFrame(tt); }, t);
    const out = await page.evaluate((SEL) => {
      const box = (e) => {
        const b = e.getBoundingClientRect();
        return { x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), bottom: Math.round(b.bottom) };
      };
      const pick = (s) => [...document.querySelectorAll(s)].filter(e => parseFloat(getComputedStyle(e).opacity) > 0.05);
      const dev = pick(SEL.device).map(box);
      const bands = {};
      for (const k in SEL.bands) bands[k] = pick(SEL.bands[k]).map(box);
      const warns = [];
      for (const d of dev) {
        for (const k in bands) {
          for (const b of bands[k]) {
            const hOverlap = !(b.x + b.w < d.x || d.x + d.w < b.x);
            if (!hOverlap) continue;
            const vGap = k === 'top' ? d.y - b.bottom : b.y - d.bottom;
            if (vGap < 0) warns.push('OVERLAP ' + SEL.device + ' x ' + k + ' by ' + (-vGap) + 'px');
            else if (vGap < 25) warns.push('TIGHT ' + SEL.device + ' x ' + k + ' gap ' + vGap + 'px');
          }
        }
      }
      return { device: dev, bands, warns };
    }, SEL);
    console.log('t=' + t, JSON.stringify(out));
  }
  await browser.close();
})();
