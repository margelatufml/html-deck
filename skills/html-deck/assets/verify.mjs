// Render every slide headless at exactly 1920x1080 and assert nothing overflows.
//
// REQUIREMENT: `playwright` must be resolvable, and its Chromium installed. From
// the directory you run this in (or any parent), or from the skill's own directory:
//
//     npm i -D playwright && npx playwright install chromium
//
// Node ESM ignores NODE_PATH, so this resolves playwright through createRequire
// against the cwd first and the script's own location second.
//
// RUN:
//     node verify.mjs <deck-dir> <slide-count>
//     node verify.mjs ~/talk/deck 14
//
// Prints one line per slide. Exits 1 if any slide overflows the canvas or clips
// its own text. Screenshots go to <deck-dir>/../shots/slideN.png.
//
// The deck pulls Tailwind, Font Awesome and Google Fonts from CDNs, so this needs
// the network. Without it every slide renders unstyled and every check is garbage.
//
// THE CHECK IS NOT THE VERIFICATION. Open the screenshots and look at them. This
// catches geometry; it does not catch a stamp sitting on a paragraph, an
// unreadable contrast pair, or a chart whose bars contradict its numbers.

import { mkdirSync } from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

let chromium;
try {
  chromium = createRequire(path.join(process.cwd(), "x.js"))("playwright").chromium;
} catch {
  chromium = createRequire(import.meta.url)("playwright").chromium;
}

const W = 1920, H = 1080;
const TOL = 1; // sub-pixel rounding

const deckDir = path.resolve(process.argv[2] ?? "");
const count = Number(process.argv[3]);

if (!process.argv[2] || !Number.isInteger(count) || count < 1) {
  console.error("usage: node verify.mjs <deck-dir> <slide-count>");
  process.exit(2);
}

const shotDir = path.join(deckDir, "..", "shots");
mkdirSync(shotDir, { recursive: true });

// .animate-entry starts at opacity 0 and fades in over 0.8s. Freezing it is what
// the print stylesheet already does; do the same here so measurements are stable.
const FREEZE = `
  *, *::before, *::after { animation: none !important; transition: none !important; }
  .animate-entry { opacity: 1 !important; transform: none !important; }
`;

const measure = ([w, h, tol]) => {
  const root = document.documentElement;
  // Stop at <body>: the head sets body{overflow:hidden}, which CSS propagates to
  // the viewport, so body does not actually clip. Walking into it would mark
  // every element on the slide as "clipped" and the check would never fire.
  const clipped = (el) => {
    for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
      const o = getComputedStyle(p);
      if (/hidden|clip|auto|scroll/.test(o.overflowX + o.overflowY)) return true;
    }
    return false;
  };
  const label = (el) => {
    const id = el.id ? `#${el.id}` : "";
    const cls = (el.getAttribute("class") || "").trim().split(/\s+/).slice(0, 4).join(".");
    const txt = (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 48);
    return `<${el.tagName.toLowerCase()}${id}${cls ? "." + cls : ""}> ${txt}`;
  };

  const outside = [];
  const overset = [];
  for (const el of root.querySelectorAll("*")) {
    if (el.tagName === "SCRIPT" || el.tagName === "STYLE") continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (getComputedStyle(el).visibility === "hidden") continue;

    if (!clipped(el) &&
        (r.left < -tol || r.top < -tol || r.right > w + tol || r.bottom > h + tol)) {
      outside.push({
        el: label(el),
        rect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)],
      });
    }
    // content taller/wider than its own clipping box: text silently cut off
    const o = getComputedStyle(el);
    if (el !== document.body && /hidden|clip/.test(o.overflowY) &&
        el.scrollHeight > el.clientHeight + tol) {
      overset.push({ el: label(el), by: el.scrollHeight - el.clientHeight });
    }
  }
  return {
    scrollW: root.scrollWidth,
    scrollH: root.scrollHeight,
    outside: outside.slice(0, 8),
    outsideTotal: outside.length,
    overset: overset.slice(0, 8),
    oversetTotal: overset.length,
  };
};

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });

let bad = 0;
for (let i = 1; i <= count; i++) {
  const file = path.join(deckDir, `slide${i}.html`);
  await page.goto(pathToFileURL(file).href, { waitUntil: "networkidle" });
  await page.addStyleTag({ content: FREEZE });
  await page.evaluate(() => document.fonts.ready.then(() => true));

  const m = await page.evaluate(measure, [W, H, TOL]);
  await page.screenshot({ path: path.join(shotDir, `slide${i}.png`) });

  const overCanvas = m.scrollW > W + TOL || m.scrollH > H + TOL;
  const fail = overCanvas || m.outsideTotal > 0 || m.oversetTotal > 0;
  if (fail) bad++;

  const tag = fail ? "FAIL" : "ok  ";
  console.log(
    `${tag} slide${String(i).padStart(2, "0")}  canvas ${m.scrollW}x${m.scrollH}` +
    `  outside=${m.outsideTotal}  clipped=${m.oversetTotal}`
  );
  for (const o of m.outside) console.log(`       outside [${o.rect.join(",")}] ${o.el}`);
  for (const o of m.overset) console.log(`       clipped ${o.by}px  ${o.el}`);
}

await browser.close();
console.log(`\n${count - bad}/${count} clean. Screenshots: ${shotDir}`);
console.log("Now LOOK at them. Geometry passing is not the same as the slide being right.");
process.exit(bad ? 1 : 0);
