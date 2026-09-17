// Render each slide to a one-page 1920x1080 PDF with print media emulation.
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
//     node export_pdf.mjs <deck-dir> <slide-count> [out-dir]
//     node export_pdf.mjs ~/talk/deck 14
//     pdfunite /tmp/deckpdf_*.pdf ~/talk/My-Talk.pdf        # poppler
//     qpdf --empty --pages /tmp/deckpdf_*.pdf -- ~/talk/My-Talk.pdf   # alternative
//
// Files are written zero-padded (deckpdf_01.pdf) so the shell glob sorts right;
// deckpdf_1, deckpdf_10, deckpdf_2 would merge the deck out of order.
//
// page.pdf() only works in headless Chromium. The @media print block in the deck
// head does the real work: it paints the background (Chrome prints white without
// it), forces print-color-adjust, and freezes .animate-entry, which starts at
// opacity 0 and would otherwise export mid-fade.

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

const deckDir = path.resolve(process.argv[2] ?? "");
const count = Number(process.argv[3]);
const outDir = path.resolve(process.argv[4] ?? "/tmp");

if (!process.argv[2] || !Number.isInteger(count) || count < 1) {
  console.error("usage: node export_pdf.mjs <deck-dir> <slide-count> [out-dir]");
  process.exit(2);
}

mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.emulateMedia({ media: "print" });

const written = [];
for (let i = 1; i <= count; i++) {
  const file = path.join(deckDir, `slide${i}.html`);
  await page.goto(pathToFileURL(file).href, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready.then(() => true));

  const out = path.join(outDir, `deckpdf_${String(i).padStart(2, "0")}.pdf`);
  await page.pdf({
    path: out,
    width: `${W}px`,
    height: `${H}px`,
    printBackground: true,
    pageRanges: "1",        // a slide that overflows must not silently become 2 pages
    margin: { top: "0", right: "0", bottom: "0", left: "0" },
  });
  written.push(out);
  console.log(`slide${String(i).padStart(2, "0")} -> ${out}`);
}

await browser.close();
console.log(`\n${written.length} pages in ${outDir}`);
console.log(`merge:  pdfunite ${path.join(outDir, "deckpdf_*.pdf")} <out>.pdf`);
