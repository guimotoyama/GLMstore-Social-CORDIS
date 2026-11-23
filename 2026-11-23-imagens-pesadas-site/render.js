const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const OUT = 'C:/Users/guilh/reel-work/frames';
const TOTAL = 737, FPS = 30;
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch({ channel: 'chrome', headless: true, args: ['--disable-gpu'] });
  const ctx = await b.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  await p.goto('file:///C:/Users/guilh/reel-work/reel.html', { waitUntil: 'load' });
  await p.waitForTimeout(1500);
  const list = [];
  for (let i = 0; i < TOTAL; i++) list.push('frames_in/f' + String(i).padStart(4, '0') + '.png');
  await p.evaluate((l, cfg) => { window.CFG = cfg; window.setFrames(l); }, list, { fps: FPS, dur: TOTAL / FPS, total: TOTAL });
  await p.waitForTimeout(2500);
  let n = 0;
  const t0 = Date.now();
  for (let i = 0; i < TOTAL; i++) {
    const f = path.join(OUT, 'f' + String(i).padStart(4, '0') + '.png');
    if (fs.existsSync(f)) continue;
    const t = i / FPS;
    await p.evaluate(tt => window.renderFrame(tt), t);
    await p.screenshot({ path: f });
    n++;
    if (n % 100 === 0) console.log('render ' + n + ' t=' + t.toFixed(2) + ' ' + ((Date.now() - t0) / 1000).toFixed(1) + 's');
  }
  console.log('RENDERIZADOS ' + n + ' dur=' + ((Date.now() - t0) / 1000).toFixed(1));
  await b.close();
})().catch(e => { console.error('ERR ' + e.message); process.exit(1); });
