# design-system.md — the visual contract

Extracted from three presented decks: Session 1 (10 slides), Session 2 (14), Session 3 (14).
**Session 3 wins every disagreement.** It is the most evolved: bodies live in separate fragment
files (`slides/slideNN.body.html`) assembled by a generator, and its `<head>` is byte-identical to
Session 2's except for the `<title>`.

The shared `<head>` is not to be retyped. Copy `assets/boilerplate.html` (147 lines, doctype →
`<body>`) and replace `{{DECK_TITLE}}`. It is lifted byte-for-byte from Session 3 `slide1.html`.

---

## 1. File shape

One slide = one standalone HTML file. No build step, no framework, no bundler.

```
deck/
  index.html      meta-refresh to slide1.html
  slide1.html ... slideN.html
```

Each slide file is exactly: `boilerplate head` + `speaker-notes HTML comment` + `body fragment` +
`nav block` + `</body></html>`. Session 3's generator does this in one line:

```python
html = html_head + notes_comment(i) + load_body(i) + get_nav(i) + "</body></html>"
```

`index.html`, verbatim:

```html
<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=slide1.html"><title>How to Test AI Features - Test Cafe Session 3</title></head><body></body></html>
```

---

## 2. The canvas

| Rule | Value |
|---|---|
| Authoring target | 1920 × 1080, 16:9. Presenting checklist says `Screen at 1920x1080`. |
| Slide root element | `<div class="h-screen w-screen p-12 flex flex-col justify-center">` |
| Title slide only | `<div class="h-screen w-screen flex flex-col items-center justify-center relative overflow-hidden">` — no `p-12`, centred both axes |
| Padding convention | `p-12` = 48px on all four sides → 1824 × 984 of usable canvas |
| Body | `overflow: hidden; margin: 0` — a slide never scrolls. If content does not fit, cut content, do not scroll. |
| `html` | untouched outside `@media print` |
| Print canvas | `@page { size: 1920px 1080px; margin: 0 }` and `html, body { width: 1920px; height: 1080px }` |

13 of Session 3's 14 bodies open with the exact `p-12` root string. Fixed-pixel diagram layers are
allowed **inside** it, centred, e.g. `<div class="relative mx-auto animate-entry delay-2"
style="width:1700px;height:470px;">` with absolutely-positioned `glass-panel` cards and an
`<svg class="absolute inset-0 pointer-events-none">` overlay for connector lines and arrow markers.

---

## 3. Colour

### The six `:root` custom properties

```css
:root {
    --bg-color: #192b37;
    --accent-color: #ff5640;
    --roi-color: #FFD700;
    --success-color: #2ecc71;
    --warn-color: #e74c3c;
    --glass: rgba(255, 255, 255, 0.05);
}
```

Colour is **never decorative**. Each one means something and a slide that uses it decoratively is wrong.

| Var | Hex | Meaning |
|---|---|---|
| `--bg-color` | `#192b37` | The deep slate canvas. Also the *foreground* on gold (`.badge-roi { color: var(--bg-color) }`) and the stamp's own backing at 72% (`rgba(25,43,55,0.72)`). |
| `--accent-color` | `#ff5640` | Coral. **This deck's voice**: eyebrows, the rule, the boundary line, the thing under discussion. Default `glass-panel` left border. |
| `--roi-color` | `#FFD700` | Gold. **The payoff**: the money number, the conclusion strip, the pull-quote, "what would change our mind". Anything the audience should leave with. |
| `--success-color` | `#2ecc71` | Green. **It worked / it is sound.** Measured positives, gates that pass, the correct side of a comparison. |
| `--warn-color` | `#e74c3c` | Red. **It failed / it is a trap.** Refusals, crossed-out things, the dangerous option, the `stamp` border. |
| `--glass` | `rgba(255,255,255,0.05)` | The single panel fill. Every panel, no exceptions. |

Green `#2ecc71` and red `#e74c3c` are the only two greens/reds. Never introduce a second.

### The fifth tone: `#8fa3b0`

A muted blue-grey. It is **inline-only**. It is never a `:root` var, never a class, never a Tailwind
arbitrary value — in all three decks it appears only as `style="color:#8fa3b0;"`,
`style="border-left-color:#8fa3b0;"` or `style="background:#8fa3b0;"` (12 uses in S1, 17 in S2,
10 in S3). Session 3's generator names it `COLOR_MUTED = "#8fa3b0"` and then never interpolates it.

It marks **the old, neutral, or non-significant side of a comparison** — the thing that is not the
point: the previous session's artefact, the unchanged baseline, the input file at the start of a
pipeline, the ratio you are *not* asking them to remember, a bar that is context rather than
evidence. Promoting it to a var or a class would make it a first-class semantic like success/warn,
and it is deliberately the absence of one. If you find yourself wanting `--muted-color`, you are
about to give significance to something that has none.

```html
<div class="absolute glass-panel rounded-xl p-4" style="left:0px;top:0px;width:255px;height:130px;border-left-color:#8fa3b0;">
    <i class="fas fa-file-code text-2xl mb-2" style="color:#8fa3b0;"></i>
    <h3 class="text-lg font-bold leading-none font-mono">golden.yaml</h3>
    <p class="text-xs opacity-60 mt-2">20 rows &middot; validated on load</p>
</div>
```

### var() vs literal hex — a hard rule

`var(--…)` appears **only** inside the `<head>` `<style>` block, where the component classes are
defined. In slide bodies the count of `var(--` is **zero** across all 42 slides of all three decks.
Bodies write the literal hex, either as an inline style or as a Tailwind arbitrary value:

```html
<span style="color:#FFD700;">          <!-- inline style: 27 uses in S3 -->
<div class="text-[#ff5640] ...">        <!-- Tailwind arbitrary: 22 uses in S3 -->
```

Checkable: `grep -c 'var(--' slides/*.body.html` must be 0.

---

## 4. CDN dependencies — exactly three

```html
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=Fira+Code&display=swap" rel="stylesheet">
```

- Tailwind Play CDN — no config, no build, arbitrary values (`text-[#ff5640]`, `text-[11px]`) work.
- Font Awesome **6.5.0** from cdnjs — pinned version. Icons are `<i class="fas fa-…">`.
- IBM Plex Sans at weights **300/400/600/700**, plus **Fira Code** for all mono.

**Consequence: the deck requires network at presentation time.** The presenting checklist carries
`□ Internet reachable (Tailwind, Font Awesome and the fonts come from CDNs)` and the failure row
`| No internet — deck renders unstyled | Open the PDF. Say so out loud, then carry on |`. That is
the entire reason the `@media print` block in §7 exists and why a PDF sits next to the deck
(`RLM-TestCafe-Session3.pdf`). Do not add a fourth CDN; do not vendor these instead — the PDF is
the offline story.

---

## 5. Type scale

Sans is IBM Plex Sans (body default). Mono is Fira Code, reached with Tailwind's `font-mono`.
Hierarchy is carried by **size + opacity**, not by colour.

| Role | Exact classes | When |
|---|---|---|
| Eyebrow (title slide) | `mb-4 text-[#ff5640] font-mono tracking-widest uppercase` | Once, slide 1. No `text-sm`. |
| Eyebrow (content slide) | `mb-3 text-[#ff5640] font-mono tracking-widest uppercase text-sm animate-entry` | First line of every content slide. Names the *register* of the slide, not its content. |
| H1 | `text-7xl font-bold mb-6` | Title slide only. Exactly one per deck. |
| H2 | `text-5xl font-bold mb-2 animate-entry` | The slide headline. Every content slide. 13/13 in S3 — no variation. |
| Subtitle | `text-xl opacity-70 mb-6 animate-entry delay-1` | One sentence under the H2. `mb-4`/`mb-5` when the slide is dense; `text-lg` when the sentence is long. |
| Card `h3` | `text-xl font-bold` (default) · `text-2xl font-bold` (two-card slides) · `text-lg font-bold leading-none font-mono` (diagram node = a filename or function) · `text-base font-bold` (dense strips) | Panel headings. |
| Body copy | `text-sm opacity-85` / `text-base` / `text-sm opacity-80` | Inside panels. `leading-relaxed` when > 2 lines. |
| Micro-label | `text-[11px] font-mono uppercase tracking-widest opacity-40` (or `opacity-50`) | Column headers, provenance tags, "whether the row is a test". |
| Footnote / receipt | `text-xs font-mono opacity-40` … `opacity-55` | Where the number came from. File paths, paper IDs, caveats. Usually `mt-3`/`mt-4` under the thing it qualifies. |
| Big stat | `font-mono text-2xl font-bold text-[#FFD700]` (S3) · `text-4xl font-bold` + `style="color:#FFD700;"` (S2) | The number you want remembered. Colour picks its meaning (gold = payoff, coral = ours, `#8fa3b0` = the one that does not matter). |
| Code | `.code-block` wrapper + `p-3 text-xs leading-relaxed` (common) / `p-5 text-sm leading-relaxed` (hero) | See §6. |
| Badge | `<span class="badge badge-accent\|badge-success\|badge-roi\|badge-warn">` | Short label pinned to a panel: `Session 2`, `R1`, `(a)`. |
| Slide counter | `text-sm opacity-40 font-mono` | Inside the nav block, never authored by hand. |

Emphasis inside body copy is `<b>`. Inline code inside prose is `class="font-mono"` or
`class="font-mono font-bold"`, not `<code>`. Typographic entities are spelled out —
`&mdash; &middot; &ldquo; &rdquo; &rsquo; &times; &ndash; &amp;` — never raw UTF-8 punctuation.

---

## 6. Components (defined in the boilerplate head)

| Class | What it is |
|---|---|
| `.glass-panel` | `--glass` fill, `blur(10px)`, 1px white-10% border, **4px coral left border**. The default panel. |
| `.glass-panel-alt` | Same, gold left border. Conclusions, quotes, payoff. |
| `.glass-panel-success` | Same, green left border. |
| `.glass-panel-warn` | Same, red left border. |
| `.code-block` | Fira Code, `background:#0d161c`, `border-radius:8px`, `border:1px solid #333`. |
| `.badge` / `-accent -success -roi -warn` | Pill, `4px 12px`, `border-radius:20px`, bold, `0.85em`. `badge-roi` is gold-on-`--bg-color`. |
| `.nav-btn` | `opacity:0.5`, hover → `opacity:1; scale(1.1); color: var(--accent-color)`. |
| `.stamp` | Absolute, `rotate(-11deg)`, 3px red border, red text, `letter-spacing:0.18em`, backing `rgba(25,43,55,0.72)`. Overprints a card that looks fine but is not. |
| `.mcp-packet` | 12px coral dot with glow, riding the `dataFlow` keyframe along a connector. |
| `.chev`, `.card-press` | Micro-transitions. `.card-press:active { transform: scale(0.98) }`. |
| `.print-only` / `.print-hide` | `display:none` by default; swapped in `@media print`. For a `<video>`/live widget on screen with a poster image + caption in the PDF. |

Panels are always given a radius and padding by Tailwind at the call site, not by the class:
`class="glass-panel-success p-6 rounded-xl"` / `p-5` / `p-4`.

A `border-left-color` override on a `glass-panel` is the sanctioned way to get the muted tone:
`<div class="glass-panel p-5 rounded-xl" style="border-left-color:#8fa3b0;">`.

Stamp, verbatim from Session 3:

```html
<div class="stamp text-lg" style="left:28px;bottom:20px;">ASSERTS NOTHING</div>
```

Code block, verbatim from Session 3 slide 4 — note the fake window chrome, the `pl-4` indent
divs, and that syntax colour is inline hex:

```html
<div class="col-span-3 code-block overflow-hidden">
    <div class="flex items-center gap-2 px-4 py-2" style="background:rgba(255,255,255,0.04);border-bottom:1px solid #333;">
        <div class="w-3 h-3 rounded-full bg-red-500"></div>
        <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
        <div class="w-3 h-3 rounded-full bg-green-500"></div>
        <span class="ml-2 text-xs opacity-50">harness/golden.py &middot; the real dataclass, no simplification</span>
    </div>
    <div class="p-5 text-sm leading-relaxed">
        <div class="opacity-70">@dataclass(frozen=True)</div>
        <div>class Row:</div>
        <div class="pl-4">id: str</div>
        <div class="pl-4" style="color:#ff5640;">provenance: str<span class="opacity-60 ml-3"># required &mdash; R2, in the type</span></div>
        <div style="color:#e74c3c;">GoldenError: R21: expected value came from the model under test</div>
    </div>
</div>
```

Table-as-grid (there are no `<table>` elements anywhere in any deck) — Session 3 slide 13:

```html
<div class="glass-panel rounded-xl overflow-hidden animate-entry delay-2" style="border-left-color:#8fa3b0;">
    <div class="grid grid-cols-12 px-6 py-2 text-[11px] font-mono uppercase tracking-widest opacity-40" style="background:rgba(255,255,255,0.04);">
        <div class="col-span-3">Not built</div>
        <div class="col-span-5">Why &mdash; the measured reason</div>
        <div class="col-span-4">What would change our mind</div>
    </div>
    <div class="grid grid-cols-12 px-6 py-2 items-center" style="border-top:1px solid rgba(255,255,255,0.07);">
        <div class="col-span-3 font-bold text-base">No reviewer agent, no critic, no self-check pass</div>
        <div class="col-span-5 text-sm opacity-80">This exact pattern is measured to <b>collapse</b> (2402.08115). The mutation gate is the reviewer.</div>
        <div class="col-span-4 text-sm opacity-70 font-mono" style="color:#FFD700;">a critic that measurably raises kill rate on a held-out mutant class</div>
    </div>
</div>
```

Layout grids in use: `grid-cols-2 gap-8`, `grid-cols-3 gap-4`, `grid-cols-5 gap-8` (with
`col-span-2` / `col-span-3`), `grid-cols-12` for tables. Nothing else.

---

## 7. Animation

Five keyframes, three animation classes, four delays. Verbatim:

```css
@keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }
@keyframes rotateGlow { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes dataFlow { 0% { left: 0%; opacity:0; } 10% { opacity:1; } 90% { opacity:1; } 100% { left: 100%; opacity:0; } }

.animate-float { animation: float 6s ease-in-out infinite; }
.animate-entry { animation: fadeIn 0.8s ease-out forwards; opacity: 0; }
.animate-pulse { animation: pulse 2s ease-in-out infinite; }
.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }
.delay-3 { animation-delay: 0.6s; }
.delay-4 { animation-delay: 0.8s; }
```

| Class | Use |
|---|---|
| `.animate-entry` | Every top-level block on a slide. Starts at `opacity: 0` and `forwards`-holds the end state. **Anything without it is invisible on load — and anything with it is invisible in a PDF unless §8 freezes it.** |
| `.animate-float` | The oversized ghost icon behind a title slide: `<i class="fas fa-flask absolute text-[400px] opacity-5 text-white animate-float -z-10"></i>` |
| `.animate-pulse` | A live/blinking indicator. Sparingly. |
| `.mcp-packet` | Consumes `dataFlow`; the only user of it. |
| `rotateGlow` | Declared in all three decks; used by none. Keep it — the head is copied verbatim. |

**Stagger follows reading order.** The eyebrow and H2 carry bare `animate-entry` (delay 0), the
subtitle `delay-1`, the main content block `delay-2`, supporting strips `delay-3`, the closing
payoff panel `delay-4`. Delays are applied to the *container*, not to each child — one
`animate-entry delay-2` on a `grid`, not four on its cards. Never run a `delay-3` element above a
`delay-1` element on the page. Four is the ceiling; if a slide needs a fifth beat, it is two slides.

---

## 8. Print / PDF

Session 1 has **no** print CSS and no `.stamp`. Sessions 2 and 3 both carry the block below on all
14 slides — it is one of the two things Session 2 added, and Session 3 inherits it unchanged.
(The generator's own comment: *"Identical to Session 2's head except for the `<title>`."*)

Verbatim, comment included:

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

Why each part exists:

| Rule | Reason |
|---|---|
| `@page { size: 1920px 1080px; margin: 0 }` | Forces one landscape 16:9 page per slide with no printer margin. Without it Chrome reflows to A4 portrait. |
| `html, body { background: … !important }` twice | Chrome does not paint the canvas background in print. Both `background` and `background-color` are set because the shorthand and the longhand are not interchangeable against the UA print sheet. Without this the whole deck prints white on white. |
| `width/height: 1920px/1080px` | Pins the print viewport so `vw`/`vh`-derived layout does not resolve against the paper box. |
| `overflow: hidden !important` | Stops a 1-pixel overflow becoming a blank second page per slide. |
| `*, *::before, *::after { print-color-adjust: exact }` | Chrome drops backgrounds and light-on-dark text in print by default. It must be forced on **everything**, including pseudo-elements, or the glass panels and badges vanish. `-webkit-` prefix retained for older Chrome. |
| `.animate-entry { animation: none; opacity: 1; transform: none }` | `.animate-entry` declares `opacity: 0` in its base rule. Print does not reliably run animations, so without this every staggered block prints blank or mid-fade at `translateY(20px)`. |
| `.animate-float, .animate-pulse, .mcp-packet { animation: none }` | Freezes the looping decorations at frame 0 instead of an arbitrary phase. |
| `.h-screen`, `.w-screen` overrides | Tailwind emits `100vh`/`100vw`; in print `vh` is the paper height, which is close but not exact. Pinning to the authoring canvas keeps the PDF pixel-identical to the screen. |
| `.print-hide` / `.print-only` | The swap that lets a video or live widget on screen become a poster image plus a caption in the PDF (Session 2 slide 11). `.print-only { display: none }` sits **outside** the media query. |

---

## 9. Nav block

Appended to every slide by the generator; never hand-authored. Verbatim (`slide1.html`):

```html
    <div class="absolute bottom-6 right-8 flex items-center gap-6 z-50">
        <span class="text-sm opacity-40 font-mono">SLIDE 01 / 14</span>
        <a href="#" class="nav-btn text-2xl"><i class="fas fa-chevron-left"></i></a>
        <a href="slide2.html" class="nav-btn text-2xl"><i class="fas fa-chevron-right"></i></a>
    </div>
    <script>
      var PREV = "#", NEXT = "slide2.html";
      document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
          if (NEXT !== '#') { e.preventDefault(); location.href = NEXT; }
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
          if (PREV !== '#') { e.preventDefault(); location.href = PREV; }
        } else if (e.key === 'Home') {
          location.href = 'slide1.html';
        } else if (e.key === 'End') {
          location.href = 'slide14.html';
        }
      });
    </script>
```

Counter is zero-padded two digits (`{slide_id:02d}`); first slide's prev and last slide's next are
both `"#"` and inert.

Speaker notes ride in the file as an HTML comment placed between `<body>` and the slide root:

```html
<!--
SPEAKER NOTES - SLIDE 01: Title

...prose, with every "--" collapsed to "-" so it cannot close the comment...
-->
```

---

## 10. Slide anatomy — the canonical content slide

```html
<div class="h-screen w-screen p-12 flex flex-col justify-center">
    <div class="mb-3 text-[#ff5640] font-mono tracking-widest uppercase text-sm animate-entry">Where Sessions 1 &amp; 2 Left Us</div>
    <h2 class="text-5xl font-bold mb-2 animate-entry">Same Problem, No Pixels to Diff</h2>
    <p class="text-xl opacity-70 mb-6 animate-entry delay-1">Session 2's conclusion: the deliverable is not the test, it is the gate record. Here is what that costs when the output is a paragraph instead of a screenshot.</p>

    <div class="grid grid-cols-2 gap-8 animate-entry delay-2">
        <div class="glass-panel-success p-6 rounded-xl">
            <div class="flex items-center gap-3 mb-4">
                <span class="badge badge-success">Session 2</span>
                <h3 class="text-2xl font-bold">What Session 2 Got for Free</h3>
            </div>
            <ul class="space-y-3 text-base">
                <li class="flex gap-3"><i class="fas fa-check mt-1" style="color:#2ecc71;"></i><span>The equivalence guard came free: if a mutation moved <b>0 px</b>, the mutant is equivalent. A decision, not a judgement.</span></li>
            </ul>
        </div>
        <div class="glass-panel-warn p-6 rounded-xl">
            <div class="flex items-center gap-3 mb-4">
                <span class="badge badge-warn">Session 3</span>
                <h3 class="text-2xl font-bold">What Text Does Not Have</h3>
            </div>
            <ul class="space-y-3 text-base">
                <li class="flex gap-3"><i class="fas fa-times mt-1" style="color:#e74c3c;"></i><span>There is no <span class="font-mono font-bold">pixelmatch</span> for meaning.</span></li>
            </ul>
        </div>
    </div>

    <div class="mt-4 text-xs font-mono opacity-40 animate-entry delay-3">Session 2 &middot; viz/runs/gates-proof/events.jsonl &middot; the guard fired 0 times in that run &mdash; architecturally present, empirically unexercised</div>

    <div class="glass-panel-alt p-5 rounded-xl mt-4 animate-entry delay-4">
        <p class="text-lg"><i class="fas fa-quote-left mr-2 opacity-60" style="color:#FFD700;"></i>Session 2 could ask <b>did it move?</b> Tonight we have to ask <b>is it right?</b> &mdash; a different question, with a worse answer, and the one our profession has argued about since before any of us started.</p>
    </div>
</div>
```

Order is fixed: **eyebrow → H2 → subtitle → evidence → receipt line → gold payoff panel.**
A green panel and a red panel side by side is the house comparison; `fa-check`/`fa-times` with
inline `#2ecc71`/`#e74c3c` are the house list bullets. The last block on a slide is almost always a
`glass-panel-alt` (gold) carrying the one sentence to remember, at `text-lg` or `text-xl font-bold`.

The eyebrow may take a different colour to set the slide's register — Session 3 uses `#e74c3c` for
the self-criticism slide ("The Adversarial Review of My Own Harness") and `#FFD700` for the
scope slide ("Scope, With Triggers"). Coral otherwise: 12 of 14.

---

## 11. How to tell you got it wrong

- A slide scrolls, or content is clipped at 1920×1080. `p-12` + `justify-center` + `overflow:hidden` means it must fit.
- `var(--accent-color)` appears in a slide body. Bodies use literal hex.
- `#8fa3b0` was promoted to `:root`, to a class, or to `text-[#8fa3b0]`.
- A colour appears that is not one of the six vars, `#8fa3b0`, `#0d161c` (code-block fill), `#333` (code-block border), or a white/black alpha.
- A block has no `animate-entry` (it will sit there dead while everything else fades in), or a `delay-3` block sits above a `delay-1` block.
- `delay-5` or greater, or per-child delays inside a grid.
- A `<table>`, a `<code>`, a raw `—`/`·`/`"` instead of `&mdash;`/`&middot;`/`&ldquo;`.
- More than one `<h1>` in the deck, or an `<h2>` that is not `text-5xl font-bold mb-2 animate-entry`.
- The PDF prints white, or prints blank slides: the `@media print` block is missing or incomplete.
- A fourth CDN, a `<link>` to a local stylesheet, or a shared `deck.css`. Every slide is standalone; the head is duplicated into each file on purpose.
- Font Awesome pinned to something other than 6.5.0, or an icon that is not `fas`.
- Gold used for something that is not the payoff, or green/red used for something that was not measured.

---

## 12. Where the decks disagree

| Thing | S1 | S2 | S3 | Winner |
|---|---|---|---|---|
| `@media print` block | absent | on all 14 | on all 14 | S3 (= S2) — **required** |
| `.stamp` | absent | present | present | S3 — present |
| Bodies in separate fragment files | no | no | yes (`slides/slideNN.body.html`) | S3 |
| Big stat | `text-4xl font-bold` + inline hex | same | `font-mono text-2xl font-bold text-[#FFD700]` | S3 for new decks; S2's form is fine for a hero ratio |
| Deck length | 10 | 14 | 14 | 14 |

Everything else in the head is byte-identical across all three.
