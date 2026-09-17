# Torsor prose style — base + voice library

The **writing** half of the torsor design system. Where `../STYLE.md` and `../tokens.css`
specify how the family *looks*, this directory specifies how it *reads*. It makes the
writing style of the manual/guide family **visible and tunable** without risking what
already works.

The old approach fused everything into one `STYLE.md` per project. This splits it along
the seam between **mechanics** (stable) and **voice** (swappable).

## How it composes

A project's effective style guide = **one base** + **one voice**.

```
prose/
  base-manual.md         ← mechanics for a tool manual (write-manual)
  base-paper-guide.md    ← mechanics for a paper reading guide (write-paper-guide)
  base-body-of-work.md   ← mechanics for a body-of-work summary (write-body-of-work-summary)
  base-state-guide.md    ← mechanics for a workshop state guide (write-workshop-state-guide)
  voices/
    01-direct.md         ← the current, proven voice. THE DEFAULT.
    02-wandering.md      ← experimental digressive register.
    03-PLACEHOLDER.md    ← a stub to copy when a third voice appears.
```

- **Base** = the rules that keep the LaTeX building and the family coherent: `\code{}` vs
  `lstlisting`, callout semantics, citation conventions, banned filler words, structure.
  You rarely touch these, and a voice experiment *cannot* reach them.
- **Voice** = register: rhythm, warmth, humor, how much it wanders vs. leads with the
  point. This is the knob. Editing a voice file changes how it *sounds*, never whether it
  *builds*.

To write in a given voice, a skill reads `base-<format>.md` + `voices/<chosen>.md`
together. The default is always `01-direct` unless a project asks for another.

## Why the split protects what works

`voices/01-direct.md` is the current voice extracted as-is. Selecting it reproduces
today's output. Trying `02-wandering` only swaps the voice file — the base, and therefore
the build and the house conventions, are untouched. That is the whole point: experiment
with register without disturbing a process that's going well.

## Spec vs. implementations

This is the **spec**. The actualized manuals are *implementations* to point at, not the
source of truth:

- **thing manual** — the proven realization of `01-direct` over a full book.
- **shelf manual** — the canonical worked example for preamble and layout.

A skill reads the spec here for the voice, and reads an implementation (e.g. the shelf
manual's `main.tex`) for layout. Spec defines; examples demonstrate.

## This copy is canonical

This directory used to be a snapshot, overwritten from a separate style library whenever
the bundled assets were refreshed. That is retired: **this copy is the source of truth**.
It carries base files the upstream library never had, and it describes register by
technique rather than by named influence. Edit it here.

## Where the rules came from

The voices were tuned in conversation toward four register targets. What survived into the
style files is the distillation — the techniques themselves — and the distillation is the
part that matters: `01-direct`'s rules and exemplars fully specify the voice, and selecting
it reproduces the writing already in hand. The targets are recorded here as *knobs*, so the
design stays editable:

- **Direct address** — second person, conversational fragments for rhythm, "let's be honest
  with each other" framing, clarity. → feeds `01-direct`.
- **Restrained humor** — dry, warm without performance; clear, easy-to-digest statements.
  → feeds `01-direct` and `02-wandering`.
- **Contrapuntal wandering** — layered, rambling moods; several lines of thought braided at
  once. Deliberately optimized *out* of the current rules ("lead with the point," "one idea
  per paragraph"). → the seed of `02-wandering`.
- **Digressive expansiveness** — the chapter that detours and earns it. A candidate
  ingredient for a wandering voice; not yet developed.

Voice files describe register in terms of **technique, not attribution** — no named authors.
Keep it that way when adding a voice.

## Status

- **Phase 1 (done):** this library exists, additively, in its canonical home.
- **Phase 2 (done):** both `write-manual` and `write-paper-guide` now read their style from
  here — `base-<format>.md` + the chosen `voices/<voice>.md`, default `01-direct` — and
  assemble it into each project's `latex/STYLE.md` with a header recording the voice. The
  skill-local `STYLE-paper-guide.md` has been retired (its content is fully carried by
  `base-paper-guide.md` + `01-direct.md`). The `envtools` manual keeps its own
  `latex/STYLE.md` — that's that manual's frozen copy, not a shared source.

A content audit confirmed `base-<format>.md` + `01-direct.md` covers everything the old
monolithic style guides contained (the one gap, the manuals' "inclusive / low-assumption"
audience rule, was added to `base-manual.md`). One intentional behavior change: new manuals
no longer inherit the *thing*-specific framing/glossary that the old shared `STYLE.md`
carried — project-specific framing now belongs in the individual manual.
