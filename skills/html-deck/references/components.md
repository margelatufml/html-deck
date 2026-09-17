# components.md — the house component library

Every block below is lifted verbatim from a presented deck. Source labels:

| Label | Path |
|---|---|
| **S1** | `RLM Test Cafe/deck/slideN.html` (10 slides) |
| **S2** | `RLM Test Cafe Session 2/deck/slideN.html` (14 slides) |
| **S3** | `RLM Test Cafe Session 3/slides/slideNN.body.html` → `.../Session 3/deck/slideN.html` (14 slides) |

**S3 wins every disagreement.** It is the only deck whose slide bodies live in separate fragment files
(`slides/slideNN.body.html`, assembled by `generate_s3_deck.py`), and its `.stamp` layout is the corrected
one. Where S1 and S2 differ from S3, the S3 form is house style.

Everything here assumes the shared `<style>` block is present in the `<head>` of every slide file. It is
identical byte-for-byte across S2 and S3 except the `<title>`. S1's copy is the same minus `.stamp` and
minus the whole `@media print` section.

Required tokens (verbatim from the head):

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

`#8fa3b0` is the fifth colour. It is **not** a CSS variable — it only ever appears as a literal, inline.

---

## 1. Glass panel and its four semantic variants

**CSS (head, verbatim).** Four rules that differ only in `border-left`:

```css
.glass-panel {
    background: var(--glass);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-left: 4px solid var(--accent-color);
}
.glass-panel-alt {
    background: var(--glass);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-left: 4px solid var(--roi-color);
}
.glass-panel-success {
    background: var(--glass);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-left: 4px solid var(--success-color);
}
.glass-panel-warn {
    background: var(--glass);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-left: 4px solid var(--warn-color);
}
```

**Semantics — the left border is the argument, not decoration:**

| Class | Stripe | Means |
|---|---|---|
| `.glass-panel` | `#ff5640` coral | neutral / the thing under discussion |
| `.glass-panel-alt` | `#FFD700` gold | the payoff, the money line, the closer |
| `.glass-panel-success` | `#2ecc71` green | what works, what is measured to help |
| `.glass-panel-warn` | `#e74c3c` red | the trap, the caveat, the thing that fails |

**Markup.** Always `class="glass-panel-X p-N rounded-xl"`. Padding is `p-3`…`p-6`, radius is always
`rounded-xl` (`rounded-2xl` once, on S1 slide10's oversized hero card; `rounded-lg` for the small
6-across stat tiles on S3 slide10).

S3 `slide02.body.html:8-18` — a titled two-column panel:

```html
<div class="glass-panel-success p-6 rounded-xl">
    <div class="flex items-center gap-3 mb-4">
        <span class="badge badge-success">Session 2</span>
        <h3 class="text-2xl font-bold">What Session 2 Got for Free</h3>
    </div>
    <ul class="space-y-3 text-base">
        <li class="flex gap-3"><i class="fas fa-check mt-1" style="color:#2ecc71;"></i><span><span class="font-mono font-bold">pixelmatch</span> is a byte-exact oracle. Two renders are identical or they are not.</span></li>
    </ul>
</div>
```

**The inline `#8fa3b0` neutral override.** When a panel is deliberately *not* making an argument — a
reference table, a file-list box, an inventory of tools, a "what I don't know" panel — keep `.glass-panel`
and override the stripe inline. 17 occurrences across the three decks; it is the single most common
inline override.

S3 `slide13.body.html:6` (the decision table's container) and S2 `slide13.html`:

```html
<div class="glass-panel rounded-xl overflow-hidden animate-entry delay-2" style="border-left-color:#8fa3b0;">
```

S3 `slide14.body.html:41`:

```html
<div class="glass-panel p-5 rounded-xl" style="border-left-color:#8fa3b0;">
```

Other inline stripe overrides in the decks, all on `.glass-panel`: `#2ecc71` ×6 (used ironically on S2
slide5 / S3 slide6 — the three always-green suites are stamped green *because* they always pass),
`#FFD700` ×8, `#e74c3c` ×2, `#ff5640` ×3.

**Trap.** A naive implementation picks the variant by how the card looks in the grid (alternating for
rhythm, or all-coral for tidiness). The stripe is a claim: gold panels are the ones the audience is
supposed to remember, red panels are the ones being argued against. A deck where every panel is
`.glass-panel` reads as unedited. A deck where the closer is not gold has lost its spine.

Second trap: `backdrop-filter: blur(10px)` only produces glass over the `#192b37` body. Nesting a
glass panel inside another glass panel doubles the fill and washes out the stripe — the decks never
do it. Nest a plain tinted `<div>` instead (see §3, form B).

---

## 2. The three-beat header block

Every interior slide opens with exactly three elements, in this order, before any content. 21 of 26
interior slides across S2+S3 use the coral eyebrow; 5 use gold `#FFD700`, 5 use red `#e74c3c`, 2 use
green `#2ecc71`, matching the slide's argument.

S3 `slide05.body.html:1-4`, verbatim:

```html
<div class="h-screen w-screen p-12 flex flex-col justify-center">
    <div class="mb-3 text-[#ff5640] font-mono tracking-widest uppercase text-sm animate-entry">Seven Ways to Score One Answer</div>
    <h2 class="text-5xl font-bold mb-2 animate-entry">Same Answer, Seven Prices</h2>
    <p class="text-xl opacity-70 mb-6 animate-entry delay-1">One row of the golden set, scored seven ways. Six of them are arithmetic. Climb only when the rung below provably cannot express the question.</p>
```

Fixed parts, non-negotiable:

| Beat | Markup | Rule |
|---|---|---|
| slide frame | `h-screen w-screen p-12 flex flex-col justify-center` | `p-12` everywhere; `p-16` once (S1 slide10), `px-12 py-8` once (S2 slide11, the video slide) |
| eyebrow | `mb-3 text-[#HEX] font-mono tracking-widest uppercase text-sm animate-entry` | mono, uppercase, wide-tracked, no delay class |
| h2 | `text-5xl font-bold mb-2 animate-entry` | always `text-5xl` on interior slides, `text-6xl` only on S1 slide10 |
| subtitle | `text-xl opacity-70 mb-6 animate-entry delay-1` | `text-lg` when the sentence is long (S3 slides 9, 11, 13, 14) |

The eyebrow may carry a second clause after a `&middot;` when it needs to make a provenance claim —
S3 `slide09.body.html:2`:

```html
<div class="mb-3 text-[#ff5640] font-mono tracking-widest uppercase text-sm animate-entry">The Honest Slide &middot; every interval recomputed on this machine</div>
```

**Animation ladder.** The header is beats 0 and 1; content is `delay-2`; supporting notes `delay-3`;
the closer `delay-4`. S1 tops out at `delay-3`; S2 and S3 use `delay-4` for the closer. Follow S3.

**Trap.** Writing the h2 as a topic ("Scorers") instead of a claim ("Same Answer, Seven Prices"). Every
h2 in all three decks is a sentence fragment that asserts something: *Six Pages Blow the Window*,
*Three Suites That Always Pass*, *Four Gates, No Opinions*, *A Model Reviewing Its Own Work Makes It
Worse*. Second trap: putting `delay-1` on the eyebrow or h2 — they carry no delay class, so the header
is on screen while the body fades in.

---

## 3. The closer strip

The last element of a content slide is a full-width bar that states the "so what", and it is what the
slide's top `delay-4` is normally spent on. Both forms below are house style.

### Form A — `.glass-panel-alt` (the default: 13 of the 26 interior slides in S2+S3 close on it, 4 more on `-warn` / `-success` / plain `.glass-panel`)

S3 `slide06.body.html:58-60`:

```html
<div class="glass-panel-alt p-5 rounded-xl mt-6 animate-entry delay-4">
    <p class="text-2xl font-bold">The deliverable is not the twenty rows. It is the proof that the twenty rows can go red.</p>
</div>
```

Text size tracks how much room is left: `text-2xl font-bold` when the slide is sparse, down to
`text-sm` when it is dense (S3 slide9 uses `text-base font-bold` at `p-3 mt-3`). `text-center` is added
when the line is short (S3 slide5, S3 slide8).

The variant can shift when the closer's argument is a warning or a win rather than a payoff — S3
slide8 closes on `.glass-panel-warn`, S3 slide11 on `.glass-panel-success`:

```html
<div class="glass-panel-success p-4 rounded-xl mt-4 animate-entry delay-4">
    <p class="text-xl font-bold">The fix is not a better critic prompt. It is a sound external verifier returning one bit &mdash; and you already have one. It is called <span class="font-mono">assert</span>.</p>
</div>
```

### Form B — the bespoke inline-styled tinted box

No glass, no left stripe: a flat 8–10%-alpha fill of one semantic colour with a 28–35%-alpha border of
the same colour. Use it when the closer is a *sentence in the slide's own voice* rather than the
slide's conclusion, or when a gold stripe would be a fourth gold thing on the slide.

S3 `slide07.body.html:109-111`:

```html
<div class="w-full text-center mt-3 py-3 rounded-lg animate-entry delay-4" style="background:rgba(255,86,64,0.08);border:1px solid rgba(255,86,64,0.3);">
    <span class="text-lg font-bold">Everything above the line is arithmetic. That is why it costs nothing, never flakes, and can be read on a projector.</span>
</div>
```

S1 `slide4.html:178-180`:

```html
<div class="mt-6 p-4 rounded-xl animate-entry delay-4" style="background:rgba(231,76,60,0.10);border:1px solid rgba(231,76,60,0.35);">
    <p class="text-base"><b style="color:#e74c3c;">The tell:</b> the strongest baselines in the RLM paper score <b class="font-mono">0.0</b> on this benchmark. That is not a model underperforming &mdash; it is a model structurally unable to be shown the input.</p>
</div>
```

S3 `slide12.body.html:71-73` uses it for an extra finding *above* the real closer:

```html
<div class="mt-4 px-4 py-3 rounded-lg animate-entry delay-3" style="background:rgba(231,76,60,0.08);border:1px solid rgba(231,76,60,0.28);">
```

The alpha pairs actually used: `rgba(255,86,64,0.08)/0.3`, `rgba(255,86,64,0.10)/0.32`,
`rgba(231,76,60,0.08)/0.28`, `rgba(231,76,60,0.10)/0.35`, `rgba(255,215,0,0.14)/0.35`,
`rgba(46,204,113,0.12)/0.4`. Pick one; do not invent a third alpha.

**Exceptions in the source.** Two interior slides end without a closer strip: S2 slide6 ends on a
centred badge row, and S2 slide11 (the video) ends on the layout itself. S2 slide5 splits the closer
into a two-up grid (`glass-panel-warn` quote + `glass-panel-alt` explanation). Treat these as licensed
exceptions, not as permission to skip the closer — a content slide with no bottom bar has no landing.

**Trap.** Writing the closer as a summary of the slide. It is not a summary; it is the sentence the
speaker says out loud and then stops. It restates nothing above it. Compare S3 slide9's body (five
Wilson intervals, three stat callouts, a sample-size line) with its closer: *"Twenty rows is a smoke
test with receipts. It is not a benchmark."* Second trap: `mt-*` is on the closer, not on the element
above it — the spacing is `mt-3`…`mt-6` depending on what is left of the 1080px.

---

## 4. The code block

**CSS (head, verbatim):**

```css
.code-block {
    font-family: 'Fira Code', monospace;
    background: #0d161c;
    border-radius: 8px;
    border: 1px solid #333;
}
```

`#0d161c` is the only other background colour in the system. It is not a variable.

### Plain form — inside a card

One `<div>` per line, no `<pre>`, no `<code>`, no syntax-highlighter. Comments and labels get
`opacity-45`; live values get a semantic colour inline.

S3 `slide06.body.html:14-18`:

```html
<div class="code-block p-3 text-sm leading-relaxed mb-4">
    <div><span class="opacity-45">scorer:</span> token_f1</div>
    <div><span class="opacity-45">threshold:</span> &gt;= 0.15</div>
    <div class="mt-1" style="color:#FFD700;">answer: ~200 words, fluent English</div>
</div>
```

Indentation is `pl-4` / `pl-6`, never leading spaces. S3 `slide04.body.html:42-51`:

```html
<div class="p-5 text-sm leading-relaxed">
    <div class="opacity-70">@dataclass(frozen=True)</div>
    <div>class Row:</div>
    <div class="pl-4">id: str</div>
    <div class="pl-4" style="color:#ff5640;">provenance: str<span class="opacity-60 ml-3"># required &mdash; R2, in the type</span></div>
    <div class="pl-4 opacity-60">notes: str = ""</div>
</div>
```

Hand-coloured tokens, S2 `slide11.html`:

```html
<div><span style="color:#8fa3b0;">test</span>(<span style="color:#2ecc71;">'empty baseline'</span>, async ({ page }) =&gt; {</div>
<div class="pl-3">await page.<span style="color:#8fa3b0;">goto</span>(<span style="color:#2ecc71;">'/empty'</span>);</div>
```

### Terminal header variant — three dots

Used 5 times across the decks (S1 slide5, S2 slide3, S2 slide14, S3 slide4, S3 slide14), always for a
shell transcript or a "this is the real file" claim. The outer `.code-block` gains `overflow-hidden` so
the header's background clips to the 8px radius.

S3 `slide14.body.html:10-24`, verbatim:

```html
<div class="code-block overflow-hidden">
    <div class="flex items-center gap-2 px-4 py-2" style="background:rgba(255,255,255,0.04);border-bottom:1px solid #333;">
        <div class="w-3 h-3 rounded-full bg-red-500"></div>
        <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
        <div class="w-3 h-3 rounded-full bg-green-500"></div>
        <span class="ml-2 text-xs opacity-50">assay &middot; zero API keys, zero dollars spent</span>
    </div>
    <div class="p-5 text-base leading-relaxed">
        <div><span style="color:#ff5640;">$</span> python -m harness.selftest</div>
        <div class="opacity-45 mb-3">&nbsp; 106 checks, about a second</div>
        <div><span style="color:#ff5640;">$</span> python -m harness.run --offline</div>
        <div class="opacity-45 mb-3">&nbsp; writes the gate record</div>
        <div><span style="color:#ff5640;">$</span> python -m pytest -q</div>
        <div class="opacity-45">&nbsp; 20 rows + the suite gate</div>
    </div>
</div>
```

The dots are Tailwind's `bg-red-500` / `bg-yellow-500` / `bg-green-500` — deliberately *not* the deck
palette; they are chrome, not argument. The label after the dots is the file path or the tool name plus
a claim (`harness/golden.py &middot; the real dataclass, no simplification`).

Prompt lines: `$` in `#ff5640`, command in default white, the output line immediately under it at
`opacity-45` with a leading `&nbsp;` and `mb-3` to group it with its command.

**Trap.** Reaching for `<pre>` or highlight.js. The decks never do; every line is a `<div>` so it can
carry Tailwind classes and per-token inline colour. Second trap: adding the three dots to every code
block — the plain form is the default and the header is for a terminal or a named file. Third: omitting
`overflow-hidden`, which leaves the header's grey fill sticking out past the rounded corners.

---

## 5. Badge

**CSS (head, verbatim):**

```css
.badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.85em;
    display: inline-block;
}
.badge-accent { background: var(--accent-color); color: white; }
.badge-success { background: var(--success-color); color: white; }
.badge-roi { background: var(--roi-color); color: var(--bg-color); }
.badge-warn { background: var(--warn-color); color: white; }
```

`badge-roi` is the only one with dark text — gold on white is unreadable, so `color: var(--bg-color)`.

Plain use, S3 `slide02.body.html:10` and `slide11.body.html:21`:

```html
<span class="badge badge-success">Session 2</span>
<span class="badge badge-warn">(a)</span>
```

Enlarged for a single-letter/rule label — override the padding inline, S3 `slide08.body.html:22` and
`slide04.body.html:12`:

```html
<span class="badge badge-accent text-lg" style="padding:6px 15px;">A</span>
<span class="badge badge-accent text-lg" style="padding:6px 16px;">R1</span>
```

Shrunk to ride inside a label, S3 `slide05.body.html:109`:

```html
<span class="badge badge-roi ml-1" style="font-size:0.6em; padding:2px 8px;">PAID</span>
```

**Fifth, unofficial variant: the neutral badge.** No class exists; it is written inline, 7 occurrences.
Use it for a fact that is not good, bad or the payoff — a count, a size, a config.

S3 `slide07.body.html:98` and S2 `slide6.html`:

```html
<span class="badge" style="background:rgba(255,255,255,0.10);color:rgba(255,255,255,0.8);">20 parametrized row tests + 1 suite-gate test</span>
<span class="badge" style="background:rgba(255,255,255,0.12);color:rgba(255,255,255,0.75);">55 files &middot; 4,442 LOC</span>
```

S3 uses `0.10 / 0.8`; S2 uses `0.12 / 0.75`. **Use S3's.**

The badge row — a centred strip of badges as a results summary, S3 `slide07.body.html:97-103`:

```html
<div class="flex items-center justify-center gap-4 mt-3 animate-entry delay-3">
    <span class="badge" style="background:rgba(255,255,255,0.10);color:rgba(255,255,255,0.8);">20 parametrized row tests + 1 suite-gate test</span>
    <span class="badge badge-success">18 passed</span>
    <span class="badge badge-warn">2 failed &middot; R02 &middot; R07</span>
    <span class="badge" style="background:rgba(255,255,255,0.10);color:rgba(255,255,255,0.8);">1 skipped &middot; paid judge row &middot; ASSAY_TIER=paid</span>
    <span class="text-sm opacity-60 italic ml-2">pytest and pyyaml. That is the entire dependency list.</span>
</div>
```

**Trap.** Using `badge-accent` as a generic tag. Coral is the deck's primary accent and a coral badge
reads as *this is the important one*. When a badge is just a label, it is neutral; when it is a status,
it is success/warn.

---

## 6. `.stamp` — the rubber stamp

**CSS (head, verbatim; present in S2 and S3, absent from S1):**

```css
.stamp {
    position: absolute;
    transform: rotate(-11deg);
    border: 3px solid var(--warn-color);
    color: var(--warn-color);
    font-weight: 700;
    letter-spacing: 0.18em;
    padding: 6px 18px;
    border-radius: 6px;
    background: rgba(25,43,55,0.72);
    white-space: nowrap;
}
```

`rgba(25,43,55,0.72)` is `--bg-color` at 72% — it lets a hint of the card show through while still
occluding whatever it lands on.

It appears on exactly two slides in the whole corpus (S2 slide5, S3 slide6) with exactly one string,
`ASSERTS NOTHING`, three times per slide. It is the deck's strongest visual and it is rationed.

### The layout rule (hard-won)

S2 slide5 positioned it from the top inside a fixed-height card with no reserved space:

```html
<!-- S2 slide5.html:183-193 — DO NOT COPY -->
<div class="relative glass-panel p-6 rounded-xl flex flex-col" style="height:288px;border-left-color:#2ecc71;">
    ...
    <p class="text-base opacity-85 flex-1">A well-written spec pointing at empty page. Green on every build, blind to everything.</p>
    <div class="stamp text-xl" style="left:34px;top:228px;">ASSERTS NOTHING</div>
</div>
```

`top:228px` in a 288px card is a magic number tuned by eye against one particular length of body copy.
Change the copy by a line and the stamp lands on it.

S3 fixed it — **bottom-anchor the stamp and reserve a padding lane in the card**:

```html
<!-- S3 slide06.body.html:9-21 — the house form -->
<div class="relative glass-panel p-6 rounded-xl flex flex-col" style="height:300px;border-left-color:#2ecc71;padding-bottom:74px;">
    <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-bold">The Loose Scorer</h3>
        <i class="fas fa-circle-check text-3xl" style="color:#2ecc71;"></i>
    </div>
    <div class="code-block p-3 text-sm leading-relaxed mb-4">
        <div><span class="opacity-45">scorer:</span> token_f1</div>
        <div><span class="opacity-45">threshold:</span> &gt;= 0.15</div>
        <div class="mt-1" style="color:#FFD700;">answer: ~200 words, fluent English</div>
    </div>
    <p class="text-sm opacity-85 flex-1">Any fluent English clears it. Green forever, on every build, for the rest of its life.</p>
    <div class="stamp text-lg" style="left:28px;bottom:20px;">ASSERTS NOTHING</div>
</div>
```

Three things make it work together, and all three are required:

1. `padding-bottom:74px` on the card — the lane. `flex-1` on the body paragraph stops *above* it.
2. `bottom:20px` on the stamp, not `top:` — it sits in the lane regardless of how tall the content is.
3. `position: relative` on the card, so the stamp's `position: absolute` resolves to the card.

Sizing: `text-lg` (S3) over `text-xl` (S2) — at `-11deg` with `letter-spacing:0.18em`, `text-xl` on a
255–300px card overhangs the card edge.

**Trap.** The naive version anchors from the top with a tuned `top:` value and no reserved padding.
It looks right in the one card you were staring at, and collides with the body copy in the other two —
which is exactly what S2 shipped and S3 corrected. Second trap: putting the stamp inside the `flex-1`
paragraph rather than as a sibling of it; absolute positioning then resolves against the wrong box.

---

## 7. The scale-drawn bar row

Three columns: **fixed-width label (right-aligned) | `flex-1` track | fixed-width value (right-aligned)**.
The track is `relative`, the fill is `absolute` with a `width:N%` that is hand-computed from a real
number and written as a literal.

S3 `slide05.body.html:9-20`, one row of eight:

```html
<div class="flex items-center gap-4">
    <div class="text-right" style="width:200px;">
        <div class="font-bold text-sm">exact</div>
        <div class="text-xs opacity-45 font-mono">normalised string equality</div>
    </div>
    <div class="flex-1 relative h-9">
        <div class="absolute left-0 top-0 h-full flex items-center px-4 rounded-r-lg" style="width:25%; background:rgba(143,163,176,0.16); border:1px solid rgba(143,163,176,0.4);">
            <span class="text-xs opacity-80">enum &middot; id &middot; code &mdash; cannot: free phrasing</span>
        </div>
    </div>
    <div class="text-right font-mono text-sm font-bold opacity-80" style="width:70px;">$0</div>
</div>
```

The eight widths on that slide are `25 / 35 / 45 / 55 / 65 / 75 / 85 / 100` — a ladder, not a
measurement, and the slide says so ("seven prices"). Where the bars *are* a measurement, the percentages
are the data. S1 `slide6.html:130-134`:

```html
<div class="relative w-full rounded" style="height:24px;background:rgba(255,255,255,0.05);">
    <div class="absolute left-0 top-0 h-full rounded-l" style="width:36%;background:rgba(255,255,255,0.16);"></div>
    <div class="absolute top-0 h-full" style="left:36%;width:20%;background:#FFD700;"></div>
    <span class="absolute font-mono text-xs" style="left:58%;top:3px;color:#FFD700;">+20.0</span>
</div>
```

Read that literally: baseline 36.0 → 56.0 is drawn as `width:36%` + a delta segment at `left:36%;
width:20%`, with the `+20.0` label parked at `left:58%` — 2 points past the end of the delta. The
sibling row is `43.9` → `58.0`: `width:43.9%`, delta `left:43.9%;width:14.1%`, label at `left:60%`.
**`43.9` and `14.1` are the data.** Nothing computes them at runtime; they are typed in, and the
caption under the group names the source (`two-proportion z-tests computed from Table 1 and the stated
eval sizes`).

Colour rule for a delta segment: `#FFD700` when the delta is the point, `#8fa3b0` when it is present
for comparison and not significant.

Highlighting one row out of the set — S3 `slide05.body.html:65-76` recolours the label, the fill and the
border, and leaves the geometry alone:

```html
<div class="font-bold text-sm font-mono" style="color:#FFD700;">contains_all</div>
...
<div class="absolute left-0 top-0 h-full flex items-center px-4 rounded-r-lg" style="width:65%; background:rgba(255,215,0,0.14); border:1px solid rgba(255,215,0,0.45);">
    <span class="text-xs font-bold" style="color:#FFD700;">the first rung where a loose threshold can lie to you</span>
</div>
```

**Trap.** Drawing bars whose widths are chosen to look balanced. Every bar in these decks either encodes
a real number or is openly declared a ladder, and the slide carries a mono `opacity-40/50` caption naming
the file or method the numbers came from. Second trap: using a flexbox width or a CSS `calc` for the
fill — it must be `position:absolute; width:N%` inside a `relative` track, or the label column stops
being a fixed lane and the bars stop lining up between rows. Third: forgetting `rounded-r-lg` on a fill
that stops short, or leaving it on a fill that runs to 100%.

---

## 8. The "value exceeds the frame" jagged-break bar

For a quantity so far past the axis that drawing it to scale is impossible. Used once, S2
`slide2.html`, for ~14,000,000 tokens against a 1,050,000-token window.

The bar has **no fixed track**: the fill is `absolute left-0 right:52px`, its right border is removed,
and a gradient-to-transparent plus three chevrons stand in for the missing end.

```html
<!-- S2 slide2.html — BAR 2, one page's computed styles, breaking off the edge -->
<div class="flex items-center gap-6 mt-4 animate-entry delay-3">
    <div class="text-right" style="width:230px;">
        <div class="font-bold text-lg leading-tight">ONE page's styles</div>
        <div class="text-xs opacity-50 font-mono">1,909,248 properties</div>
    </div>
    <div class="flex-1">
        <div class="relative w-full" style="height:74px;">
            <div class="absolute left-0 top-0 h-full rounded-l-lg" style="right:52px;border:1px solid rgba(231,76,60,0.5);border-right:none;background:rgba(231,76,60,0.16);"></div>
            <div class="absolute inset-y-0 left-0 flex items-center pl-6">
                <span class="text-2xl font-bold font-mono" style="color:#e74c3c;">~14,000,000 tokens</span>
            </div>
            <!-- the jagged break -->
            <div class="absolute top-0 h-full" style="right:0;width:56px;background:linear-gradient(90deg, rgba(231,76,60,0.16), rgba(25,43,55,0));"></div>
            <div class="absolute top-0 h-full flex flex-col justify-between" style="right:44px;">
                <span class="text-3xl font-bold leading-none" style="color:#e74c3c;">&#8250;</span>
                <span class="text-3xl font-bold leading-none" style="color:#e74c3c;">&#8250;</span>
                <span class="text-3xl font-bold leading-none" style="color:#e74c3c;">&#8250;</span>
            </div>
        </div>
    </div>
    <div class="text-right font-mono" style="width:150px;">
        <div class="text-3xl font-bold" style="color:#e74c3c;">&times;13</div>
        <div class="text-xs opacity-50">the whole window,<br>for one page</div>
    </div>
</div>
```

The four parts: `rounded-l-lg` + `border-right:none` (the bar is cut, not closed); the 56px gradient
fading the fill into `rgba(25,43,55,0)` = the page background; three `&#8250;` chevrons at `right:44px`
in a `justify-between` column so they spread over the bar's full height; a multiplier in the value
column instead of a number, because the number is meaningless at that scale.

Its sibling bar on the same slide *is* to scale and overflows in-frame, using a repeating stripe for
the over-budget part plus a marker line that both bars share:

```html
<div class="absolute left-0 top-0 h-full" style="width:80.05%;background:rgba(255,86,64,0.30);"></div>
<div class="absolute top-0 h-full" style="left:80.05%;right:0;background:repeating-linear-gradient(45deg, rgba(231,76,60,0.30) 0 10px, rgba(231,76,60,0.10) 10px 20px);"></div>
```

with the axis marker placed above at the identical percentage:

```html
<div class="absolute bottom-0 pl-4 flex flex-col justify-end" style="left:80.05%;height:58px;border-left:2px solid #ff5640;">
    <div class="font-bold text-lg leading-none" style="color:#ff5640;">1,050,000 tokens</div>
    <div class="text-xs opacity-50 font-mono mt-1">the whole frontier window. Everything right of this line is never seen.</div>
</div>
```

`80.05%` is 1,050,000 / 1,311,725, typed in three times on one slide.

**Trap.** Drawing the huge value to scale and shrinking everything else to a sliver — the small bars
then carry no information. Second trap: using the break bar for a value that *would* fit; a break is a
statement that the axis has given up, and it costs its credibility if used decoratively. Third: the
gradient must fade to the page background (`rgba(25,43,55,0)`), not to `transparent` — Safari and
older Chrome interpolate `transparent` through black and leave a grey smear.

---

## 9. The interval / range bar

A floating bar positioned by `left:%` **and** `width:%`, both ends meaningful, drawn inside a visible
empty track. Used on S3 slide9 for five Wilson 95% confidence intervals on a common 0–100% axis, plus a
1px–2px white tick at the point estimate.

S3 `slide09.body.html:18-25`, the highlighted row:

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

and a non-highlighted row:

```html
<div class="flex items-center gap-3 mb-1.5">
    <div class="text-right font-mono text-xs opacity-60" style="width:150px;">1,800 / 2,000</div>
    <div class="flex-1 relative" style="height:26px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.1);border-radius:4px;">
        <div class="absolute top-0 h-full rounded" style="left:88.6%;width:2.6%;background:#2ecc71;opacity:0.55;"></div>
        <div class="absolute top-0 h-full" style="left:89.6%;width:2px;background:white;"></div>
    </div>
    <div class="font-mono text-xs opacity-60" style="width:210px;">[88.6%, 91.2%] &middot; 2.6pp</div>
</div>
```

Every number is checkable against the value column: `left` = lower bound, `width` = upper − lower, and
the value column prints `[lower, upper] · width pp`. 69.9 + 27.3 = 97.2. 88.6 + 2.6 = 91.2. The white
tick is the point estimate (18/20 = 90%, drawn at `left:89.6%` — the 0.4pp offset centres the 2px tick).

Emphasis is done with three things and no change of geometry: track height `30px` vs `26px`, a tinted
track (`rgba(255,86,64,0.06)` + a 50%-alpha border instead of `rgba(255,255,255,0.03)` + 10%), and fill
opacity `0.75` vs `0.55`. Colour encodes the verdict: `#ff5640` for our suite, `#8fa3b0` for neutral
comparisons, `#2ecc71` for "wide enough n".

The axis labels sit under the group, padded by the exact column widths so they land on the track:

```html
<div class="flex justify-between text-xs font-mono opacity-35 mt-1" style="padding-left:162px;padding-right:222px;">
    <span>0%</span><span>50%</span><span>100%</span>
</div>
```

`162px` = the 150px label column + the 12px (`gap-3`) gutter. `222px` = 210px + 12px. If you change a
column width, change these.

**Trap.** Anchoring the interval at `left:0`, which turns a confidence interval into a magnitude bar and
silently reverses the slide's argument. Second trap: letting the axis labels be `justify-between` on the
full row instead of on the padded lane — they then sit under the label column and the intervals cannot
be read off them. Third: computing the intervals in your head. These are Wilson score intervals; the
deck says "Wilson" on the slide and explicitly refuses to put a Wald half-width on the same axis.

---

## 10. The `grid-cols-12` decision table

A table with no `<table>`. One `.glass-panel ... overflow-hidden` shell with a neutral `#8fa3b0` stripe,
one header row, then N body rows, each a `grid grid-cols-12` with a top hairline. Column split is
**3 / 5 / 4** in both decks that use it (S2 slide13, S3 slide13), and it is always the same three
columns: *what we did not build* / *the measured reason* / *what would change our mind*.

S3 `slide13.body.html:6-18`, header plus first row, verbatim:

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
    <!-- four more rows, identical shape -->
</div>
```

Fixed per-column typography, and it is what makes the table readable at projector distance:

| Column | Classes |
|---|---|
| 1 — the thing | `col-span-3 font-bold text-base` |
| 2 — the reason | `col-span-5 text-sm opacity-80` |
| 3 — the trigger | `col-span-4 text-sm opacity-70 font-mono` + `style="color:#FFD700;"` |

Header row: `px-6 py-2 text-[11px] font-mono uppercase tracking-widest opacity-40` on
`rgba(255,255,255,0.04)`. Body rows: `px-6 py-2 items-center`, separated by
`border-top:1px solid rgba(255,255,255,0.07)` — the first body row carries it too, so the header is
underlined by the same hairline. No zebra striping, no vertical rules, no `border-bottom` on the last
row (the shell's `overflow-hidden` + `rounded-xl` closes it).

The `text-[11px] font-mono uppercase tracking-widest opacity-40/50` micro-label is a house idiom beyond
this table — it also labels sub-blocks inside cards (S3 slide4 `Five things that may never become an
expected value`, S3 slide12 `the fix, in the mechanism`, S3 slide14 `the open question`).

**Trap.** Making the third column prose. Gold + mono is a promise that the cell is a *falsifiable
trigger* — "a team that will not review a golden-set diff in a pull request", "never. This one is
arithmetic." A paragraph of reasoning there breaks the contract the column's styling makes. Second
trap: reaching for a real `<table>`; the 12-col grid is what lets a cell be `items-center`-aligned
against a two-line neighbour without `vertical-align` fights.

---

## 11. Bottom-right nav cluster and keyboard script

**Generated, not hand-written.** `generate_s3_deck.py:173-196` emits both the cluster and the script
into every slide file; they are the last things in `<body>` before `</body>`. Never hand-edit them in a
slide, and never put them in a body fragment.

The generator (verbatim; `{...}` are Python f-string braces, `{{...}}` emits a literal brace):

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

Rendered output on slide 2 of 14, verbatim from `S3 deck/slide2.html`:

```html
<div class="absolute bottom-6 right-8 flex items-center gap-6 z-50">
    <span class="text-sm opacity-40 font-mono">SLIDE 02 / 14</span>
    <a href="slide1.html" class="nav-btn text-2xl"><i class="fas fa-chevron-left"></i></a>
    <a href="slide3.html" class="nav-btn text-2xl"><i class="fas fa-chevron-right"></i></a>
</div>
```

CSS dependency:

```css
.nav-btn { transition: all 0.3s; opacity: 0.5; }
.nav-btn:hover { opacity: 1; transform: scale(1.1); color: var(--accent-color); }
```

Notes that matter:

- `z-50` — the cluster must beat every `absolute`-positioned diagram element (S3 slide7's boxes sit at
  default z-index; the `.mcp-packet` rule uses `z-index: 8`).
- On slide 1, `PREV` is the string `"#"` and the `if (PREV !== '#')` guard swallows the keypress; the
  anchor still renders, pointing at `#`. Same for `NEXT` on the last slide.
- `' '` (Space) and `PageDown` advance — presenter remotes send `PageDown` / `PageUp`.
- `index.html` is a meta-refresh stub, not a frame: `<meta http-equiv="refresh" content="0;url=slide1.html">`.

**Trap.** Hand-writing the cluster per slide and getting `SLIDE 07 / 14` off by one, or leaving
`TOTAL_SLIDES` stale in the `End` handler. Second trap: a global listener in a slide body that also
binds Space/arrows — it will fight this one (see §13 for the one sanctioned way to take the keys back).
Third: this listener is registered *after* anything in the body, so a body listener that calls
`stopImmediatePropagation()` wins. That ordering is load-bearing.

---

## 12. The giant faint background glyph

One Font Awesome icon at `text-[400px]`, `opacity-5`, white, floating, behind everything.

Hero / title slide, dead-centred behind the stack — S3 `slide01.body.html:1-2`:

```html
<div class="h-screen w-screen flex flex-col items-center justify-center relative overflow-hidden">
    <i class="fas fa-flask absolute text-[400px] opacity-5 text-white animate-float -z-10"></i>
    <div class="text-center z-10 animate-entry">
```

Three required companions: `relative overflow-hidden` on the slide frame (or the glyph produces a
scrollbar on an `overflow:hidden` body and bleeds into the next slide's print page), `-z-10` on the
glyph, and `z-10` on the content stack.

One glyph per deck, chosen as the deck's subject: `fa-diagram-project` (S1, RLM/recursion),
`fa-terminal` (S2, REPL harness), `fa-flask` (S3, evaluation). Reuse it on the closing slide if the
deck has one, corner-anchored and one size up — S1 `slide10.html`:

```html
<div class="h-screen w-screen p-16 flex flex-col justify-center relative overflow-hidden">
    <i class="fas fa-terminal absolute text-[420px] opacity-5 text-white animate-float -z-10" style="right:-50px;bottom:-70px;"></i>
```

CSS dependency:

```css
@keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
.animate-float { animation: float 6s ease-in-out infinite; }
```

and the print freeze, which is why it survives PDF export:

```css
@media print { .animate-float, .animate-pulse, .mcp-packet { animation: none !important; } }
```

**Trap.** Raising the opacity. `opacity-5` (5%) is the only value used, on all four occurrences; at 10%
it competes with the h1 on a projector. Second trap: putting a glyph on interior slides — only 4 exist
across 38 slides, all on hero/closing slides. Third: omitting `overflow-hidden`, which is what keeps a
400px glyph inside a 1080px frame.

---

## 13. The video slide (S2 slide11)

The only video in the corpus. Four parts, all of them required.

### a. The frame

`px-12 py-8` instead of `p-12` (the video needs the vertical room), and a two-beat header — h2 and
subtitle on one `items-baseline` line instead of stacked:

```html
<div class="h-screen w-screen px-12 py-8 flex flex-col justify-center">
    <div class="mb-1 text-[#FFD700] font-mono tracking-widest uppercase text-sm animate-entry">One Container, Offline, 2:31 &middot; Nothing Below Is Re-enacted</div>
    <div class="flex items-baseline gap-5 animate-entry">
        <h2 class="text-5xl font-bold">Watch It Refuse a Test</h2>
        <p class="text-lg opacity-70">A whole run, end to end: URL in, one spec written, one <b>quarantined with a reason</b>.</p>
    </div>
```

### b. The `<video>`

Sized off viewport height so it never pushes the payoff column off the slide. `print-hide` because a
`<video>` paints nothing in a PDF.

```html
<div class="mx-auto" style="width:min(100%, calc(64vh * 1.6));">
    <video id="vizdemo" tabindex="0" controls muted playsinline preload="metadata"
           poster="media/viz-demo-poster.jpg"
           src="media/viz-demo.mp4"
           class="block rounded-xl mx-auto print-hide"
           style="height:64vh;aspect-ratio:16/10;width:auto;max-width:100%;object-fit:contain;background:#0d161c;border:1px solid rgba(255,255,255,0.14);box-shadow:0 18px 60px rgba(0,0,0,0.45);">
    </video>
```

`tabindex="0"` is what makes the focus handoff in (d) possible. `muted` + `playsinline` + a `poster`
are non-negotiable: no autoplay, nothing to unmute, and a first frame before the metadata loads.

### c. The print-only poster fallback

```html
    <!-- PDF fallback: a <video> paints nothing in print, so the poster frame stands in. -->
    <img class="print-only rounded-xl mx-auto" src="media/viz-demo-poster.jpg"
         alt="viz at 0:50 - offloading headline, live agent tree, volatility fan-out to 4 workers"
         style="height:64vh;width:auto;max-width:100%;object-fit:contain;background:#0d161c;border:1px solid rgba(255,255,255,0.14);box-shadow:0 18px 60px rgba(0,0,0,0.45);">
    <div class="print-only mt-3 text-center text-sm leading-relaxed">
        <b style="color:#FFD700;">Still frame at 0:50 &mdash; the 2:31 video cannot play inside a PDF.</b><br>
        <span class="opacity-70">Watch the run at <span class="font-mono">stendavatestcafe7f5369.z6.web.core.windows.net/session2/slide11.html</span><br>
        or open <span class="font-mono">deck/slide11.html</span> &middot; file <span class="font-mono">deck/media/viz-demo.mp4</span></span>
    </div>
```

CSS dependency (head):

```css
.print-only { display: none; }
@media print {
    .print-hide { display: none !important; }
    .print-only { display: block !important; }
}
```

The `<img>` carries the *same* inline style as the `<video>` so the PDF page has identical geometry,
and the caption tells a PDF reader where to get the real thing.

### d. The keyboard-focus handoff IIFE

Placed in the slide body, i.e. **before** the generated nav `<script>` — the comment in the source says
so, and the ordering is the whole mechanism.

```html
<div id="keyhint" class="mt-3 mx-auto w-fit px-4 py-1.5 rounded-full text-sm font-mono print-hide" style="border:1px solid rgba(255,255,255,0.18);"></div>
```

```html
<script>
  (function () {
    var v = document.getElementById('vizdemo');
    var hint = document.getElementById('keyhint');
    // keys the <video> and the deck both want
    var GRAB = [' ', 'Spacebar', 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'PageUp', 'PageDown'];
    function paint() {
      if (document.activeElement === v) {
        hint.innerHTML = '<i class="fas fa-keyboard mr-2"></i>the <b>video</b> has the keys — Space plays, ← → scrub &middot; <b>Esc</b> hands them back';
        hint.style.color = '#FFD700';
        hint.style.borderColor = 'rgba(255,215,0,0.55)';
      } else {
        hint.innerHTML = '<i class="fas fa-keyboard mr-2"></i>the <b>deck</b> has the keys — Space / → advances &middot; click the video to hand them over';
        hint.style.color = 'rgba(255,255,255,0.6)';
        hint.style.borderColor = 'rgba(255,255,255,0.18)';
      }
    }
    v.addEventListener('focus', paint);
    v.addEventListener('blur', paint);
    // registered before get_nav's listener, so stopImmediatePropagation wins
    document.addEventListener('keydown', function (e) {
      if (e.target !== v && !v.contains(e.target)) return;
      if (e.key === 'Escape') { v.blur(); paint(); return; }
      if (GRAB.indexOf(e.key) !== -1) { e.stopImmediatePropagation(); }
    });
    paint();
  })();
</script>
```

How it works: both listeners are on `document`, so DOM order decides which runs first. This one runs
first, and *only* acts when the event target is the video — then `stopImmediatePropagation()` prevents
the nav listener from ever seeing the key. Click elsewhere or press `Esc` and the video blurs, the
guard falls through, and the deck has the keys back. `#keyhint` says which, at all times.

### e. Scrub cues

A 4-up row of timestamps under the video, with the two you intend to pause on tinted:

```html
<div class="grid grid-cols-4 gap-3 mt-4">
    <div class="p-2 rounded-lg text-center" style="background:rgba(255,255,255,0.04);">
        <div class="font-mono text-lg font-bold">0:09</div>
        <div class="text-xs opacity-60 mt-0.5">URL submitted</div>
    </div>
    <div class="p-2 rounded-lg text-center" style="background:rgba(255,215,0,0.10);border:1px solid rgba(255,215,0,0.32);">
        <div class="font-mono text-lg font-bold" style="color:#FFD700;">0:46</div>
        <div class="text-xs opacity-75 mt-0.5">fan-out, <b>4 workers</b> &mdash; pause here</div>
    </div>
    <!-- 1:35 neutral, 2:20 coral -->
</div>
```

The payoff column beside the video is a fixed `width:420px;flex:none;` stack of a
`glass-panel-success` ("the one it kept", with the code) and a `glass-panel-warn` ("the one it
refused", with the verbatim machine-written reason).

**Trap.** Shipping the `<video>` with no `print-only` sibling: the PDF export then has a blank slide
where the demo was, and the whole point of the deck's print CSS is that the PDF is a real artefact.
Second trap: registering the focus IIFE after the nav script (or in the generator's footer), which
makes `stopImmediatePropagation()` a no-op and lets Space both play the video and advance the slide.
Third: `autoplay` — the decks never use it; the speaker presses play.
