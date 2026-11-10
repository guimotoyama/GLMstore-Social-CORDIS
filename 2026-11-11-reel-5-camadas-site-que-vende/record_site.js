const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = path.resolve(__dirname, 'sitevideo');
const SITE = 'https://guimotoyama.github.io/LP-Advogados/';
const W = 1440, H = 900;

// The site uses GSAP ScrollTrigger: window.scrollTo() is fought by the
// library and the position sticks. Real wheel events are the only way in.
const SCROLL_STEP = 15;   // px per wheel tick
const SCROLL_EVERY = 72; // ms between ticks -> ~150 px/s
const HOLD_MS = 3000;     // hold on the contact section at the end
const LOAD_MS = 2500;     // settle before scrolling starts (trimmed later)

(async () => {
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });

  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const ctx = await browser.newContext({
    viewport: { width: W, height: H },
    recordVideo: { dir: OUT, size: { width: W, height: H } },
  });
  const page = await ctx.newPage();
  const t0 = Date.now();
  await page.goto(SITE, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(400);

  await page.evaluate(() => {
    document.querySelectorAll('*').forEach(el => {
      const s = getComputedStyle(el);
      if (s.animationName !== 'none') el.style.animationPlayState = 'paused';
    });
  });
  await page.waitForTimeout(LOAD_MS);

  const maxY = await page.evaluate(() => {
    const el = document.scrollingElement || document.documentElement;
    return Math.max(0, el.scrollHeight - window.innerHeight);
  });
  console.log('max scroll:', maxY);

  await page.mouse.move(720, 450);

  const totalTicks = Math.ceil(maxY / SCROLL_STEP);
  const tScroll = Date.now();
  for (let i = 0; i < totalTicks; i++) {
    await page.mouse.wheel(0, SCROLL_STEP);
    await page.waitForTimeout(SCROLL_EVERY);
    if (i % 40 === 0) {
      const y = await page.evaluate(() => Math.round(window.scrollY));
      console.log('  tick', i, '/', totalTicks, 'y=', y);
    }
  }
  console.log('scroll took', ((Date.now() - tScroll) / 1000).toFixed(1), 's');

  await page.waitForTimeout(HOLD_MS);

  const elapsed = (Date.now() - t0) / 1000;
  console.log('wall time:', elapsed.toFixed(1), 's');

  const video = page.video();
  await ctx.close();               // flushes the video file
  await browser.close();

  const p = await video.path();
  const dest = path.join(__dirname, 'site-scroll-raw.webm');
  fs.copyFileSync(p, dest);
  fs.rmSync(OUT, { recursive: true, force: true });
  console.log('RECORDED:', dest, fs.statSync(dest).size, 'bytes');
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
