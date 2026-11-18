const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const DIR = __dirname;
const OUT = path.join(DIR, 'frames');
const FPS = 25, DUR = 28.0;
const TOTAL = Math.round(DUR * FPS);

(async () => {
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file:///' + path.join(DIR, 'reel.html').replace(/\\/g, '/'));
  await page.waitForTimeout(600);

  // wait for video metadata
  await page.waitForFunction(() => {
    const v = document.getElementById('siteVid');
    return v && v.readyState >= 1 && v.videoWidth > 0;
  }, { timeout: 30000 });

  // preload the whole video so seeks are instant
  await page.evaluate(async () => {
    const v = document.getElementById('siteVid');
    v.muted = true;
    try { await v.play(); } catch (e) {}
    await new Promise(r => setTimeout(r, 400));
    try { v.pause(); } catch (e) {}
  });
  await page.waitForTimeout(400);

  console.log('rendering', TOTAL, 'frames');
  const t0 = Date.now();
  const START = parseInt(process.argv[2] || '0', 10);
  for (let i = START; i < TOTAL; i++) {
    const t = i / FPS;
    const vt = await page.evaluate(tt => window.renderFrame(tt), t);
    // deterministic seek
    await page.evaluate(async (target) => {
      const v = document.getElementById('siteVid');
      if (Math.abs(v.currentTime - target) > 0.001) {
        await new Promise(res => {
          const done = () => res();
          v.addEventListener('seeked', done, { once: true });
          try { v.currentTime = target; } catch (e) { res(); }
          setTimeout(done, 800);
        });
      }
      await new Promise(res => requestAnimationFrame(() => requestAnimationFrame(res)));
    }, vt);
    await page.screenshot({ path: path.join(OUT, `f${String(i).padStart(4, '0')}.png`) });
    if (i % 75 === 0) {
      const el = ((Date.now() - t0) / 1000).toFixed(1);
      console.log(`  frame ${i}/${TOTAL}  (${el}s)`);
    }
  }
  await browser.close();
  console.log('DONE in', ((Date.now() - t0) / 1000).toFixed(1), 's');
})();
