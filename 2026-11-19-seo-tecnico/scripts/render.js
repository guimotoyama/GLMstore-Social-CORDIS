const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const DIR = __dirname;
const OUT = path.join(DIR, 'frames');
const FPS = 25, DUR = 25.0;
const TOTAL = Math.round(DUR * FPS);
const BATCH = 80;

const START = parseInt(process.argv[2] || '0', 10);
const END = parseInt(process.argv[3] || String(TOTAL), 10);

if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

async function newPage() {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file:///' + path.join(DIR, 'reel.html').replace(/\\/g, '/'));
  await page.waitForTimeout(500);
  await page.waitForFunction(() => {
    const v = document.getElementById('siteVid');
    return v && v.readyState >= 1 && v.videoWidth > 0;
  }, { timeout: 30000 });
  await page.evaluate(async () => {
    const v = document.getElementById('siteVid');
    v.muted = true;
    try { await v.play(); } catch (e) {}
    await new Promise(r => setTimeout(r, 300));
    try { v.pause(); } catch (e) {}
  });
  await page.waitForTimeout(300);
  return { browser, page };
}

(async () => {
  let done = START;
  const t0 = Date.now();
  while (done < END) {
    const target = Math.min(done + BATCH, END);
    const { browser, page } = await newPage();
    try {
      for (let i = done; i < target; i++) {
        const t = i / FPS;
        const vt = await page.evaluate(tt => window.renderFrame(tt), t);
        await page.evaluate(async (vtarget) => {
          const v = document.getElementById('siteVid');
          if (Math.abs(v.currentTime - vtarget) > 0.001) {
            await new Promise(res => {
              const done2 = () => res();
              v.addEventListener('seeked', done2, { once: true });
              try { v.currentTime = vtarget; } catch (e) { res(); }
              setTimeout(done2, 700);
            });
          }
          await new Promise(res => requestAnimationFrame(() => requestAnimationFrame(res)));
        }, vt);
        await page.screenshot({ path: path.join(OUT, `f${String(i).padStart(4, '0')}.png`) });
        if (i % 40 === 0) {
          const el = ((Date.now() - t0) / 1000).toFixed(1);
          console.log(`  frame ${i}/${TOTAL}  (${el}s)`);
        }
      }
    } finally {
      await browser.close();
    }
    done = target;
    console.log(`batch ${done}/${END} ok`);
  }
  console.log('DONE in', ((Date.now() - t0) / 1000).toFixed(1), 's');
})();
