# Layout archetypes

Catalogue of every distinct slide layout used across the three decks. Source of truth:

| Deck | Path | Slides | Bodies live in |
|---|---|---|---|
| S1 | `RLM Test Cafe/deck/` | 10 | the slide HTML itself |
| S2 | `RLM Test Cafe Session 2/deck/` | 14 | the slide HTML itself |
| S3 | `RLM Test Cafe Session 3/deck/` | 14 | `../slides/slideNN.body.html`, assembled by `../generate_s3_deck.py` |

S3 is the most evolved and wins every disagreement. Citations below are `S2/9` = Session 2, slide 9.

---

## 0. The frame — every non-hero slide

Not an archetype; the shell all the others sit inside. Do not vary it.

```html
<div class="h-screen w-screen p-12 flex flex-col justify-center">
    <div class="mb-3 text-[#ff5640] font-mono tracking-widest uppercase text-sm animate-entry">The Build</div>
    <h2 class="text-5xl font-bold mb-2 animate-entry">Twenty Rows, One Command, Zero API Keys</h2>
    <p class="text-xl opacity-70 mb-6 animate-entry delay-1">One horizontal line. Above it, everything that computes a bit.</p>

    <!-- ARCHETYPE BODY GOES HERE, carrying animate-entry delay-2 -->

    <div class="mt-6 glass-panel-alt p-5 rounded-xl animate-entry delay-4">
        <p class="text-2xl font-bold">The deliverable is not the twenty rows. It is the proof that the twenty rows can go red.</p>
    </div>
</div>
```

Rules, all checkable:

- Eyebrow colour carries meaning: `#ff5640` (default), `#e74c3c` (a wall / a failure slide — S1/4, S2/2, S2/12, S3/12), `#FFD700` (an honesty or scope slide — S1/6, S1/9, S2/10, S2/13, S3/13), `#2ecc71` (a proof slide — S2/8, S2/9).
- Animation ladder is positional, never decorative: eyebrow + `h2` bare `animate-entry`; deck line `delay-1`; main body `delay-2`; secondary strips `delay-3`; closer `delay-4`. Nothing uses `delay-5`; it does not exist.
- Deck line is `text-xl` when the body is short, `text-lg` when the body is crowded (S2/7, S2/8, S2/13, S3/9, S3/11, S3/13). Bottom margin `mb-6`, dropped to `mb-5` or `mb-4` on crowded slides.
- Almost every slide ends with one `glass-panel-alt` closer holding a single bold sentence. `p-5 text-2xl` when there is room, `p-4 text-lg` / `p-3 text-base` when there is not.

**Vertical budget.** Canvas is 1920×1080. `p-12` leaves **984 px** usable. Header costs a fixed **140 px** (eyebrow 20+12, h2 48+8, deck 28+24). A `p-5`/`text-2xl` closer plus `mt-6` costs **~96 px**; a `p-3`/`text-base` closer plus `mt-3` costs **~64 px**. So the archetype body gets **~750–790 px**. Every fixed height quoted below was chosen against that number.

Nav is appended by the generator, never written by hand:

```html
<div class="absolute bottom-6 right-8 flex items-center gap-6 z-50">
    <span class="text-sm opacity-40 font-mono">SLIDE 07 / 14</span>
    <a href="slide6.html" class="nav-btn text-2xl"><i class="fas fa-chevron-left"></i></a>
    <a href="slide8.html" class="nav-btn text-2xl"><i class="fas fa-chevron-right"></i></a>
</div>
```

---

## 1. Hero / title

**Job:** open the deck. Session number, title, subtitle, one quotation, the speaker, one provenance line of hard numbers.

**Used by:** S1/1, S2/1, S3/1 — identical structure in all three, the only fully stable archetype.

```html
<div class="h-screen w-screen flex flex-col items-center justify-center relative overflow-hidden">
    <i class="fas fa-flask absolute text-[400px] opacity-5 text-white animate-float -z-10"></i>
    <div class="text-center z-10 animate-entry">
        <div class="mb-4 text-[#ff5640] font-mono tracking-widest uppercase">Test Cafe &middot; Session 3 of the RLM-Driven Automation series</div>
        <h1 class="text-7xl font-bold mb-6">How to Test AI Features</h1>
        <p class="text-2xl opacity-80 font-light max-w-3xl mx-auto">Building an Evaluation Harness in pytest</p>
        <div class="mt-8 w-24 h-1 bg-[#ff5640] mx-auto"></div>
        <p class="mt-8 text-2xl font-light italic opacity-75 animate-entry delay-2">&ldquo;The output changes every time. That is not a reason you cannot test it &mdash; it is a reason your assertion has to change shape.&rdquo;</p>
        <p class="mt-3 text-base opacity-55 animate-entry delay-2">Session 1 drew the map. Session 2 built the harness. Tonight we point it at the thing everyone says cannot be tested.</p>
        <div class="mt-8 animate-entry delay-3">
            <p class="text-lg opacity-70"><i class="fas fa-user-tie text-[#ff5640] mr-2"></i><b>Andrei Margelatu</b> | AI Engineer @ Endava</p>
        </div>
        <div class="mt-8 animate-entry delay-4">
            <p class="font-mono text-sm opacity-40">python -m pytest -q &middot; 20 rows &middot; 4 gates &middot; 106 checks green &middot; 0 API keys</p>
        </div>
    </div>
</div>
```

- No `p-12`; centring is `items-center justify-center` on the full screen.
- The giant watermark icon is `text-[400px] opacity-5 ... -z-10` and changes per deck: `fa-diagram-project` (S1), `fa-terminal` (S2), `fa-flask` (S3).
- Rule divider `w-24 h-1 bg-[#ff5640] mx-auto` is `mt-10` in S1, `mt-8` in S2/S3. Use `mt-8`.
- Gotcha: the last line is always real, reproducible numbers, never a tagline. It is the deck's honesty contract in one line.

Budget: ~640 px of stacked centred text. Never crowd it.

---

## 2. Two-column comparison

**Job:** two things that must be read against each other — before/after, can/cannot, free/paid, what-we-got/what-we-lack.

**Used by:** S1/2 (Reasoning vs Execution), S1/8 (paste vs REPL), S1/9 (parallels vs five questions), S2/10 (pixels vs aria), S2/12 (R1 hole vs R2 hole), S3/2 (Session 2 free vs Session 3 not free), S3/10 top (CAN vs CANNOT).

```html
<div class="grid grid-cols-2 gap-8 animate-entry delay-2">
    <div class="glass-panel-success p-6 rounded-xl">
        <div class="flex items-center gap-3 mb-4">
            <span class="badge badge-success">Session 2</span>
            <h3 class="text-2xl font-bold">What Session 2 Got for Free</h3>
        </div>
        <ul class="space-y-3 text-base">
            <li class="flex gap-3"><i class="fas fa-check mt-1" style="color:#2ecc71;"></i><span><span class="font-mono font-bold">pixelmatch</span> is a byte-exact oracle.</span></li>
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
```

- `gap-8` for two columns, always.
- The two panels carry **different** glass variants so the verdict is legible from the back row: `-success` vs `-warn` (S3/2, S3/10), or plain vs `border-left-color:#8fa3b0` for the deprecated side (S1/9, S2/10).
- Bullet glyph encodes the side: `fa-check`/`fa-caret-right` on the good column, `fa-times`/`fa-xmark`/`fa-minus` on the bad one.
- **Gotcha — fixed height.** Only set one when the two columns' copy is visibly unequal. S1/2 sets `style="height:346px;"` on both panels *and* puts `flex flex-col` + `flex-1` on the last block so the bullets bottom-align. S3/2 sets none, because both `<ul>`s have exactly three items. Getting this wrong is the single commonest way the house style breaks: unequal copy in a `grid` stretches both cards to the taller one and the internal rows stop lining up.

Budget: 340–420 px per panel; two of them plus the closer fills the band.

---

## 3. N-card grid

**Job:** N parallel, independent items of the same kind — objections, gates, cheats, holes, scorers, findings. The reader scans rather than reads.

| N | Grid | Gap | Fixed card height | Used by |
|---|---|---|---|---|
| 3 | `grid grid-cols-3 gap-6` | 24 | `300px` | S3/6 |
| 3 | `grid grid-cols-3 gap-6` | 24 | `288px` | S2/5 |
| 3 | `grid grid-cols-3 gap-5` | 20 | `430px` | S3/12 |
| 3 | `grid grid-cols-3 gap-6` | 24 | none | S1/4, S2/7, S2/13-tiles, S3/9, S3/10 |
| 3 | `grid grid-cols-3 gap-4` | 16 | none | S3/11 |
| 4 (1×4) | `grid grid-cols-4 gap-5` | 20 | `314px` (S2) / `352px` (S3) | S2/8, S3/8 |
| 4 (2×2) | `grid grid-cols-2 gap-6` | 24 | `260px` | S3/3 |
| 6 | `grid grid-cols-6 gap-3` | 12 | none | S3/10 |

Gap shrinks as N grows: 8 → 6 → 5 → 3. Follow it.

Canonical 4-up card (S3/8), showing the badge + title + "catches:" + code strip + `flex-1` body:

```html
<div class="glass-panel p-5 rounded-xl flex flex-col" style="height:352px;">
    <div class="flex items-center gap-3 mb-2">
        <span class="badge badge-accent text-lg" style="padding:6px 15px;">B</span>
        <h3 class="text-xl font-bold">DISCRIMINATING</h3>
    </div>
    <p class="text-sm opacity-60 mb-3">catches: the row that cannot go red</p>
    <div class="code-block p-2 text-xs leading-relaxed mb-3">
        <div class="px-1 py-0.5">truncate_half &middot; drop_last_field</div>
        <div class="px-1 py-0.5 mt-1 rounded flex items-center justify-between" style="background:#000;">
            <span class="font-bold" style="color:#ff5640;">(held-out mutant)</span>
            <span class="text-[10px] font-bold tracking-widest" style="color:#ff5640;">NEVER NAMED</span>
        </div>
    </div>
    <p class="text-sm opacity-85 flex-1">Every live mutant must redden at least one row.</p>
</div>
```

**Gotchas.**

1. `flex flex-col` + `style="height:NNNpx"` is mandatory whenever the cards' copy differs in length — which is almost always. Without it the tallest card sets the height and every internal element (code strip, footer) lands at a different y in each card. `flex-1` on the last paragraph absorbs the slack.
2. A card with a pinned footer uses `mt-auto pt-3` with a hairline instead of `flex-1` (S3/12):
   ```html
   <div class="mt-auto pt-3" style="border-top:1px solid rgba(255,255,255,0.12);">
       <div class="text-[11px] font-mono uppercase tracking-widest opacity-50 mb-1">the fix, in the mechanism</div>
       <p class="text-xs opacity-80"><span class="font-mono">mutate.py</span> &mdash; the mutation gate now runs on the <b>free ladder only</b>.</p>
   </div>
   ```
3. The 6-up variant is a **stat-tile row**, not a card grid: `glass-panel p-3 rounded-lg` (note `rounded-lg`, not `-xl`), a big `font-mono` number, a `text-xs` gloss, a `text-[10px] font-mono opacity-45` citation.
   ```html
   <div class="glass-panel-warn p-3 rounded-lg">
       <div class="font-mono text-2xl font-bold text-[#FFD700]">33&ndash;41pp</div>
       <div class="text-xs opacity-75 mt-1">exact-match overstates agreement vs. kappa</div>
       <div class="text-[10px] font-mono opacity-45 mt-2">2606.19544 &middot; text pairwise preference</div>
   </div>
   ```

### Modifier: the ASSERTS NOTHING stamp

Only on the "three suites that always pass" slides (S2/5, S3/6). Card needs `relative`.

```html
<div class="relative glass-panel p-6 rounded-xl flex flex-col"
     style="height:300px;border-left-color:#2ecc71;padding-bottom:74px;">
    ...
    <div class="stamp text-lg" style="left:28px;bottom:20px;">ASSERTS NOTHING</div>
</div>
```

The cards are deliberately `border-left-color:#2ecc71` (green) while stamped red — that contradiction *is* the argument. S2/5 positions the stamp with `top:228px` on a 288 px card and no reserved padding; S3/6 uses `bottom:20px` plus `padding-bottom:74px`. **Use the S3 form** — top-anchoring breaks the moment the height changes. `.stamp` is not defined in S1's stylesheet.

---

## 4. Ascending staircase

**Job:** a ladder where each rung strictly contains the one before — visual height *is* the argument.

**Used by:** S1/3 only (LLM → AI Engine → Agent → Orchestration).

```html
<div class="flex items-end gap-6 animate-entry delay-2" style="height:462px;">
    <div class="glass-panel rounded-xl p-6 flex-1 flex flex-col" style="height:300px;border-left-color:#8fa3b0;">
        <div class="flex items-center justify-between mb-3">
            <span class="font-mono text-sm opacity-30">01</span>
            <i class="fas fa-comment-dots text-3xl" style="color:#8fa3b0;"></i>
        </div>
        <h3 class="text-3xl font-bold leading-none">LLM</h3>
        <p class="text-xs font-mono opacity-40 mt-1 mb-3">the model, alone</p>
        <p class="text-base opacity-80 leading-snug flex-1">Text in, text out. One window, one shot.</p>
        <div class="mt-3 pt-3 border-t border-white/10">
            <div class="text-[11px] font-mono uppercase tracking-widest opacity-40 mb-1">Adds</div>
            <div class="font-bold text-lg" style="color:#8fa3b0;">Reasoning</div>
        </div>
    </div>
    <!-- 02: height:354px; border-left-color:#FFD700 -->
    <!-- 03: height:408px; border-left-color:#ff5640 -->
    <!-- 04: height:462px; border-left-color:#ff5640; background:rgba(255,86,64,0.07) -->
</div>
```

- Heights are an arithmetic series: **300 / 354 / 408 / 462**, step 54. The wrapper's height equals the tallest card.
- `flex items-end` bottom-aligns; `flex-1` makes the columns equal width.
- Border colour warms up the ladder: `#8fa3b0` → `#FFD700` → `#ff5640` → `#ff5640` + tint.
- Closed by a gradient autonomy axis, not a glass panel:
  ```html
  <div class="mt-5 flex items-center gap-4 animate-entry delay-3">
      <span class="text-xs font-mono uppercase tracking-widest opacity-40">less autonomy</span>
      <div class="flex-1" style="height:2px;background:linear-gradient(90deg, rgba(255,255,255,0.12), #ff5640);"></div>
      <i class="fas fa-caret-right text-[#ff5640]"></i>
      <span class="text-xs font-mono uppercase tracking-widest" style="color:#ff5640;">more autonomy &middot; more ways to fail</span>
  </div>
  ```

Budget: 462 px band + 30 px axis.

---

## 5. Scale-drawn bar comparison — `label | bar | value`

**Job:** any claim of the form "these N things differ by orders of magnitude / by measured points". The bar widths are the evidence, so they must be computed, never eyeballed.

**Used by:** S3/5 (eight scorers by price), S3/9 (five Wilson intervals), S2/2 (two token bars vs the window), S2/7 (three tiers of context), S2/4 (log-scale rungs, absolutely positioned), S1/4 (one overflowing bar), S1/6 (paired delta bars inside two panels).

Canonical row (S3/5):

```html
<div class="flex flex-col gap-2 animate-entry delay-2">
    <div class="flex items-center gap-4">
        <div class="text-right" style="width:200px;">
            <div class="font-bold text-sm font-mono">token_f1</div>
            <div class="text-xs opacity-45 font-mono">bag-of-tokens overlap</div>
        </div>
        <div class="flex-1 relative h-9">
            <div class="absolute left-0 top-0 h-full flex items-center px-4 rounded-r-lg"
                 style="width:75%; background:rgba(143,163,176,0.16); border:1px solid rgba(143,163,176,0.4);">
                <span class="text-xs opacity-80">cannot: word order, negation</span>
            </div>
        </div>
        <div class="text-right font-mono text-sm font-bold opacity-80" style="width:70px;">$0</div>
    </div>
</div>
```

Interval variant (S3/9) — a track with a filled segment and a point marker:

```html
<div class="flex items-center gap-3 mb-1.5">
    <div class="text-right font-mono text-xs font-bold" style="width:150px;color:#ff5640;">18 / 20 <span class="opacity-70 font-normal">&larr; our suite</span></div>
    <div class="flex-1 relative" style="height:30px;background:rgba(255,86,64,0.06);border:1px solid rgba(255,86,64,0.5);border-radius:4px;">
        <div class="absolute top-0 h-full rounded" style="left:69.9%;width:27.3%;background:#ff5640;opacity:0.75;"></div>
        <div class="absolute top-0 h-full" style="left:89.6%;width:2px;background:white;"></div>
    </div>
    <div class="font-mono text-xs font-bold" style="width:210px;color:#ff5640;">[69.9%, 97.2%] &middot; 27.3pp</div>
</div>
```

Rules:

- Label gutter and value gutter are **fixed px**, the bar is `flex-1`. Observed gutters: 200/70 (S3/5), 150/210 (S3/9), 230/150 (S2/2), 230/190 (S2/7), 214/– (S2/4).
- The axis strip under the bars repeats those gutters as padding so the ticks land on the bar, not on the label:
  ```html
  <div class="flex justify-between text-xs font-mono opacity-35 mt-1" style="padding-left:162px;padding-right:222px;">
      <span>0%</span><span>50%</span><span>100%</span>
  </div>
  ```
  (S2/7 uses `padding-left:254px;padding-right:214px;` = gutter + gap.)
- Bar `width` is a **percentage of the real number**, stated in the caption. S3/9's 69.9%/27.3% are the actual Wilson bounds. S2/4 is explicitly log-scaled and says so in the axis label.
- The one row that carries the argument is recoloured gold or coral and given a heavier border; everything else is `rgba(143,163,176,·)` muted. S3/5 also detaches the paid row with `mt-3`.
- **Gotcha — sub-pixel bars.** When a bar rounds to less than a pixel, draw it at 2 px and say so on the slide: *"to scale this bar is `0.2 px` wide. It is drawn at 2 px because a browser cannot draw less."* (S2/7). Do not silently inflate it.
- **Gotcha — overflow.** A bar that exceeds the container is drawn as a hatched remainder, not clipped:
  ```html
  <div class="absolute top-0 h-full" style="left:5%;right:0;background:repeating-linear-gradient(45deg, rgba(255,255,255,0.05) 0 10px, rgba(255,255,255,0.015) 10px 20px);"></div>
  ```
  S2/2 goes further and breaks the bar off the right edge with three `&#8250;` chevrons plus a fade.
- **Gotcha — the boundary marker.** A threshold line is a separate absolutely-positioned element sitting on the same percentage as the bar's split, with its own label block:
  ```html
  <div class="relative animate-entry delay-2" style="height:58px;">
      <div class="absolute bottom-0 pl-4 flex flex-col justify-end" style="left:80.05%;height:58px;border-left:2px solid #ff5640;">
          <div class="font-bold text-lg leading-none" style="color:#ff5640;">1,050,000 tokens</div>
          <div class="text-xs opacity-50 font-mono mt-1">the whole frontier window.</div>
      </div>
  </div>
  ```

Budget: rows are 36–86 px each. Eight rows + caption + two strips + closer fills S3/5 exactly.

---

## 6. Fixed-pixel diagram canvas

**Job:** one architecture picture per deck, showing a boundary and what crosses it. **One per deck, maximum.**

**Used by:** S1/5, S2/6, S3/7. Nothing else.

```html
<div class="relative mx-auto animate-entry delay-2" style="width:1700px;height:470px;">

    <svg class="absolute inset-0 pointer-events-none" width="1700" height="470" viewBox="0 0 1700 470" style="overflow:visible;">
        <defs>
            <marker id="arCoral7" markerWidth="10" markerHeight="8" refX="8" refY="3.5" orient="auto">
                <polygon points="0 0, 9 3.5, 0 7" fill="#ff5640"/>
            </marker>
            <marker id="arMute7" markerWidth="10" markerHeight="8" refX="8" refY="3.5" orient="auto">
                <polygon points="0 0, 9 3.5, 0 7" fill="rgba(255,255,255,0.45)"/>
            </marker>
        </defs>
        <line x1="0" y1="280" x2="1700" y2="280" stroke="#ff5640" stroke-width="4"/>
        <line x1="820" y1="244" x2="820" y2="310" stroke="#ff5640" stroke-width="3" marker-end="url(#arCoral7)"/>
        <line x1="900" y1="310" x2="900" y2="244" stroke="rgba(255,255,255,0.45)" stroke-width="3" marker-end="url(#arMute7)"/>
    </svg>

    <div class="absolute glass-panel rounded-xl p-4" style="left:0px;top:0px;width:255px;height:130px;border-left-color:#8fa3b0;">
        <i class="fas fa-file-code text-2xl mb-2" style="color:#8fa3b0;"></i>
        <h3 class="text-lg font-bold leading-none font-mono">golden.yaml</h3>
        <p class="text-xs opacity-60 mt-2">20 rows &middot; validated on load</p>
    </div>
    <i class="fas fa-arrow-right absolute text-sm" style="left:263px;top:56px;color:#ff5640;opacity:0.6;"></i>

    <div class="absolute px-4 py-1 rounded font-mono text-sm font-bold uppercase tracking-widest"
         style="left:24px;top:258px;white-space:nowrap;background:#192b37;color:#ff5640;border:2px solid #ff5640;">
        the line
    </div>
</div>
```

Canvas dimensions actually used: **1200×520** (S1/5), **1400×494** (S2/6), **1700×470** (S3/7). All `relative mx-auto` with hard px. No responsive units anywhere inside.

**This is the archetype that is easiest to get wrong. Read this part twice.**

- **Inline `<svg>` is rare.** Counted across all 38 slides: S1 has 2 (`slide5`, `slide7`), S2 has 2 (`slide6`, `slide13`), S3 has **1** (`slide07`). Thirty-three slides have none. A build that reaches for SVG on every diagram will not look like these decks.
- **The SVG draws lines only.** Boxes, labels, icons, badges, code panels are all absolutely-positioned `div`s on top. The only non-line SVG primitives ever used are: the dashed container `rect`, the blocked-path `circle` + two crossing `line`s, and `marker`/`polygon` arrowheads. There is no SVG `<text>` in any deck.
- **Short connectors between adjacent boxes are Font Awesome, not SVG:** `<i class="fas fa-arrow-right absolute text-sm" style="left:263px;top:56px;color:#ff5640;opacity:0.6;"></i>`. SVG is reserved for lines that *cross the boundary* or fan out.
- Arrow semantics are fixed: **coral `#ff5640` = a call going away from the model; muted `rgba(255,255,255,0.45)` = a value coming back; gold `#FFD700` = a value landing in a variable or on disk; red `#e74c3c` dashed with a crossed circle = the path that is forbidden.** Marker ids are per-slide (`ahCoral`/`arCoral`/`arCoral7`) so two canvases never collide.
- The boundary is one `stroke-width="4"` coral line, and its label is a `div` with `background:#192b37` sitting on top of it so the line appears to break. Same trick for the dashed-container label.
- The only curved arrows in any deck are S1/7's fan-out/fan-in `<path d="M 470 2 C 380 40, 260 66, 152 110">` — calls leave the left half of the root, values return to the right half, so the two bundles never overlap.
- S2/13's second SVG is *not* a canvas: it is a 520×104 `preserveAspectRatio="none"` two-line crossover chart with a dashed marker line and HTML labels positioned over it. That is the only chart-shaped SVG in the decks.
- Gotcha: `pointer-events:none` on the overlay, `overflow:visible` on the `<svg>` (markers otherwise clip), and every `<line>` coordinate must be re-derived when a box moves. These layouts do not reflow; nothing is forgiving.
- A canvas slide gets a badge strip below it instead of a glass closer:
  ```html
  <div class="flex items-center justify-center gap-4 mt-3 animate-entry delay-3">
      <span class="badge" style="background:rgba(255,255,255,0.10);color:rgba(255,255,255,0.8);">20 parametrized row tests + 1 suite-gate test</span>
      <span class="badge badge-success">18 passed</span>
      <span class="badge badge-warn">2 failed &middot; R02 &middot; R07</span>
      <span class="text-sm opacity-60 italic ml-2">pytest and pyyaml. That is the entire dependency list.</span>
  </div>
  ```

**Most diagrams are not this.** S1/2's Q→A loop, S1/3's ladder, S2/10's diff-box mock-up, S3/8's gate cards and S3/11's three conditions are all plain flex/grid or absolutely-positioned `div`s. Reach for the canvas only when there is a literal boundary to draw.

---

## 7. Terminal / code panel

**Job:** show the real artefact — a dataclass, a REPL session, the commands the audience will run. Never a screenshot, never a syntax highlighter.

**Used by:** as the primary body — S1/5, S2/3, S3/4 (split rules+code), S2/14, S3/14 (commands). As an element inside cards — S2/5, S2/8, S2/9, S3/6, S3/8, S3/12. As a transcript triptych — S2/9.

Full panel with chrome:

```html
<div class="code-block overflow-hidden">
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
        <div class="mt-4"><span class="opacity-40">&gt;&gt;&gt;</span> load_goldens("goldens/support.golden.yaml")</div>
        <div style="color:#e74c3c;">GoldenError: R21: expected value came from the model under test</div>
        <div style="color:#e74c3c;" class="pl-4">raised at load. before a single test runs.</div>
    </div>
</div>
```

Bare strip inside a card (no chrome): `<div class="code-block p-3 text-sm leading-relaxed mb-4">`.

Rules:

- One `<div>` per line. No `<pre>`, no `<code>`, no highlighter library. Indentation is `pl-4` / `pl-8` / `pl-10` / `pl-14`.
- Colour is semantic, applied inline: prompt `class="opacity-40"` on `>>>` or `style="color:#ff5640;"` on `$`; output `text-green-400` (S1/S2) or `style="color:#2ecc71;"` (S3); error `#e74c3c`; the costed line `#FFD700`; comments `opacity-45` / `opacity-60`.
- The chrome caption is a file path or a provenance note, never "Terminal".
- `overflow-hidden` on the wrapper, or the rounded corners leak.
- **Gotcha — faded truncation.** A long log is faded out, not cut:
  ```html
  <div class="absolute inset-x-0 bottom-0" style="height:120px;background:linear-gradient(to bottom, transparent, #0d161c);"></div>
  <div class="absolute bottom-3 left-0 right-0 text-center font-mono text-xs" style="color:#e74c3c;">&hellip; 412,331 more lines</div>
  ```
  The gradient must end on `#0d161c` — that is `.code-block`'s background, not the slide's `#192b37`.

### 7b. Rules-and-code split

**Used by:** S2/3, S3/4. Two rules on the left, the mechanism that enforces them on the right.

```html
<div class="grid grid-cols-5 gap-8 animate-entry delay-2">
    <div class="col-span-2 flex flex-col gap-4">
        <div class="glass-panel p-5 rounded-xl">
            <div class="flex items-center gap-3 mb-2">
                <span class="badge badge-accent text-lg" style="padding:6px 16px;">R1</span>
                <span class="text-[11px] font-mono uppercase tracking-widest opacity-40">whether the row is a test</span>
            </div>
            <h3 class="text-xl font-bold leading-snug mb-2">A row is a test only if it can fail.</h3>
            <p class="text-sm opacity-85 leading-relaxed">A row that cannot go red asserts nothing, however green it is.</p>
        </div>
        <div class="glass-panel-alt p-5 rounded-xl"><!-- R2, badge-roi --></div>
    </div>
    <div class="col-span-3 code-block overflow-hidden"><!-- chrome + lines --></div>
</div>
```

`grid-cols-5` with `col-span-2` / `col-span-3`, `gap-8`. R1 is `glass-panel` + `badge-accent`; R2 is `glass-panel-alt` + `badge-roi`. Both decks end this slide by promising the rules are broken later ("enforced by a paragraph in the README until slide 12").

### 7c. Transcript triptych

**Used by:** S2/9 only. Three `code-block` columns in a `grid-cols-3 gap-6`, each a verbatim gate report, each headed by a title + verdict badge and footed by a `text-sm opacity-60` gloss. Columns are `flex flex-col` with `flex-1` on the `code-block` so the three transcripts bottom-align despite different line counts. Use it when the payoff is "here is the machine's own output, unedited".

---

## 8. Decision / trigger table on `grid-cols-12`

**Job:** the scope slide. N things deliberately not built, why, and the written trigger that would reverse the decision.

**Used by:** S2/13, S3/13. Structurally identical; S3 renames the middle column to "Why — the measured reason".

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

- Never a `<table>`. `grid-cols-12` with `3 / 5 / 4`.
- Wrapper is one `glass-panel` with `overflow-hidden` and `border-left-color:#8fa3b0` (neutral — this slide is not an argument).
- Header row is tinted `rgba(255,255,255,0.04)`; every body row gets `border-top:1px solid rgba(255,255,255,0.07)` and `items-center`.
- Third column is always `font-mono` + `color:#FFD700` — the trigger is the payload, and gold is the deck's "this costs something" colour. One row is allowed to read `never. This one is arithmetic.`
- Followed by a `glass-panel-warn` "who should not build this" panel, then the closer.

Budget: five rows ≈ 300 px; header 32 px; leaves room for the warn panel and closer.

---

## 9. Closing CTA — "run it, then break it"

**Job:** last slide of a hands-on session. Commands on the left, honesty on the right, citations and the speaker along the bottom.

**Used by:** S2/14, S3/14. Same skeleton, S3 adds a third right-hand panel.

```html
<div class="grid grid-cols-2 gap-8 animate-entry delay-2">
    <div class="flex flex-col gap-5">
        <div class="code-block overflow-hidden"><!-- chrome + $ commands, each followed by an opacity-45 gloss --></div>
        <div class="glass-panel-warn p-4 rounded-xl">
            <div class="flex items-center gap-3 mb-2">
                <i class="fas fa-flask text-xl" style="color:#e74c3c;"></i>
                <h3 class="text-lg font-bold">Two exercises, both designed to fail</h3>
            </div>
            <div class="space-y-2 text-sm opacity-90">
                <div class="flex gap-3"><span class="font-mono font-bold" style="color:#ff5640;">1</span><span>&hellip;</span></div>
                <div class="flex gap-3"><span class="font-mono font-bold" style="color:#ff5640;">2</span><span>&hellip;</span></div>
            </div>
        </div>
    </div>

    <div class="flex flex-col gap-5">
        <div class="glass-panel p-5 rounded-xl" style="border-left-color:#8fa3b0;">
            <div class="flex items-center gap-3 mb-3">
                <i class="fas fa-circle-question text-xl" style="color:#8fa3b0;"></i>
                <h3 class="text-xl font-bold">What I still do not know</h3>
            </div>
            <div class="space-y-2 text-sm opacity-85">
                <div class="flex gap-3"><i class="fas fa-minus text-xs mt-2 opacity-40"></i><span>&hellip;</span></div>
            </div>
        </div>
        <div class="glass-panel-alt p-4 rounded-xl"><!-- fa-flag-checkered · "The ask" --></div>
        <div class="glass-panel-warn p-4 rounded-xl"><!-- "the open question" --></div>
    </div>
</div>

<div class="mt-6 flex items-end justify-between animate-entry delay-4">
    <p class="text-sm opacity-40 font-mono">AgentRewardBench 2504.08942 &middot; Judge audit 2606.19544 &middot; WebJudge 2504.01382</p>
    <p class="text-lg opacity-70"><i class="fas fa-comments text-[#ff5640] mr-2"></i>Questions &middot; <b>Andrei Margelatu</b> | AI Engineer @ Endava</p>
</div>
```

- There is no glass closer on this archetype; the `items-end justify-between` footer is the closer.
- The left column is always executable, the right column always admits something. That asymmetry is the archetype.
- `space-y-2` bullet rows use `<i class="fas fa-minus text-xs mt-2 opacity-40">` — the `mt-2` is what aligns the dash with the first text line.

### 9b. Series-handoff close

**Used by:** S1/10 only — a session that ends by pointing at the next one.

```html
<div class="h-screen w-screen p-16 flex flex-col justify-center relative overflow-hidden">
    <i class="fas fa-terminal absolute text-[420px] opacity-5 text-white animate-float -z-10" style="right:-50px;bottom:-70px;"></i>
    <div class="mb-4 text-[#ff5640] font-mono tracking-widest uppercase text-sm animate-entry">What&rsquo;s Next</div>
    <h2 class="text-6xl font-bold mb-10 animate-entry">That Was the Map. Next We Build.</h2>
    <div class="glass-panel p-10 rounded-2xl max-w-5xl animate-entry delay-1">
        <div class="flex items-center gap-4 mb-4">
            <span class="badge badge-accent">Session 2 &middot; next</span>
            <span class="text-sm font-mono opacity-40">hands-on &middot; bring a laptop</span>
        </div>
        <h3 class="text-4xl font-bold mb-4"><i class="fas fa-code text-[#ff5640] mr-4"></i>Building a REPL Harness</h3>
        <p class="text-xl opacity-80 font-light leading-relaxed">&hellip;</p>
    </div>
    <div class="mt-10 p-6 rounded-xl max-w-5xl animate-entry delay-2" style="background:rgba(255,86,64,0.08);border:1px solid rgba(255,86,64,0.35);">
        <p class="text-3xl font-light italic">Bring me the artefact you gave up on reading. <b class="not-italic" style="color:#ff5640;">That is Session 2&rsquo;s demo.</b></p>
    </div>
    <div class="mt-12 flex items-end justify-between animate-entry delay-3"><!-- series line + speaker --></div>
</div>
```

Only slide in any deck using `p-16`, `text-6xl`, `rounded-2xl`, `p-10`, `max-w-5xl` — it is deliberately roomier than everything before it. The watermark icon is offset (`right:-50px;bottom:-70px`) rather than centred.

---

## 10. Video slide

**Job:** play a recorded run. Exactly one in the whole series.

**Used by:** S2/11 only. Uses `px-12 py-8` (not `p-12`) and puts the h2 and deck line on one baseline via `flex items-baseline gap-5`.

```html
<video id="vizdemo" tabindex="0" controls muted playsinline preload="metadata"
       poster="media/viz-demo-poster.jpg" src="media/viz-demo.mp4"
       class="block rounded-xl mx-auto print-hide"
       style="height:64vh;aspect-ratio:16/10;width:auto;max-width:100%;object-fit:contain;background:#0d161c;border:1px solid rgba(255,255,255,0.14);box-shadow:0 18px 60px rgba(0,0,0,0.45);">
</video>

<!-- PDF fallback: a <video> paints nothing in print, so the poster frame stands in. -->
<img class="print-only rounded-xl mx-auto" src="media/viz-demo-poster.jpg" alt="..." style="height:64vh;...">
<div class="print-only mt-3 text-center text-sm leading-relaxed">
    <b style="color:#FFD700;">Still frame at 0:50 &mdash; the 2:31 video cannot play inside a PDF.</b><br>
</div>
```

Three gotchas, all solved on that slide and all mandatory if you copy it:

1. `print-hide` / `print-only` pair, because a `<video>` renders blank in the PDF.
2. Scrub-cue row (`grid-cols-4`, timecode + one-line label) so the presenter can jump.
3. A `keydown` listener registered **before** the nav script that calls `stopImmediatePropagation()` when the video has focus, plus a visible hint pill saying who currently owns the arrow keys. Without it Space both plays the video and advances the slide.

---

## Modifiers usable on any archetype

| Modifier | Markup | Where |
|---|---|---|
| Pre-step strip above a grid | `<div class="glass-panel-alt p-4 rounded-xl mb-5 animate-entry delay-1 flex items-center gap-6">` with an icon block and a `flex-1 pl-6` body divided by `border-left:1px solid rgba(255,255,255,0.12)` | S2/8, S3/8 |
| Provenance footnote | `<div class="mt-4 text-xs font-mono opacity-40 animate-entry delay-3">Session 2 &middot; viz/runs/gates-proof/events.jsonl</div>` | S3/2, S3/5, S3/11 |
| Struck-through token list | `<span class="text-sm relative inline-block">the feature's own output<span class="absolute left-0 right-0" style="top:50%;height:2px;background:#e74c3c;"></span></span>` in a `flex flex-wrap gap-x-8 gap-y-1` | S3/4 |
| Inline delta bar inside a panel | track `rgba(255,255,255,0.05)` h-24px, baseline segment `rgba(255,255,255,0.16)`, delta segment coloured, label absolutely placed just past the end | S1/6 |
| Two-up term mapping | `grid grid-cols-2 gap-x-4 items-baseline py-1`, muted left / bold right, under a `text-[11px] font-mono uppercase tracking-widest` header pair | S1/9 |
| Callout with no glass | `<div class="p-4 rounded-xl" style="background:rgba(231,76,60,0.10);border:1px solid rgba(231,76,60,0.35);">` — used when a glass panel would be the fifth in a row | S1/4, S1/9, S3/7, S3/12 |

---

## Rhetorical job → archetype

| The job on the slide | Archetype |
|---|---|
| Open the deck, state the honesty contract | 1 · Hero |
| "Two things, read them against each other" | 2 · Two-column comparison |
| "N parallel items of one kind" (objections, gates, cheats, findings) | 3 · N-card grid |
| "All of these pass, none of them assert" | 3 + ASSERTS NOTHING stamp |
| "Six measured numbers, each with a citation" | 3 · 6-up stat tiles |
| "Each rung contains the one below" | 4 · Ascending staircase |
| "These differ by orders of magnitude" / "here is the real spread" | 5 · Scale-drawn bars |
| "It does not fit, and here is by how much" | 5 + overflow hatching + boundary marker |
| "Here is the system, and here is the one line nothing crosses" | 6 · Diagram canvas (once per deck) |
| "Here is the actual code / the actual refusal" | 7 · Terminal panel |
| "Two rules generate everything, and here is the mechanism" | 7b · Rules-and-code split |
| "Here is the machine's own unedited output, three ways" | 7c · Transcript triptych |
| "What we deliberately did not build, and what would reverse it" | 8 · `grid-cols-12` decision table |
| "Run this tonight; here is what I still don't know" | 9 · Closing CTA |
| "That was the map — next session we build" | 9b · Series handoff |
| "Watch it happen" | 10 · Video slide |
| Any slide's last word | The `glass-panel-alt` closer from §0 |

---

## Where the decks contradict each other

| Point | S1 | S2 | S3 | Use |
|---|---|---|---|---|
| Print/PDF CSS | absent | **present, all 14 slides** | present, all 14 slides — byte-identical block to S2 | S2/S3 form |
| `.stamp`, `.print-only` in the stylesheet | absent | present | present | present |
| Bodies | inline in each slide | inline in each slide | separate `slides/slideNN.body.html` fragments | S3 form |
| Stamp positioning | n/a | `top:228px` on a 288 px card | `bottom:20px` + `padding-bottom:74px` | S3 form |
| REPL output colour | `text-green-400` | `text-green-400` | `style="color:#2ecc71;"` | S3 form |
| Hero rule divider margin | `mt-10` | `mt-8` | `mt-8` | `mt-8` |
| Closing slide | series handoff (9b), `p-16` | run-it (9) | run-it (9) | pick by session type |
| Equivalence guard claim | n/a | "solved **for free** because our domain is pixels" (S2/8) | "Session 2 got this exactly and for free… we compare serialised text, **strictly weaker**" (S3/8), and S3/2 notes the S2 guard **fired zero times** in the recorded run | S3's framing supersedes S2's |
