const { chromium } = require('playwright');
const path = require('path');

const SEL = {
  device: '.frame',
  headline: '#headline',
  kicker: '#kicker',
  counter: '#counter',
  card: '#card',
  summary: '#summary',
  brandbar: '#brandbar',
  end: '#end',
};
const EXCLUDE_PAIRS = new Set([['device', 'kicker'], ['device', 'counter']]); // texto por cima do aparelho nao existe; mantido para registro

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file:///' + path.join(__dirname, 'reel.html').replace(/\\/g, '/'));
  await page.waitForTimeout(700);
  await page.waitForFunction(() => {
    const v = document.getElementById('siteVid');
    return v && v.readyState >= 1 && v.videoWidth > 0;
  }, { timeout: 30000 });
  await page.evaluate(async () => {
    const v = document.getElementById('siteVid');
    v.muted = true;
    try { await v.play(); } catch (e) {}
    await new Promise(r => setTimeout(r, 400));
    try { v.pause(); } catch (e) {}
  });

  const rows = [];
  let worst = 999, worstAt = null, problems = 0;
  for (let t = 0; t <= 28.001; t += 0.5) {
    await page.evaluate(tt => window.renderFrame(tt), t);
    const r = await page.evaluate((sel) => {
      const out = {};
      for (const k in sel) {
        const e = document.querySelector(sel[k]);
        if (!e) continue;
        const b = e.getBoundingClientRect();
        const cs = getComputedStyle(e);
        out[k] = { x: b.x, y: b.y, w: b.width, h: b.height, right: b.right, bottom: b.bottom, o: parseFloat(cs.opacity) };
      }
      return out;
    }, SEL);
    const vis = Object.entries(r).filter(([, v]) => v.o > 0.05);
    for (const [k, v] of vis) {
      if (v.x < -1 || v.y < -1 || v.right > 1081 || v.bottom > 1921) {
        console.log(`FORA t=${t.toFixed(1)} ${k} ${JSON.stringify(v)}`); problems++;
      }
    }
    for (let i = 0; i < vis.length; i++) {
      for (let j = i + 1; j < vis.length; j++) {
        const [ka, a] = vis[i], [kb, b] = vis[j];
        const dx = Math.max(0, Math.max(a.x, b.x) - Math.min(a.right, b.right));
        const dy = Math.max(0, Math.max(a.y, b.y) - Math.min(a.bottom, b.bottom));
        const gap = (dx > 0 && dy > 0) ? Math.hypot(dx, dy) : Math.max(dx, dy);
        if (gap < 25) {
          console.log(`COLISAO t=${t.toFixed(1)} ${ka}<->${kb} gap=${gap.toFixed(1)}`);
          problems++;
        }
        if (ka === 'device' && gap < worst) { worst = gap; worstAt = `${t.toFixed(1)} ${kb}`; }
      }
    }
  }
  console.log(`\nWORST_DEVICE_GAP = ${worst.toFixed(1)}px em t=${worstAt}`);
  console.log(`PROBLEMAS = ${problems}`);
  await browser.close();


})().catch(e=>{console.error("ERR",e.message);process.exit(1)});
