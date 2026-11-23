const { chromium } = require('playwright');
const fs = require('fs');
const TILES = 'C:/Users/guilh/reel-work/tiles2';
(async () => {
  fs.mkdirSync(TILES, { recursive: true });
  const b = await chromium.launch({ channel: 'chrome', headless: true, args: ['--disable-gpu'] });
  const ctx = await b.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });
  const p = await ctx.newPage();
  await p.goto('https://agencia.glmstore.com.br/', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await p.waitForTimeout(6000);
  await p.evaluate(() => {
    document.querySelectorAll('*').forEach(el => {
      const s = getComputedStyle(el);
      if (s.animationName !== 'none') el.style.animationPlayState = 'paused';
    });
    document.documentElement.style.scrollBehavior = 'auto';
  });
  await p.mouse.move(195, 500);
  const max = await p.evaluate(() => Math.round(document.documentElement.scrollHeight - window.innerHeight));
  console.log('MAXSCROLL ' + max);
  const STEP = 8, WAIT = 45;
  let i = 0; const meta = [];
  const t0 = Date.now();
  for (; i < 1500; i++) {
    await p.mouse.wheel(0, STEP);
    await p.waitForTimeout(WAIT);
    const y = await p.evaluate(() => Math.round(window.scrollY));
    await p.waitForTimeout(30);
    await p.screenshot({ path: `${TILES}/t${String(i).padStart(4, '0')}.png` });
    meta.push([i, y]);
    if (y >= max - 2) { console.log('FIM y=' + y); break; }
    if (i % 100 === 0) console.log('tile ' + i + ' y=' + y + ' t=' + ((Date.now() - t0) / 1000).toFixed(1));
  }
  fs.writeFileSync('C:/Users/guilh/reel-work/tiles_meta.json', JSON.stringify(meta));
  console.log('TILES ' + meta.length + ' dur=' + ((Date.now() - t0) / 1000).toFixed(1));
  await b.close();
})().catch(e => { console.error('ERR ' + e.message); process.exit(1); });
