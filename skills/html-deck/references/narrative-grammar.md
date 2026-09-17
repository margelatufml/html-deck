# Narrative grammar

The rhetorical contract of the house style. Layout is in the other reference files; this one is what
makes a deck *good*. Source of truth: the three delivered decks (Session 1, 10 slides · Session 2,
14 · Session 3, 14) plus their `SPEAKER_NOTES.md` and `PRESENTING.md`.

**Where the decks disagree, Session 3 wins.** It is the most evolved: it is the only one whose slide
bodies live in separate `slides/slideNN.body.html` fragments, and the only one that separates the
statistical honest slide (9) from the scope/trigger table (13). (Print/PDF CSS is on every slide of
both S2 and S3, and on none of S1 — that one is not an S3 innovation.)

---

## 1. The one-sentence contract

> Every clean claim is immediately punctured by the author, with a number, before the audience can
> raise it. The deck's credibility comes from the slides where the author looks worst.

A deck that only argues *for* its thesis is off-style, however pretty.

---

## 2. Deck shape

| Section | S1 (10) | S2 (14) | S3 (14) | What it does |
|---|---|---|---|---|
| Title | 1 | 1 | 1 | Promise + receipts strip |
| Recap / hook | — | 2 | 2–3 | One slide of prior session, then the new problem |
| Theory | 2–5 | 3–5 | 4–6 | The rules everything else falls out of |
| Build / evidence | 6–7 | 6–11 | 7–9 | The artefact, measured on this machine |
| Critical thinking | 8–9 | 12–13 | 10–13 | Judge limits, self-review, the review of my own work, triggers |
| Close | 10 | 14 | 14 | Ask · unknowns · open question |

Declared verbatim in the speaker notes:

- S2: `Theory: slides 2-5. Build: 6-11 (11 is the recorded run). Critical thinking: 12-14.`
- S3: `Theory: slides 2-6. Build: 7-9. The judge: 10-12. Critical thinking: 13-14.`

Proportions to reproduce: theory ≈ 30%, build/evidence ≈ 30%, critical thinking + close ≈ 30%,
title + recap ≈ 10%. **The critical-thinking block is never smaller than the theory block.**

Two structural rules from the source decks:

1. **Theory is "two rules", never more.** S2 slide 3 and S3 slide 4 are both titled *The Theory, In
   One Screen* and both carry exactly R1 and R2. The speaker notes both say: say them as numbers,
   twice.
2. **The theory block ends on a trap slide.** S2 slide 5 *A Generator That Always Passes*, S3 slide 6
   *Three Suites That Always Pass*. Three cards, each stamped `ASSERTS NOTHING`, each one plausible.
   Both notes call this "the hinge of the talk" and "the slide to slow down on". This is the slide
   that turns the deliverable from the artefact into the proof the artefact works.

---

## 3. Per-slide grammar

Every content slide, in order, top to bottom:

| Element | Rule | Example |
|---|---|---|
| Eyebrow | 2–5 words, uppercase mono, coral `#ff5640`. Names the *rhetorical move*, not the topic | `The Objection` · `The Honest Slide` · `Where a Claim Becomes a Fact` |
| Headline | A claim with a verb, never a topic label | `Pixels See What Structure Cannot`, not `Visual vs Structural Testing` |
| Subhead | One line, carries the provenance of the whole slide | `Both panels are the paper's own numbers, from its own Table 1 and its own ablation.` |
| Body | Panels, bars, code, tables — the evidence |  |
| Source strip | Mono, `opacity-40`, paths/commands/paper ids | `python3 -m harness.measure · runs/measurements.json · 8 routes, 4,089 nodes` |
| Counter-evidence | `glass-panel-warn`, red bold lead-in | §5 |
| Closer | `glass-panel-alt`, one bold sentence | §8 |

Eyebrows that recur across decks and should be reused: `The Theory, In One Screen` · `The Build` ·
`Where a Claim Becomes a Fact` · `The Honest Slide` · `The Adversarial Review of My Own Harness` ·
`Scope, With Triggers` · `Your Turn — Laptops Open`.

Eyebrows carry provenance too when the slide is a measurement:

```html
<div class="mb-3 text-[#ff5640] font-mono tracking-widest uppercase text-sm animate-entry">The Honest Slide &middot; every interval recomputed on this machine</div>
```

S1 and S2 vary the eyebrow colour slide by slide (`#ff5640`, `#e74c3c`, `#FFD700`, `#2ecc71`); S3
standardises on coral for all fourteen except slide 13, which is gold because the whole slide is
triggers. **Use S3’s convention: coral everywhere, gold only for the trigger table.**

---

## 4. Evidence discipline

**Every number carries its provenance in the same breath.** Not in a footnote, not on a sources
slide — in the sentence, or in a mono strip directly under the figure.

Four provenance forms, all in use:

| Form | Example |
|---|---|
| The run | `Session 2 · viz/runs/gates-proof/events.jsonl · the guard fired 0 times in that run` |
| The file / command | `python -m harness.selftest → 106 checks passed` |
| The app it was measured on | `measured on linear.app with Playwright + tiktoken o200k_base` |
| The source id, with its domain | `2604.25235, vision — a strong prior, not a text measurement` |

Subrules, all checkable:

- **A paper number is labelled with the paper id.** `Self-critique measurably collapses performance
  (2402.08115)`.
- **A number measured in another domain says so, every time it appears.** S3 slide 10 and slide 13
  both re-flag `2604.25235` as *vision*.
- **A statistic names which statistic it is.** S3 slide 9: `That is a Wald half-width; the intervals
  above are Wilson. Different statistics — do not put them on the same axis.`
- **When the source records a direction and no magnitude, print no magnitude.** S3 slide 11: `The
  source records this directionally — no percentage delta in it, so none is printed here.` The
  speaker note is blunter: inventing it "would be the exact failure this deck is about".
- **n is always printed next to a rate.** `86.7% agreement, Cohen's kappa 0.42, n=15`.

### The don't-mix-ratios rule — Session 2, slide 7, verbatim

```html
<div class="glass-panel-warn p-4 rounded-xl mt-4 animate-entry delay-4">
    <p class="text-base"><b style="color:#e74c3c;"><i class="fas fa-triangle-exclamation mr-2"></i>Cite every number against the app it came from.</b> On <b>this demo app</b> DOM-over-aria is <b class="font-mono">1.93&times;</b> &mdash; not the <b class="font-mono">104&times;</b> measured on linear.app. The demo is hand-written HTML with no framework wrapper-div bloat. The 104&times; belongs to the real SPA; the 6,390&times; belongs to this run. <b>Mixing them is how a deck stops being true.</b></p>
</div>
```

The speaker note for that slide states the reason: *"the moment a client's engineer reproduces 1.93x
on their own hand-written page, everything else I said becomes suspect."*

Two ratios measured on different things never appear in the same sentence unless the sentence is
about the fact that they differ.

---

## 5. Puncture your own diagram

Every clean claim gets a counter-evidence callout on the **same slide**, phrased as *said before
anyone raises it*. It is `glass-panel-warn`, it sits after the body and before the closer.

Session 2, slide 4 — verbatim:

```html
<div class="mt-4 glass-panel-warn p-4 rounded-xl animate-entry delay-4">
    <p class="text-base"><b style="color:#e74c3c;">The counter-evidence, said out loud before anyone raises it:</b> aria drops layout, and layout is literally our task. That is exactly why pixels stay in the loop instead of being replaced by the tree &mdash; and why the model still never sees one.</p>
</div>
```

Session 3, slide 5 — verbatim:

```html
<div class="mt-3 glass-panel-warn p-3 rounded-xl animate-entry delay-3">
    <p class="text-sm"><b style="color:#e74c3c;">Cheap is not the same as correct, said before anyone raises it:</b> <span class="font-mono">contains_all</span> with a threshold of 0.15 is free, deterministic, and asserts nothing. The ladder tells you what a scorer <i>costs</i>, not whether it <i>works</i>. That is the next slide.</p>
</div>
```

Lead-in phrasings actually used: *"The counter-evidence, said out loud before anyone raises it:"* ·
*"said before anyone raises it:"* · *"Owned on the record:"* · *"Be honest about the limit"* ·
*"Reality check before you draw this on a whiteboard:"* · *"Read it honestly:"*.

Density in the delivered decks (counting rendered panels, not the CSS rule): 1–3 on a normal slide,
6 on S3 slide 10, which is nothing but ceilings. Slides with zero: the trap slide, the build slide,
and the objections slide — where the whole slide is already the counter-argument.

The puncture is specific and costed. It names the case where the claim fails:

- `Owned on the record: D's geometric mutant is near-blind when the clip is the mutated element` — S2 slide 9
- `the guard fired 0 times in that run — architecturally present, empirically unexercised` — S3 slide 2
- `We compare serialised outputs, which is strictly weaker than comparing pixels. Say this out loud.` — S3 slide 2

---

## 6. The honest slide

One dedicated slide near the end whose job is to make the author look worst, with real numbers. Two
kinds exist; S3 ships both, and that is the model to copy.

**Kind A — the statistical self-undercut (S3 slide 9, eyebrow `The Honest Slide`).** It attacks the
deck's own headline offer. The session sells twenty rows; the slide prints:

- `A perfect 20/20 is still consistent with a true pass rate of 83.9%.`
- `A 20-row suite shows no drop at all 25.0% of the time when the true pass rate falls from 90% to 80% — and the degraded run scores higher 12.8% of the time.`
- Closer: `Twenty rows is a smoke test with receipts. It is not a benchmark …`

The speaker note: *"Say that even though the session sells twenty rows."*

**Kind B — the adversarial review of my own work (S2 slide 12, S3 slide 12).** Not a confession — a
method. The framing is fixed: reviewers were told to **break the rules, not to check the rules were
documented.** Three or four findings, each in three columns: the rule, the hole with real output,
and the fix *in the mechanism* with `file.py:line`.

Real findings, verbatim:

- `353 LOC of gates were decorative. Every "produced 0 specs" run was this bug, not the agent being appropriately careful. We were reading modesty into a crash.` (S2)
- `95 checks passed # … on a harness where an online judge was setting a gate bit.` (S3)
- `Row R01's expected value is byte-identical to str(triage(R01.input)) — a snapshot of the feature under test — and it loaded clean, because its provenance simply did not start with that word.` (S3)

Both end on a generalisation that is a testing lesson before it is an AI one:

- `A rule in a prompt is a wish. A rule in a mechanism is a rule.` (S2)
- `A denylist is a list of the ways you already thought of.` (S3)
- `Every one of these was invisible to the ninety-five checks that already existed.` (S3)

Delivery note, both decks: *steady, no apology, no jokes.* S3 PRESENTING.md adds: *"let it be quiet
afterwards. That's fine."*

---

## 7. The trigger table

One table slide listing what was deliberately **not** built. Three columns, fixed:
`Not built` | `Why — the measured reason` | `What would change our mind`.

The third column is the whole point: **every row is a falsifiable condition, never a principle.**
S3 slide 13 subhead: *"each is a decision with a written trigger, so someone can come back in six
months and pull one."*

```html
<div class="grid grid-cols-12 px-6 py-2 items-center" style="border-top:1px solid rgba(255,255,255,0.07);">
    <div class="col-span-3 font-bold text-base">No reviewer agent, no critic, no self-check pass</div>
    <div class="col-span-5 text-sm opacity-80">This exact pattern is measured to <b>collapse</b> (2402.08115). The mutation gate is the reviewer.</div>
    <div class="col-span-4 text-sm opacity-70 font-mono" style="color:#FFD700;">a critic that measurably raises kill rate on a held-out mutant class</div>
</div>
```

Good triggers (real):

| Not built | Trigger |
|---|---|
| A retrieval index | `a repo where rg over the route set exceeds the turn budget` |
| An approve/reject UI | `a team that will not review baselines in a pull request` |
| Depth ≥ 2 recursion | `a route corpus that will not fit one sub-call` |
| LPIPS / SSIM | `a metric that kills the 3px mutant and ignores antialiasing` |
| No embedding index | `the golden set no longer fits in one file a human reads` |

One row may have **no** trigger, and must say why it never will. The S3 row, all three columns:

| Not built | Why — the measured reason | What would change our mind |
|---|---|---|
| No self-consistency voting, no best-of-n | `Resampling cannot lower a verifier's false-positive rate: accuracy is capped at (1−p) regardless of compute, and the optimal attempt count is often fewer than ten (2411.17501).` | `never. This one is arithmetic.` |

The table always ends with a commercial refusal — the case where the audience should not build this
at all, stated in a warn panel:

> `If your AI feature is a classifier with a fixed label set, you do not need any of this.` You need
> `assertEqual`, two hundred rows and an afternoon. This harness earns its keep when the output is
> open-ended and the expected value is a judgement. **Saying so is worth more than the engagement.**

S2's equivalent: *"If a client asks for this on a saucedemo-sized app, saying **no** is the
higher-value consulting answer — and it is worth more trust than the engagement."*

---

## 8. The planted payoff

One sentence early in the deck is explicitly cashed in later, by slide number, on the slide itself.
It is set in mono, low opacity, under the theory panel — it reads as an aside and it is the hook
that buys the middle of the deck.

**Session 2, slide 3 → slide 12:**

```html
<p class="text-base opacity-85">R1 is what it may <b>see</b>. R2 is what it may <b>spend</b>. That asymmetry <i>is</i> the contract &mdash; and both were enforced by a paragraph of prompt until slide&nbsp;11.</p>
```

cashed on slide 12: *"Two rules generate the entire design. The review found both were enforced by
**asking the model nicely**."*

**Session 3, slide 4 → slide 12:**

```html
<div class="mt-3 text-sm font-mono opacity-55 text-[#ff5640] animate-entry delay-3">Both of these were enforced by a paragraph in the README until slide 12.</div>
```

cashed on slide 12: *"I pointed three reviewers at this repo and told them to **break the two rules
from slide 4** — not to check that the rules were documented."*

PRESENTING.md marks both with the same instruction and a different price: S3 *"Plant the hook — this
buys you the next eight slides"*, S2 *"Plant the hook — this buys attention for the next 20 minutes"*.

Second-order planting: the deck also plants forward with `builds on slide 5` badges (S3 slide 3) and
pays back across sessions — S3 slide 9 and slide 11 both quote Session 1 verbatim, in quotes, with
the session named. **A callback is quoted, never paraphrased.**

---

## 9. The closer strip

Every content slide ends with one bold quotable sentence in a `glass-panel-alt` (or `-warn` when the
sentence is a warning, or a bare tinted strip). It is the last thing on the slide before the nav.
Session 3 has one on every slide 2–13; Session 1's are lead-in-plus-sentence and less aphoristic —
**Session 3's aphoristic form wins**, though S3 itself still uses the lead-in variant on slide 12
(`A denylist is a list of the ways you already thought of.` + a continuation clause).

```html
<div class="mt-4 glass-panel-alt p-4 rounded-xl animate-entry delay-4">
    <p class="text-xl font-bold">R1 decides whether the row is a test. R2 decides whether the answer is evidence.</p>
</div>
```

Third variant, a bare tinted strip instead of a panel (S3 slide 7):

```html
<div class="w-full text-center mt-3 py-3 rounded-lg animate-entry delay-4" style="background:rgba(255,86,64,0.08);border:1px solid rgba(255,86,64,0.3);">
    <span class="text-lg font-bold">Everything above the line is arithmetic. That is why it costs nothing, never flakes, and can be read on a projector.</span>
</div>
```

Variant with a quieter second line (S2 slide 13):

```html
<div class="mt-5 glass-panel-alt p-4 rounded-xl animate-entry delay-4">
    <p class="text-xl font-bold">&ldquo;The demo app lies to you. It is small, hand-written and cooperative, and your client's app is none of those.&rdquo;</p>
    <p class="text-sm opacity-65 mt-1">If a client asks for this on a saucedemo-sized app, saying <b>no</b> is the higher-value consulting answer &mdash; and it is worth more trust than the engagement.</p>
</div>
```

Variant with a bold lead-in (S1 form):

```html
<div class="mt-5 glass-panel-alt p-4 rounded-xl animate-entry delay-4">
    <p class="text-base opacity-90"><b class="text-[#FFD700]">Read it honestly:</b> no rung is a smarter model. It is the same model handed more room to act &mdash; and a longer list of things that can go wrong while nobody is watching.</p>
</div>
```

### The register — every real closer, all three decks

Session 1:
- `Models got better at answering. All the interesting work moved to what surrounds them.`
- `The opposite bet, same month: Strix — 38 tool schemas plus compaction, 58,000 stars. Both are shipping. Neither has won.`
- `An Automation Engineer would have failed that in code review. Nobody has hired you to break this work yet.`
- `What to build: the REPL first. Treat sub-calls as a measured add-on, not as the architecture.`

Session 2:
- `This is not a big-context problem. It is a wrong-shape problem.`
- `A handle costs forty tokens. The thing it points at costs a hundred thousand.`
- `A green test with nothing behind it is not a test. It is an alibi.`
- `Mixing them is how a deck stops being true.`
- `Stability is not evidence.`
- `That is why the pixels are still necessary — and why the model still never sees one.`
- `A rule in a prompt is a wish. A rule in a mechanism is a rule.`

Session 3:
- `Every one of these is an argument about the oracle, not about AI. We have been having this argument since the first person wrote assertEquals.`
- `Nineteen rows of arithmetic and one model call is not a compromise. It is the design.`
- `The deliverable is not the twenty rows. It is the proof that the twenty rows can go red.`
- `Everything above the line is arithmetic. That is why it costs nothing, never flakes, and can be read on a projector.`
- `Twenty rows is a smoke test with receipts. It is not a benchmark — and tonight you leave with a harness that prints that on its own report.`
- `A judge you have not validated is a coin flip with a vocabulary.`
- `The fix is not a better critic prompt. It is a sound external verifier returning one bit — and you already have one. It is called assert.`
- `A denylist is a list of the ways you already thought of.`
- `None of these are principles. Every one is a decision with a trigger, written down.`

Shared shape: two clauses, the second one reversing or costing the first. Most are 8–18 words. None
restates the slide title. None contains a hedge.

---

## 10. The close

The last slide has exactly four parts and **no recap**. Nothing in any of the three decks summarises
what was covered.

1. **Three commands** that run on the audience's laptop, with the cost stated: `No API key needed:
   the offline stub is deterministic, spends nothing`.
2. **Two exercises, both designed to fail.** `Loosen one failing row's threshold until it goes green,
   then re-run the mutation gate and watch B — DISCRIMINATING go red. The row you just "fixed" can
   no longer fail — R1, catching you.`
3. **A `What I still do not know` panel.** Three to four items, each a real unknown with a number:

```html
<div class="glass-panel p-5 rounded-xl" style="border-left-color:#8fa3b0;">
    <div class="flex items-center gap-3 mb-3">
        <i class="fas fa-circle-question text-xl" style="color:#8fa3b0;"></i>
        <h3 class="text-xl font-bold">What I still do not know</h3>
    </div>
    ...
    <div class="flex gap-3"><i class="fas fa-minus text-xs mt-2 opacity-40"></i><span>Whether a golden set written by <b>one person</b> is a test suite or one person's opinion with a CI badge on it.</span></div>
</div>
```

4. **A concrete ask**, always an artefact the audience owns, never "get in touch":
   - S1: `Bring me the artefact you gave up on reading.`
   - S2: `Bring one real route from a product you actually ship.`
   - S3: `Bring one AI feature from a product you actually ship, and twenty rows you wrote yourself. Not generated — written.`

Plus **the open question** in a warn panel — a genuinely unsolved problem, posed as a question, with
the author's ignorance stated:

> `What is the equivalent-mutant problem in text? In pixels, 0 px moved is a decision. In text there
> is no such measurement, and I do not know of anyone who has one.`

Footer: the paper ids, mono, `opacity-40`, and `Questions · <name> | <role>`.

Both PRESENTING.md files give the same delivery instruction: read the unknowns panel out loud in
full — *"It's the most credible thing on the slide"* — then *"stop talking. Don't fill the silence."*

---

## 11. Tone

| Rule | Check |
|---|---|
| Short declarative sentences | Most body sentences under 20 words. `Stability is not evidence.` |
| Exact, unrounded numbers | `8,412,996 tokens`, `50,459,441 chars`, `1,974 tokens`, `+20 points at p=0.044`. Never "about 8 million" |
| A rounded number is rounded on purpose and says so | `~114 rows rerun (exact McNemar, assuming 14% discordance — honest range 78–249)` |
| No marketing language | Nothing is "powerful", "seamless", "revolutionary", "game-changing". The word "just" appears only in scare quotes: `"Just send it a screenshot" is not a shortcut` |
| Competitors are named and credited | `promptfoo · Braintrust · LangSmith · DeepEval · Ragas · OpenAI Evals — All six ship the runner, the dashboard and the diff — and they ship them better than we will tonight. … If one of them ships a mutation gate by the time you watch this, use theirs.` |
| No hedging in body copy | No "might", "could arguably", "in some cases" in a claim. Claims are stated flat and then punctured with a number |
| Hedging is quarantined | Every "I don't know" lives in the unknowns panel, the counter-evidence callout, or a domain label. Nowhere else |
| Second person for the audience's world, first person for mistakes | `your client's app`, `my own golden set was contaminated` |
| Imperatives for what to do | `Quote this one to a sceptic.` `Pick deliberately.` `Say this out loud.` |

Numbers that flatter are punctured in the same panel as the number:

```
6,390×   corpus ÷ root peak. The whole point of the build, in one ratio.
23.2×    the floor: DOM only, styles already thrown away. Quote this one to a sceptic.
```

---

## 12. Audience calibration

The rule, from both PRESENTING.md files: **explain the thing they do not know, never the thing they
do.**

> Who is in the room: testers and automation engineers. They know pytest, CI, flaky tests, fixtures
> and code review. They do **not** know how LLMs work inside. So explain the AI; never explain
> testing.

Consequence: every AI concept is delivered as a thing the room already owns. `benchmark
contamination → asserting on your own fixture`. `held-out mutant → you don't show a developer the
mutation set before they write their unit tests`. `external verifier → it's called assert`.

### Jargon translation

The deck keeps the precise term on the slide; the spoken form is the translation. The rule of thumb,
verbatim from PRESENTING.md:

> **if a word needs a definition, give the definition *before* the word, in the same breath.** "The
> honest error bar on a pass rate — the Wilson interval — is twenty-seven points wide."

Ship a `Say it this way, not that way` table with the deck. Real rows:

| Don't say | Say |
|---|---|
| context window | how much text the model can read at once |
| tokens | roughly, pieces of words — the unit you get billed for |
| offloading | we keep the data in a file and let code search it |
| the CSSOM / computed styles | every style value the browser calculated for every element |
| mutation testing | we break the feature on purpose and check a row notices |
| held-out mutant | one way of breaking it that the generator is never told about |
| LLM-as-a-judge | letting a model mark another model's homework |
| non-determinism | it gives a different answer to the same question |
| threshold | how close is close enough, written down in advance |
| Wilson score interval | the honest error bar on a pass rate |
| Cohen's kappa | agreement after you subtract the agreement you'd get by luck |
| contamination | grading the model against its own homework |
| provenance | where the expected answer came from, and who decided it |

---

## 13. Where the decks contradict each other

| Point | S1 | S2 | S3 | Winner |
|---|---|---|---|---|
| Honest slide vs trigger table | merged into slide 9 | merged: slide 13 is titled `The Honest Slide` *and* is the trigger table | split: 9 = statistical honesty, 13 = `Scope, With Triggers` | **S3** — the split |
| Closer strip | bold lead-in, present on most slides | aphorism, most slides | aphorism, every slide 2–13 | **S3** |
| Slide bodies | inline in the generator | inline in the generator | separate `slides/slideNN.body.html` fragments | **S3** |
| Print/PDF CSS | 0 of 10 slides | 14 of 14 | 14 of 14, byte-identical block to S2's | **S2 = S3** |
| Planted payoff target | n/a | S2 slide 3 says `until slide 11` — **stale, the review is slide 12** | slide 4 says `until slide 12` — correct | **S3** |
| Eyebrow colour | varies per slide | varies per slide | coral `#ff5640` throughout, gold only on the trigger table | **S3** |
| Companion docs | `SPEAKER_NOTES.md` only | `SPEAKER_NOTES.md` + `PRESENTING.md` + `SLIDE_GUIDE.md` (written against a 13-slide cut; its numbers are off by one from the shipped 14) | `SPEAKER_NOTES.md` + `PRESENTING.md` | **S3** |

If a deck plants a forward reference by slide number, the generator must be able to renumber it. A
stale `until slide 11` is the one factual error in the shipped corpus.

---

## 14. DO NOT

These are the specific ways a generated deck betrays itself.

1. **Round numbers.** `~8 million tokens`, `about 100x`, `roughly half`. The real decks print
   `8,412,996`, `104×`, `1,198 of 1,284`. A round number reads as an estimate, and an estimate reads
   as a guess.
2. **An unsourced claim.** A number with no run, file, app or paper id attached in the same
   sentence. If you cannot name where it came from, delete it.
3. **Two ratios from different things in one breath.** `1.93×` and `104×` are both true and belong to
   different apps. *Mixing them is how a deck stops being true.*
4. **A summary recap slide.** No "what we covered", no "key takeaways", no agenda slide. Three decks,
   38 slides, zero recaps. The close is an ask, not a summary.
5. **Hedging everywhere.** "may", "could potentially", "in many cases", "it seems". Hedges go in the
   unknowns panel and nowhere else. A body sentence is flat, then punctured.
6. **Decorative colour.** Gold = the rule or the trigger. Red/coral = the counter-evidence, the
   failure, the thing that cannot be reached. Green = a passed gate. Grey-blue = a caveat. A colour
   used because it looked nice is off-style.
7. **A closer that restates the title.** If the slide is headlined `Four Gates, No Opinions`, the
   closer is not "so the four gates matter". It is `There is no reviewer agent in this harness, by
   design — every bit above is computed by code that cannot call a model (2402.08115).`
8. **A clean claim with no puncture.** A slide that only argues for its thesis is unfinished.
9. **A trigger column full of principles.** `if it becomes important`, `when the team is ready` — not
   triggers. A trigger is falsifiable by someone who does not like you.
10. **Competitors dismissed.** Name them, say what they do better, then state the narrow claim.
11. **An invented magnitude.** If the source is directional, print the direction and say the source
    records no delta.
12. **Explaining the audience's own discipline back to them.** Explain the AI; never explain testing.
13. **A confessional tone on the honest slide.** No apology, no jokes, no "full disclosure". Three
    columns: the rule, the hole with real output, the fix at `file.py:line`.
