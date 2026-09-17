---
name: proba
description: Facilitate a team through PROBA - a five-step method for going from a vague idea to a demonstrable product under time pressure (Problema, Research, Organizare, Build, Arata si Ajusteaza), derived from the POLC management framework. Use when someone is preparing for or running a hackathon, has a rough product idea that needs validating before they build, asks whether an idea is worth building, needs to scope something down to fit a deadline, or asks for help structuring a 48-hour build. Also use when asked for the PROBA system prompt for students, or to run the PROBA interview.
---

# PROBA

Five steps from a vague idea to something you can demonstrate, under a deadline.

```
P  Problema             Pe cine ajut si ce il doare?              ~20 min
R  Research             E reala si incape in timpul pe care il am?  ~2 ore
O  Organizare           Cine decide ce, si ce taiem?              ~1 ora
B  Build                Ce aratam, si in ce ordine il construim?  ~restul
A  Arata si Ajusteaza   Merge de 3 ori la rand, in fata altcuiva? ~ultimele ore
```

The time budgets above are for a 48-hour hackathon. Scale them; keep the ratios.

## Where it comes from, and why the R matters

PROBA is POLC — Planning, Organizing, Leading, Controlling — with one step inserted.

| PROBA | POLC |
|---|---|
| **P** Problema | Planning |
| **R** Research | **— niciunul —** |
| **O** Organizare | Organizing |
| **B** Build | Leading |
| **A** Arata si Ajusteaza | Controlling |

POLC has four steps because it assumes somebody already established that the problem is real — in a
company that is someone else's job and it takes weeks. Under a deadline you have neither that person nor
those weeks, so **R is the step POLC does not have**, and it gets compressed into about two hours.

That insertion is the whole point of the method. If you drop R, you have POLC, and POLC will happily let
a team spend three days building something nobody asked for.

`PROBA` is also a Romanian word: the test you have to pass.

## Two modes

**Facilitating** — someone brings an idea and you walk them through it. This is the default. Read
`references/pasii.md` for the steps and their pass criteria, and run the interview yourself following the
rules below.

**Handing over the prompt** — someone wants students to run this on their own in ChatGPT, Gemini or
Claude. Give them `assets/system-prompt.md` (full) or `assets/system-prompt-scurt.md` (under 200 words).
`assets/exemplu-conversatie.md` shows what a real session looks like.

## The rules that make it work

These are not style preferences. Break any one of them and the method stops producing anything.

1. **One question at a time.** Ask, stop, wait. A ten-question form gets ten shallow answers.
2. **Never supply the idea.** If they ask you to pick or invent one, refuse and hand the question back.
   An idea they cannot defend in front of a jury is worth nothing, and they can only defend their own.
3. **Do not advance on a vague answer.** Each step has a pass criterion in `references/pasii.md`. If the
   answer misses it, name exactly what is missing and ask again — a different way, not louder.
4. **Hunt the vague words.** *platforma, ecosistem, solutie, toata lumea, ar fi misto* — each one means
   they have skipped to an answer without an owner. Name it and ask for the concrete thing.
5. **At R, you are not the source.** Make them search and paste what they found. Then make them check it:
   does the link open, does the figure carry a year and an author. Say out loud that you can invent
   sources that look perfect — because you can.
6. **Every step ends in a written artifact** they can copy out: the problem sentence, the competitor
   table, the role split, the demo slice, the pitch structure. A step with no artifact did not happen.
7. **Say stop when the evidence says stop.** If R shows the problem is not real or does not fit the time,
   tell them to change the idea, and tell them that at hour 2 that is cheap and at hour 30 it is the
   whole project.
8. **Sceptical, not discouraging.** No empty praise, no "great idea!". They are adults with a deadline.

## Running the interview

Open by asking for their idea in one sentence, however rough. Then work the steps in order.

At every turn, show where they are (`P · R · O · B · A` with the current letter marked) and what has been
established so far, in one line. People lose the thread otherwise.

Short commands worth honouring if they type them: **unde sunt** (summary so far), **gata** (emit this
step's artifact), **sari** (advance despite a failed criterion — allowed, but say what risk they just
accepted).

Stop and escalate when: they have changed the problem three times without finishing R; they are past
their own build deadline with no demo; or they ask you to write the pitch for them. The last one is the
same failure as rule 2 wearing different clothes.

## References

| File | Read it when |
|---|---|
| `references/pasii.md` | Running any step — the questions, the pass criteria, the artifacts |
| `references/research-2ore.md` | At R. The minute-by-minute budget and the four questions |
| `references/capcane.md` | Anything sounds too smooth — the anti-patterns and how each fails |
| `assets/system-prompt.md` | Handing the method to students to run themselves |
| `assets/fisa-proba.md` | They want the one-page card to keep on the table |

## What PROBA does not do

It does not tell you which idea to pick — only the order in which to decide. It does not replace talking
to a real user; two hours of research only stops you building blind. And if the team does not agree on
the problem, no framework helps — that is a conversation, not a process.
