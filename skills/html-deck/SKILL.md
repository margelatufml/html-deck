---
name: html-deck
description: Build a conference-quality presentation as standalone HTML slides - one file per slide, no framework, no build step - in a dark, evidence-first house style with a Python generator, a 1920x1080 render check and PDF export. Use when the user asks for a slide deck, a presentation, a talk, a session, "slides", a deck for a meetup or conference, or wants an existing deck extended, restyled or exported. Also use when a deck must be self-hosted as plain files rather than made in PowerPoint, Google Slides or an artifact.
---

# html-deck

A deck is 14-ish standalone HTML files. No bundler, no framework, no slide library. Every slide is a
complete document that opens on its own. The style is dark, dense and evidence-first: it looks like a
senior engineer's conference talk, not a corporate template.

This skill is extracted from three decks that were actually presented. The references are descriptions
of those files, not aspirations. When in doubt, go and read the decks the references cite.

## The non-negotiables

1. **Every number carries its provenance in the same breath.** The run, the file, the source, the date.
   A number with no origin is the fastest way to lose a technical room.
2. **Every slide ends in a closer strip** — one full-width bar with one bold, quotable sentence that
   states the slide's "so what".
3. **Every interior slide opens with the three-beat header** — mono uppercase eyebrow, `text-5xl` H2,
   `opacity-70` subtitle.
4. **Colour is semantic, never decorative.** Coral = the strong/new side. Gold = the trap or the payoff.
   Green = pass. Red = the honest limitation. Slate = neutral/old.
5. **Nothing overflows.** The canvas is exactly 1920×1080 and there is no scrolling. This is verified by
   rendering, not by estimating.
6. **The deck argues, it does not list.** See `references/narrative-grammar.md`. A deck that is a feature
   tour has failed even if every slide is pixel-perfect.

## Build order

Work in this order. Steps 2 and 3 are where the quality is; do not rush them to get to the HTML.

### 1. Fix the shape before writing anything

Decide the total slide count **first** — it is hardcoded in three places per slide and renumbering later is
manual churn. 14 slides ≈ 40 minutes. 10 ≈ 35.

The shape that works:

| Slides | Section |
|---|---|
| 1 | Title |
| 2 | Recap / where we are |
| 3–6 | Theory — ending on a hinge slide that undercuts the easy answer |
| 7–9 | The build, and the honest measurement |
| 10–12 | Evidence, and the slide where the author is wrong |
| 13–14 | What was deliberately not built, and the close |

### 2. Gather the evidence before designing a slide

If the deck makes claims, the claims need sources, and the sources need checking. Produce an evidence
sheet first: the spine claims, the exact numbers cleared for a slide, and — most important — a
**DO-NOT-CLAIM list** of things that are tempting, wrong, and would be caught by someone in the room.

Recompute any arithmetic yourself rather than quoting it. If a figure cannot be sourced, it does not go
on a slide; it goes in the "what I still do not know" panel.

### 3. Write per-slide briefs

One brief per slide, before any HTML: eyebrow, headline, subtitle, the archetype from
`references/layout-archetypes.md`, the content blocks with their exact copy and numbers, and the closer
sentence. The brief is the spec. Writing HTML without one produces a pretty feature tour.

### 4. Write the slide bodies

One plain HTML fragment per slide at `slides/slideNN.body.html` (zero-padded). A fragment is **only** the
outer wrapper div and its content — no `<head>`, no `<style>`, no `<script>`, no nav cluster. The
generator adds all of that.

Read `references/components.md` for the markup and `references/design-system.md` for the tokens.

Fragments are independent, so they can be written in parallel — but give each writer the design system,
its own brief, and a real slide from a reference deck to match.

### 5. Generate

Copy `assets/generate_deck.py`, set the CONFIG block, fill `SLIDE_TITLES` and `SPEAKER_NOTES`, run it. It
emits `deck/slide1.html … slideN.html`, `deck/index.html` and `SPEAKER_NOTES.md`.

### 6. Verify by rendering — mandatory

```bash
node assets/verify.mjs <deck-dir> <slide-count>
```

It renders every slide headless at exactly 1920×1080, reports any element crossing the canvas edge, and
writes screenshots. **Then actually look at the screenshots.** The overflow check catches geometry; it
does not catch a rubber stamp sitting on top of a paragraph, an unreadable contrast pair, or a chart whose
bars do not match its numbers.

Re-run after every edit. An edit that adds two lines of copy can push a card off the slide.

### 7. Export the PDF

```bash
node assets/export_pdf.mjs <deck-dir> <slide-count> && pdfunite /tmp/deckpdf_*.pdf out.pdf
```

The deck loads Tailwind, Font Awesome and Google Fonts from CDNs, so it needs the network at present time.
The PDF is the stage fallback for when the venue wifi fails. It is not optional for a talk that matters.

### 8. Serve or deploy

```bash
cd deck && python3 -m http.server 8080
```

For a public URL, `references/build-and-verify.md` documents an Azure Storage static-website pattern. Any
static host works — the deck is plain files.

## Companion documents

A deck that will be presented wants three more files. They are cheap and they are what makes it
deliverable rather than just built:

- **`SPEAKER_NOTES.md`** — emitted by the generator; also embedded in each slide as an HTML comment.
- **`PRESENTING.md`** — the delivery script: who is in the room, a "say it this way, not that way"
  jargon-translation table, per-slide *what it is / what to say / what to do*, the questions you will get,
  a pre-flight checklist, and what to do when the demo breaks.
- **`SLIDE_GUIDE.md`** — one paragraph per slide explaining what it means, for someone reading the deck
  without the speaker.

## References

Load these as you need them, not up front.

| File | Read it when |
|---|---|
| `references/design-system.md` | Before writing any slide. Tokens, type scale, colour semantics, print CSS. |
| `references/components.md` | While writing slide bodies. Real markup for every reusable piece. |
| `references/layout-archetypes.md` | When choosing how a slide should be composed. |
| `references/narrative-grammar.md` | Before writing slide *copy*. The rules that make a deck argue. |
| `references/build-and-verify.md` | At generate/verify/export/deploy time. |
| `assets/boilerplate.html` | The verbatim shared `<head>`. Copy it, do not retype it. |

## The traps that actually bit

Learned the hard way on the source decks:

- **A rubber stamp overlapping body copy.** Bottom-anchor it and reserve a padding lane in the card.
- **Naming a thing you claimed was secret.** If a slide says "held out, never named", grep the whole deck
  to confirm the name appears nowhere.
- **Numbers drifting out of sync with the thing they measure.** If the deck quotes a repo, re-measure
  right before publishing, not once at the start.
- **Reusing a ratio measured on a different subject.** Cite each number against what it was measured on.
- **An eyebrow colour used against its meaning.** Three colours are legitimate for an eyebrow; pick the
  one that matches the slide's register.
- **Estimating the vertical budget instead of rendering.** Estimates were wrong roughly half the time.
