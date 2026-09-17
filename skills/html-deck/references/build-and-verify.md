# Build and verify

Mechanics only. Style lives in `design-system.md` and `components.md`.

Source decks: `RLM Test Cafe` (S1, 10 slides), `RLM Test Cafe Session 2` (S2, 14), `RLM Test Cafe
Session 3` (S3, 14). **S3 wins every disagreement** — it is the only one whose bodies live in separate
fragment files, and its head is S2's head with a different `<title>`.

---

## 1. File layout

```
my-talk/
  generate_deck.py                  the whole build; ~300 lines, stdlib only
  slides/
    slide01.body.html               ZERO-PADDED fragments, plain HTML
    slide02.body.html
    …  slide14.body.html
  deck/
    index.html                      one line, meta-refresh to slide1.html
    slide1.html                     1-INDEXED, NOT zero-padded
    slide2.html
    …  slide14.html
  SPEAKER_NOTES.md                  emitted, sibling of deck/ — never hand-edited
```

Two numbering conventions, on purpose, and they do not match:

| Thing | Format | Example |
|---|---|---|
| Fragment on disk | zero-padded | `slides/slide07.body.html` |
| Emitted slide | not padded | `deck/slide7.html` |
| On-screen counter | zero-padded | `SLIDE 07 / 14` |

The emitted names are unpadded because the nav writes `slide{n-1}.html` / `slide{n+1}.html` by
arithmetic. The fragments are padded so `ls slides/` sorts correctly past nine.

`deck/` is self-contained and deployable: every asset is either inline or an absolute CDN URL. If a slide
needs a local file (S2 slide 11 has a video), it goes in `deck/media/` and is referenced relatively, so
`file://`, a USB stick and a static host all work.

### deck/index.html

Verbatim from S3 (S1 and S2 are identical except the title). It is **one line, 169 bytes**, not three:

```html
<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=slide1.html"><title>How to Test AI Features - Test Cafe Session 3</title></head><body></body></html>
```

---

## 2. Why bodies live in separate files

S1 and S2 built each body as a Python lambda returning an f-string:

```python
slides_content[6] = lambda: f"""
    <div class="h-screen w-screen p-12 flex flex-col justify-center">
        <div class="mb-3 text-[{COLOR_ACCENT}] font-mono tracking-widest uppercase text-sm animate-entry">The Build</div>
```

Note `{COLOR_ACCENT}`: in S1/S2 the colour constants were interpolated into every body. S3's fragments
write `#ff5640` literally instead. Same output.

That works until a body contains a literal `{` or `}`. Slide bodies contain plenty:

- inline `<svg>` with `<marker>` / `viewBox` is fine, but any `<style>` or `<script>` inside a body is not
- Tailwind arbitrary values — `text-[#ff5640]`, `w-[1700px]` — are fine, but adjacent CSS in a `style`
  attribute with a function call is a constant hazard
- S2 slide 11 had to be written as a **plain** `lambda: """…"""` instead of an f-string precisely because
  it carries a `<script>` block full of braces

In an f-string every one of those braces has to be doubled. Get one wrong and you get a `ValueError` at
import time, or worse, silent interpolation.

S3 moved them out:

```python
def load_body(slide_id):
    path = os.path.join(BODIES_DIR, f"slide{slide_id:02d}.body.html")
    if not os.path.exists(path):
        return (f"<div class='h-screen w-screen flex items-center justify-center'>"
                f"<h1 class='text-4xl opacity-40'>Slide {slide_id} &mdash; not written yet</h1></div>")
    with open(path, encoding="utf-8") as f:
        return f.read()
```

A fragment is now plain HTML: no escaping, editor syntax highlighting works, and two people can write
two slides without touching the same file. **The emitted deck is byte-identical either way** — this is a
change to the authoring ergonomics, nothing else.

The missing-body placeholder matters: an unwritten slide still renders and still navigates, so you can
generate and click through the deck from slide one onward.

A fragment is **only** the outer wrapper div and its content. No `<head>`, no `<style>`, no nav, no
`</body>`. It starts at `<div class="h-screen w-screen …">` and ends at its matching `</div>`.

If a fragment does carry its own `<script>` (S2 slide 11 only), it is emitted **before** the nav script,
so its `keydown` listener runs first and `stopImmediatePropagation()` can take the keys away from the
deck. S2's own comment:

```js
// registered before get_nav's listener, so stopImmediatePropagation wins
```

---

## 3. The generator

`assets/generate_deck.py`. Set the CONFIG block, fill `SLIDE_TITLES` and `SPEAKER_NOTES`, run it.

Every slide is exactly five pieces concatenated, in this order:

```python
html = html_head + notes_comment(i) + load_body(i) + get_nav(i) + "</body></html>"
```

| Piece | What it is |
|---|---|
| `html_head` | `<!DOCTYPE>` … `<body>` — CDN links, `:root` tokens, all component CSS, print CSS. Identical on every slide. A plain string, never an f-string. |
| `notes_comment(i)` | `<!-- SPEAKER NOTES - SLIDE 07: … -->` |
| `load_body(i)` | `slides/slideNN.body.html` |
| `get_nav(i)` | counter + chevrons + keyboard script |
| `"</body></html>"` | literal |

`html_head` is a plain `"""…"""` with a comment saying why:

```python
# NOTE: plain string, not an f-string. The colour literals are written out so that
# Tailwind/CSS braces can never collide with f-string interpolation.
```

The parameterised version substitutes the title with `.replace("__PAGE_TITLE__", PAGE_TITLE)` rather
than switching to an f-string, for the same reason.

### The nav cluster is generated, never hand-written

Verbatim from S3 (identical in S1 and S2):

```python
def get_nav(slide_id):
    prev_link = f"slide{slide_id - 1}.html" if slide_id > 1 else "#"
    next_link = f"slide{slide_id + 1}.html" if slide_id < TOTAL_SLIDES else "#"
    return f"""
    <div class="absolute bottom-6 right-8 flex items-center gap-6 z-50">
        <span class="text-sm opacity-40 font-mono">SLIDE {slide_id:02d} / {TOTAL_SLIDES}</span>
        <a href="{prev_link}" class="nav-btn text-2xl"><i class="fas fa-chevron-left"></i></a>
        <a href="{next_link}" class="nav-btn text-2xl"><i class="fas fa-chevron-right"></i></a>
    </div>
    <script>
      var PREV = "{prev_link}", NEXT = "{next_link}";
      document.addEventListener('keydown', function (e) {{
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
          if (NEXT !== '#') {{ e.preventDefault(); location.href = NEXT; }}
        }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
          if (PREV !== '#') {{ e.preventDefault(); location.href = PREV; }}
        }} else if (e.key === 'Home') {{
          location.href = 'slide1.html';
        }} else if (e.key === 'End') {{
          location.href = 'slide{TOTAL_SLIDES}.html';
        }}
      }});
    </script>
    """
```

and what it emits, verbatim from `deck/slide7.html`:

```html
    <div class="absolute bottom-6 right-8 flex items-center gap-6 z-50">
        <span class="text-sm opacity-40 font-mono">SLIDE 07 / 14</span>
        <a href="slide6.html" class="nav-btn text-2xl"><i class="fas fa-chevron-left"></i></a>
        <a href="slide8.html" class="nav-btn text-2xl"><i class="fas fa-chevron-right"></i></a>
    </div>
```

Do not put a nav cluster, a counter or a keyboard handler in a fragment. Slide 1's back arrow and the
last slide's forward arrow are `href="#"` — dead on purpose, so the deck has ends.

### The three hardcoded slide counts

`TOTAL_SLIDES` is one constant in the generator but reaches the emitted HTML of **every** slide three
times:

| # | Where | Emitted as | Wrong if stale |
|---|---|---|---|
| 1 | `next_link` guard, `slide_id < TOTAL_SLIDES` | `href="slide15.html"` on the last slide | forward arrow walks off the end into a 404 |
| 2 | the counter | `SLIDE 07 / 14` | every slide displays the wrong denominator |
| 3 | the `End` key target | `location.href = 'slide14.html'` | End jumps to a missing file |

So **fix the slide count before you write any files**, and after any change to it re-run the generator
over the *whole* deck. Emitting only the new slide leaves thirteen slides saying `/ 14` and one saying
`/ 15`. The generator is idempotent and takes under a second; there is never a reason to partially
regenerate.

Renumbering is not just the nav, either: bodies and speaker notes in S3 refer to slides by number in
prose — "tell them slide 13 is for them", "both of these rules were enforced by a paragraph in the
README until slide 12", "slide 11 is the measurement that justifies it". Those are hand-written and the
generator cannot fix them. `grep -rn "slide [0-9]" slides/ generate_deck.py` after any renumber.

### Speaker notes

One source, two destinations.

1. An HTML comment immediately after `<body>`, before the body div — so `view-source:` on a slide, or a
   `grep` over `deck/`, carries the notes with the slide:

```python
def notes_comment(slide_id):
    body = SPEAKER_NOTES.get(slide_id, "").replace("--", "-")
    return f"<!--\nSPEAKER NOTES - SLIDE {slide_id:02d}: {SLIDE_TITLES.get(slide_id, '')}\n\n{body}\n-->\n"
```

   The `.replace("--", "-")` is not cosmetic: `--` inside an HTML comment is invalid and ends the
   comment early in some parsers, which would dump your notes onto the slide. Consequence: **never write
   an em dash as `--` in `SPEAKER_NOTES`**, it will be silently rewritten. In notes use the word or a
   comma; in slide bodies use `&mdash;`.

2. `SPEAKER_NOTES.md`, written to `os.path.dirname(OUTPUT_DIR)` — i.e. next to `deck/`, not inside it,
   so the notes never deploy with the deck. Header, then one section per slide:

```markdown
# How to Test AI Features: Building an Evaluation Harness in pytest

**Test Cafe - Session 3 of the RLM-Driven Automation series** | Andrei Margelatu | AI Engineer @ Endava

Hands-on, laptops open. Navigation: arrow keys, space, or PageUp/PageDown. `deck/index.html` opens slide 1.

Theory: slides 2-6. Build: 7-9. The judge: 10-12. Critical thinking: 13-14.

---

## Slide 01 - Title

Say plainly that this is the third of the series and the first one where the thing being tested is the
thing everyone in the room has already been asked about. …

---
```

Notes are prose wrapped at ~110 columns, addressed to the speaker in the imperative ("Walk the ladder
from the bottom and do not rush it"), and they say what to do when short of time ("If you are behind
time, take it out of slide 5, never out of this one"). They are not a transcript of the slide.

`SPEAKER_NOTES.md` is generated. Edit the dict, re-run, never edit the `.md`.

---

## 4. The verification loop — mandatory

This is the part that separates the skill from guessing. The canvas is exactly 1920×1080 with
`body { overflow: hidden }`: anything past the edge is not scrolled to, it is **gone**, and you will not
find out until you are on stage. S2's own pre-flight checklist carries the scar:

```
□  Screen at 1920x1080  (slide 6 overflows on a 1440-wide screen)
```

Estimating the vertical budget from the markup was wrong about half the time on the source decks. Render
it.

Calibration, so you know the checker is not vacuous: it reports 14/14 clean on S3's shipped `deck/`, and
goes red on each of three hand-made mutants — a card moved to `left:1800px` (4 elements outside, canvas
2165×1080), a 900px block inserted into slide 9 (canvas 1920×1290, 18 elements outside), and 16 words
dropped into a `height:20px; overflow:hidden` box (clipped by 4px). A check that has never gone red is
not a check.

```bash
node assets/verify.mjs <deck-dir> <slide-count>
node assets/verify.mjs ~/talk/deck 14
```

Prints one line per slide, writes `<deck-dir>/../shots/slideN.png`, exits non-zero if anything overflows.
Re-run after **every** edit — two extra words of copy can push a card off the slide.

The full script (`assets/verify.mjs`):

```js
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
```

Three checks, and why each exists:

| Check | Catches |
|---|---|
| `documentElement.scrollWidth/scrollHeight` vs 1920×1080 | the whole-slide case: a body taller than the canvas |
| per-element rect outside the canvas, ignoring clipped descendants | one card or one absolutely-positioned SVG off the edge. The clipped-ancestor filter is required or slide 1's `text-[400px]` background flask, which sits inside an `overflow-hidden` wrapper, reports as a 400px overflow on every deck |
| `scrollHeight > clientHeight` inside an `overflow:hidden` box | text silently cut off inside a fixed-height card — `style="width:255px;height:130px"` cards are everywhere in these decks and they clip without any visible symptom |

Prerequisites, and the failure modes if you skip them:

- `npm i -D playwright && npx playwright install chromium`, in the directory you run the check from or
  any parent. Node ESM ignores `NODE_PATH`, which is why both scripts resolve playwright through
  `createRequire` instead of a bare `import`.
- **Network.** Tailwind, Font Awesome and the Google Fonts are CDN `<link>`s. Offline, every slide renders
  unstyled, nothing overflows, and the run is meaningless green. The `waitUntil: "networkidle"` plus
  `document.fonts.ready` is what makes the measurement reflect the real type metrics — the deck is laid
  out in IBM Plex Sans and measuring it in the fallback font is measuring a different deck.
- The `FREEZE` stylesheet. `.animate-entry { opacity: 0 }` until its animation runs; without freezing you
  screenshot a deck mid-fade and half the elements are invisible.

### Then look at the screenshots

Non-negotiable, and it is a separate step from the exit code. The checker is geometry only. It cannot see:

- a `.stamp` (`position:absolute; rotate(-11deg)`) landing on top of body copy — it overlaps without
  overflowing. Fix: bottom-anchor the stamp and reserve a padding lane in the card.
- a bar chart whose bar widths contradict the numbers printed next to them
- gold-on-coral, or `opacity-40` body text that dies on a projector
- an eyebrow in the wrong semantic colour
- a duplicated headline, or a card that renders but says nothing

Open every PNG. On the source decks this is where the real defects were found.

---

## 5. PDF export

The deck fetches Tailwind, Font Awesome and its fonts from CDNs at page-load time. Venue wifi fails. The PDF is the stage fallback and it is not
optional for a talk that matters — both S2 and S3 ship one next to the deck
(`RLM-TestCafe-Session3.pdf`, 2.2 MB).

```bash
node assets/export_pdf.mjs <deck-dir> <slide-count> [out-dir]
node assets/export_pdf.mjs ~/talk/deck 14

pdfunite /tmp/deckpdf_*.pdf ~/talk/My-Talk.pdf                    # poppler: brew install poppler
qpdf --empty --pages /tmp/deckpdf_*.pdf -- ~/talk/My-Talk.pdf     # alternative
```

Files are written `deckpdf_01.pdf … deckpdf_14.pdf`. Zero-padding is load-bearing: the shell glob is
lexical, so `deckpdf_1, deckpdf_10, deckpdf_2` would merge the deck out of order.

This is not a reconstruction: run against S3's `deck/` and merged with `pdfunite`, it reproduces
`RLM-TestCafe-Session3.pdf` at the same 2,202,125 bytes, differing only in the trailer `/ID`. Page
`/MediaBox` is `[0 0 1440 810]` — 1920×1080 CSS px at 72/96.

The full script (`assets/export_pdf.mjs`):

```js
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
```

The export only works because the head carries a print block. Its own comment explains the two traps:

```css
        /* ---- PRINT / PDF EXPORT -------------------------------------------------
           Chrome does NOT paint the canvas background in print: without the
           html/body rule below the whole deck prints WHITE. print-color-adjust
           must be forced on everything, and .animate-entry starts at opacity 0
           so it has to be frozen or slides render mid-fade. */
        .print-only { display: none; }
        @media print {
            @page { size: 1920px 1080px; margin: 0; }
            html, body {
                background: #192b37 !important;
                background-color: #192b37 !important;
                width: 1920px; height: 1080px;
                overflow: hidden !important;
            }
            *, *::before, *::after {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .animate-entry {
                animation: none !important;
                opacity: 1 !important;
                transform: none !important;
            }
            .animate-float, .animate-pulse, .mcp-packet { animation: none !important; }
            .h-screen { height: 1080px !important; }
            .w-screen { width: 1920px !important; }
            .print-hide { display: none !important; }
            .print-only { display: block !important; }
        }
```

`.h-screen`/`.w-screen` are overridden because in print media Tailwind's `100vh` is the *page* box, not
the 1080px you asked for. `.print-hide` / `.print-only` are the escape hatch for anything that cannot
survive paper: S2 slide 11 swaps its `<video>` for the poster JPEG with exactly this pair.

`page.pdf()` is headless-Chromium-only. `pageRanges: "1"` is a second overflow alarm — if a slide grew
past 1080px you get a truncated page rather than a silently two-page slide.

---

## 6. Serving locally

`file://` is enough for a deck with no local media. For anything with `deck/media/`, or to rehearse the
way the audience will see it:

```bash
cd deck && python3 -m http.server 8080
# http://localhost:8080/  -> index.html -> slide1.html
```

No other server is needed and there is nothing to build. Reloading after a `generate_deck.py` run is
enough; there is no watcher and no cache to bust.

---

## 7. Deploy (optional)

`deck/` is plain static files — any static host works: GitHub Pages, Netlify, S3, a nginx directory, a
USB stick. Nothing below is required to present.

The source decks use Azure Storage static websites, one storage account shared across all three sessions,
each session in its own prefix (S3's `deploy.sh`):

- `set -euo pipefail`, `az account set -s "$SUB"`, `az group create` (idempotent by design)
- the account name is **derived, not stored**: `BASE="stendavatestcafe"` plus
  `SUFFIX=$(printf '%s' "$SUB$RG" | shasum | cut -c1-6)`, so every session's script computes the same
  name and they share one site
- create the account only if `az storage account show` fails; otherwise reuse it
- authenticate with the account key from `az storage account keys list`, because "Owner grants the
  management plane, not the data plane"
- `az storage blob service-properties update --static-website --index-document index.html
  --404-document index.html`
- `az storage blob upload-batch -d '$web' --destination-path "$PREFIX" -s "$SRC" --overwrite`, where
  `PREFIX=session3` keeps the session in its own folder and `--overwrite` makes re-runs idempotent
- print the public URL, `${WEB}${PREFIX}/index.html`, and the single-session teardown command

The two transferable ideas, whatever the host: **one prefix per deck so a redeploy never disturbs an
older talk**, and **a re-runnable script rather than a drag-and-drop**, because you will redeploy after
the last-minute fix on the morning of the talk.

---

## 8. Checklist

```
□  TOTAL_SLIDES fixed before any file was written
□  generate_deck.py run; all N slides + index.html + SPEAKER_NOTES.md present
□  verify.mjs exits 0 for all N slides
□  every screenshot opened and looked at
□  PDF exported, merged in order, and page count == N
□  no literal "--" in SPEAKER_NOTES; em dashes in slide bodies written as &mdash;
□  claims-to-slide-number references in prose still correct after any renumber
□  deck/ opens from file:// with no console errors
```

---

## Where the three decks disagree

| | S1 | S2 | S3 |
|---|---|---|---|
| Slides | 10 | 14 | 14 |
| Bodies | inline Python lambdas | inline Python lambdas | `slides/slideNN.body.html` **← use this** |
| Generator size | 83 KB | 117 KB | 30 KB + 14 fragments |
| Print/PDF CSS | **absent** | present | present |
| `.stamp` CSS | absent | present | present |
| `--` colour vars | 5 | 5 | 5 + `COLOR_MUTED` constant |
| Head otherwise | identical | identical | identical |
| `get_nav`, `notes_comment` | identical | identical | identical |
| `generate_slides` | same loop; body from `slides_content[i]()` | same | body from `load_body(i)` |
| Local media | none | `deck/media/` (video + poster) | none |

Everything else — the head, the nav, the notes convention, `index.html`, the `SPEAKER_NOTES.md` layout —
is the same three times over. Copy S3.
