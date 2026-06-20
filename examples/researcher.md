# Example instantiation — researcher

> A PhD student or independent researcher whose recurring outputs are papers, talks, and grant proposals.

---

## Folder structure

```
my-wiki/
├── raw/
│   ├── readings/             ← papers, books, talk transcripts
│   ├── conversations/        ← advisor meeting notes, collaborator threads
│   ├── experiments/          ← raw lab/code outputs worth keeping
│   └── clippings/            ← short article saves
│
├── wiki/
│   ├── index.md
│   ├── log.md
│   │
│   ├── knowledge/
│   │   ├── index.md
│   │   ├── methods/                ← experimental / analytical methods
│   │   │   ├── index.md
│   │   │   ├── methodology.md
│   │   │   └── cases.md
│   │   ├── prior-work/             ← what's been published in your area
│   │   │   ├── index.md
│   │   │   └── <line-of-work>.md
│   │   ├── open-questions/         ← things nobody has answered yet
│   │   │   └── index.md
│   │   └── readings/
│   │       ├── index.md
│   │       └── <paper-slug>.md     (one per paper that mattered)
│   │
│   ├── papers/                     ← OUTPUT: paper drafts
│   │   ├── index.md
│   │   └── <paper-slug>.md
│   │
│   ├── talks/                      ← OUTPUT: conference / lab talks
│   │   ├── index.md
│   │   └── <event-slug>.md
│   │
│   └── proposals/                  ← OUTPUT: grants, fellowships
│       ├── index.md
│       └── <proposal-slug>.md
```

---

## Format conventions per channel

| Channel | Format | Sections |
|---|---|---|
| `papers/` | journal/conference template | abstract → intro → methods → results → discussion |
| `talks/` | 3-act | setup (the puzzle) → conflict (the surprise) → resolution (the new question) |
| `proposals/` | funder template | problem → approach → feasibility → impact → timeline |

---

## How the loop runs

- **Ingest:** every paper you actually read goes through `raw/readings/`. If you didn't bother to extract it, you didn't really read it.
- **Compile (weekly):** each new reading gets a `readings/<slug>.md`. Any new framework from it lands in `knowledge/methods/methodology.md`. Any new experimental finding lands in `knowledge/prior-work/<line>.md`. Open questions go to `open-questions/`.
- **Lint (monthly):** find readings that were never cited (extract a framework or archive); find open questions that have been there 6+ months (still open? worth pursuing?).
- **Package (per event):**
  - **Paper:** pull from `methods/`, `prior-work/`, your own `cases.md`. Sources section lists ~15 knowledge pages.
  - **Talk:** pull from 1 methodology + 2–3 cases. Sources section much shorter.
  - **Proposal:** pull from `open-questions/` heavily; this is what `open-questions/` exists for.
- **Post-event compile:** advisor's pushback on a paper draft → new entry in `methods/methodology.md` or new case. Q&A at a talk → new `open-question`. Grant feedback → update `proposals/index.md` with what funders cared about.

---

## What this looks like vs single-layer

Without the output layer: every paper you write, every talk you give, requires reconstructing the framing from your notes. Your notes either stay clean (and you re-derive) or drift toward the most recent paper (and become useless for the next one).

With the output layer: the framing for paper N+1 is a remix of frameworks already stable in `methods/` plus a fresh angle. Talks reuse 3-act structures. Proposals reuse the "approach" section across applications with cosmetic edits. The compounding is real.

---

## Anti-patterns specific to researchers

- **Treating `readings/` as a literature review.** It's not — it's distillation. Literature reviews are *output*; readings are *input*. Don't combine them.
- **Putting paper drafts in `knowledge/`.** Papers are outputs. They cite knowledge. They're not knowledge themselves.
- **One folder per paper you're writing.** No — one folder per *topic of inquiry*. Papers are deliverables that draw from multiple topics. The topic outlives the paper.
