# html-deck

A Claude Code skill for building conference-quality presentations as **standalone HTML slides** — one
file per slide, no framework, no build step, no slide library.

Extracted from three decks that were actually presented, not designed in the abstract.

![style](https://img.shields.io/badge/canvas-1920%C3%971080-192b37) ![deps](https://img.shields.io/badge/build_step-none-2ecc71) ![verify](https://img.shields.io/badge/verified-headless_render-ff5640)

---

## What it produces

```
my-talk/
  deck/
    index.html            3-line meta-refresh to slide1.html
    slide1.html … slide14.html    each a complete standalone document
  slides/
    slide01.body.html … slide14.body.html   plain HTML fragments you edit
  generate_deck.py        concatenates head + notes + body + nav
  SPEAKER_NOTES.md        emitted by the generator
  PRESENTING.md           the delivery script
  my-talk.pdf             stage fallback for when the wifi dies
```

Every slide opens on its own in a browser. Arrow keys, space or PageUp/PageDown to navigate. Nothing to
install, nothing to serve, nothing to deploy — though it deploys to any static host as plain files.

## The house style

Dark, dense, evidence-first. It looks like a senior engineer's conference talk rather than a corporate
template.

| Token | Value | Means |
|---|---|---|
| background | `#192b37` | flat dark navy-slate, never a gradient |
| accent | `#ff5640` | the strong / new / action side |
| roi | `#FFD700` | the trap, the caveat, the payoff |
| success | `#2ecc71` | pass, kept, shipped |
| warn | `#e74c3c` | failure, the honest limitation |
| neutral | `#8fa3b0` | old, neutral, non-significant — inline only |

Typography is IBM Plex Sans for prose and Fira Code for anything numeric. Cards are frosted glass panels
with a 4px semantic left border. Charts are hand-built from divs with hand-computed percentages — no chart
library, ever.

## What makes it more than a theme

The skill encodes the **rhetorical** rules, not just the visual ones:

- Every number carries its provenance in the same breath
- Every slide ends in one bold, quotable closer sentence
- Every clean claim is immediately punctured by its own counter-evidence
- A dedicated **honest slide** near the end that makes the author look worst, with real numbers
- A trigger table of what was deliberately *not* built — each with a falsifiable condition that would
  change the decision, never a principle
- A planted sentence early in the deck that is explicitly cashed in later
- No summary recap slide. Close on a concrete ask and an open question.

A deck that is a feature tour has failed even if every slide is pixel-perfect.

## Verification is part of the build

```bash
node skills/html-deck/assets/verify.mjs deck 14
```

Renders every slide headless at exactly 1920×1080 and fails if any element crosses the canvas edge. Then
you look at the screenshots — the geometry check does not catch a rubber stamp sitting on a paragraph or a
bar chart that disagrees with its own caption.

Estimating the vertical budget instead of rendering was wrong about half the time on the source decks.

## Install

```bash
git clone https://github.com/margelatufml/html-deck.git
cp -r html-deck/skills/html-deck ~/.claude/skills/
```

Then ask Claude Code for a deck: *"build me a 14-slide talk on X"*.

## Layout

```
skills/html-deck/
  SKILL.md                      entry point: the build order and the non-negotiables
  references/
    design-system.md            tokens, type scale, colour semantics, print CSS
    components.md               real markup for every reusable piece
    layout-archetypes.md        the slide layout catalogue
    narrative-grammar.md        the rules that make a deck argue
    build-and-verify.md         generator, render check, PDF, deploy
  assets/
    boilerplate.html            the verbatim shared <head>
    generate_deck.py            the generator
    verify.mjs                  headless 1920×1080 overflow check
    export_pdf.mjs              per-slide PDF renderer
examples/
    farmers-on-romania/         a deck built by the skill, end to end
```

## Requirements

- Python 3.9+ (generator — standard library only)
- Node with `playwright` resolvable (verification and PDF export only)
- `pdfunite` or `pypdf` to merge the PDF
- Network at present time: Tailwind, Font Awesome and Google Fonts load from CDNs. This is why the PDF
  export exists.

## Licence

MIT.
