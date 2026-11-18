const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Filmstrip determinístico: uma captura por frame de reel, rolando com rodas reais.
// Cada frame é uma foto real da página numa posição de rolagem diferente -> movimento garantido.
const OUT = path.resolve(__dirname, 'footage');
const TILES = path.join(OUT, 'tiles');
const URL = 'https://agencia.glmstore.com.br/';
const W = 860, H = 1864;
const TOTAL = parseInt(process.argv[2] || '700', 10);
const SETTLE = parseInt(process.argv[3] || '90', 10);

(async () => {
  fs.rmSync(TILES, { recursive: true, force: true });
  fs.mkdirSync(TILES, { recursive: true });
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  try {
    await page.waitForFunction(() => { const p = document.querySelector('.preloader'); return !p || getComputedStyle(p).opacity === '0'; }, { timeout: 25000 });
  } catch (e) {}
  await page.waitForTimeout(2200);
  await page.evaluate((z) => { document.documentElement.style.zoom = z; }, 1.6);
  await page.waitForTimeout(1000);
  const info = await page.evaluate(() => ({ sh: document.documentElement.scrollHeight, maxScroll: document.documentElement.scrollHeight - window.innerHeight }));
  console.log('INFO', JSON.stringify(info));
  await page.mouse.move(W / 2, H / 2);
  await page.waitForTimeout(300);

  const t0 = Date.now();
  for (let i = 0; i < TOTAL; i++) {
    // curva alvo: espalha a rolagem por todos os frames (nada de cauda parada)
    const target = Math.round((i / (TOTAL - 1)) * info.maxScroll);
    let y = await page.evaluate(() => Math.round(window.scrollY));
    let guard = 0;
    while (y < target && guard < 12) {
      await page.mouse.wheel(0, 60);
      await page.waitForTimeout(16);
      y = await page.evaluate(() => Math.round(window.scrollY));
      guard++;
    }
    await page.waitForTimeout(SETTLE);
    await page.screenshot({ path: path.join(TILES, `f${String(i).padStart(4, '0')}.png`) });
    if (i % 50 === 0) console.log(`  frame ${i}/${TOTAL}  y=${y} target=${target}  ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  }
  const yEnd = await page.evaluate(() => Math.round(window.scrollY));
  console.log(JSON.stringify({ tiles: TOTAL, yEnd, maxScroll: info.maxScroll, secs: +((Date.now() - t0) / 1000).toFixed(1) }));
  await browser.close();
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
