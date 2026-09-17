# Farmers in Romania

A 14-slide deck built end to end by the `html-deck` skill, as its verification test.

The topic is deliberately unrelated to the decks the skill was extracted from — the point was to find
out whether the skill generalises beyond the technical talks it came from, or had merely memorised them.

## Run it

```bash
python3 generate_deck.py          # emits deck/ and SPEAKER_NOTES.md
cd deck && python3 -m http.server 8080
```

## Verify it

```bash
node ../../skills/html-deck/assets/verify.mjs deck 14
```

14/14 clean at 1920×1080.

## What it argues

Romania has 2.9 million agricultural holdings — 32.6% of every farm in the EU (Eurostat, 2023) — and that
headline is the least useful true thing you can say about the country. Nine in ten of those farms are
under 5 hectares and work roughly a quarter of the land; 1.0% of them work 53.1% of it.

The hinge is slide 6: three official sources give three different answers to "how many Romanians work in
agriculture" — 20.7% (Eurostat), 11.9% (INS) and 23% (DG AGRI, undated). They are not contradicting each
other; they count different things. But you cannot average them, and you cannot quietly pick one.

Every figure on every slide carries its source and year. The briefs carry a DO-NOT-CLAIM list of figures
that were tempting and had to be left out — stale data, secondary sites, and numbers that could not be
confirmed on a live primary page.

## Honest note

The figures were researched and sourced for this exercise, not fact-checked to publication standard.
Slide 12 exists precisely because four of the numbers have a second official value, and slide 11 is the
case against the deck's own framing.
