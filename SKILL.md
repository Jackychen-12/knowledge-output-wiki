---
name: knowledge-output-wiki
description: Build a dual-layer personal wiki that extends Karpathy's LLM Wiki pattern with an explicit output layer. The knowledge layer compounds long-term (concept articles compiled from raw sources, Karpathy-style); the output layer packages scenario-specific deliverables (talks, interviews, reports, PRDs, posts) by drawing from the knowledge layer. Use this when the user is starting or restructuring a personal knowledge base, has accumulated raw notes that need compiling, or needs the same knowledge to serve multiple audiences (resume vs research talk vs blog post).
metadata:
  source-inspiration: Karpathy's LLM Wiki (2026-04-03)
  extension: explicit output layer
---

# knowledge-output-wiki

> A dual-layer personal wiki pattern: compound knowledge long-term, package outputs short-term.
>
> Extends [Karpathy's LLM Wiki](references/karpathy-pattern.md) (2026-04-03) by separating *what I know* from *how I present it for X audience*.

---

## When to use this skill

Use this skill when the user is doing any of the following:

- Starting a personal knowledge base from scratch and asks for "structure"
- Has accumulated raw notes / clippings / files and asks to "organize" or "compile" them
- Already has a wiki/Obsidian/Notion vault but the *same* knowledge needs to serve multiple deliverables (talk, blog post, resume, client deck)
- Says they want to "build a second brain", "personal wiki", "LLM-maintained knowledge base", or references Karpathy's LLM Wiki post
- Is preparing for a recurring high-stakes scenario (job interviews, conference talks, board updates, sales cycles) that draws on a shared knowledge base

**Do not use this skill** for: project documentation (README, ADRs), team wikis (Confluence, Notion teams), or short-lived task notes. This pattern is for *personal* knowledge that compounds over years.

---

## Core idea in 60 seconds

```
raw/              KNOWLEDGE LAYER              OUTPUT LAYER
(staging)         (long-term compound)         (short-term packaging)
────────          ─────────────────────        ──────────────────────
clippings    →    concept pages          →    talks
papers       →    methodology pages      →    interviews
transcripts  →    case notes             →    PRDs / proposals
chats        →    reading notes          →    blog posts
project       │    index pages            │    resume bullets
files         │                           │    client decks
              │                           │
   LLM compiles ──┘   LLM packages ───────┘
   (Karpathy)          (this skill's extension)
```

- **Knowledge layer = Karpathy's wiki.** Topic-organized concept articles compiled from raw sources. Grows with backlinks. Optimized for *recall and reuse*.
- **Output layer = goal-organized deliverables.** Each output draws from knowledge pages, formatted for a specific audience and scenario. Optimized for *being shipped*. Often disposable after the event.
- **Both layers are flat markdown.** Portable across LLMs, editors, and decades.

The two-layer split is the whole point: without it, every interview prep degrades your knowledge base; without it, every "let me update my notes" feels like procrastination because there's no clear output.

---

## File structure

```
my-wiki/
├── raw/                     ← unprocessed sources (gitignored or low-touch)
│   ├── readings/
│   ├── conversations/
│   └── projects/
│
├── wiki/
│   ├── index.md             ← global hub (link to both layers)
│   ├── log.md               ← change log (LLM-maintained)
│   │
│   ├── knowledge/           ← THE COMPOUND LAYER
│   │   ├── index.md
│   │   ├── <topic-1>/
│   │   │   ├── methodology.md
│   │   │   └── cases.md
│   │   └── <topic-2>/
│   │       └── ...
│   │
│   ├── <output-channel-1>/  ← e.g. portfolio/, interview/, talks/, blog/
│   │   ├── index.md
│   │   └── <deliverable>.md
│   │
│   └── <output-channel-2>/  ← e.g. industry/, branding/, clients/
│       └── ...
│
└── scripts/
    └── compile_wiki.py      ← optional: link graph + HTML viewer
```

The exact channel names depend on the user's goal — see [examples/](examples/) for `researcher/`, `creator/`, `jobseeker/` instantiations.

---

## Page types (the taxonomy)

There are exactly **6 page types**, split across the two layers. Use the right one or the system rots.

### Knowledge-layer page types

| # | Type | Filename pattern | Purpose | When to create |
|---|---|---|---|---|
| 1 | **Index** | `<topic>/index.md` | Hub: links + 1-line summaries of every page in topic | First page in any new topic |
| 2 | **Methodology** | `<topic>/methodology.md` | Frameworks, principles, evaluation rubrics — *how to think about* this topic | After you've read enough to extract a pattern |
| 3 | **Case / Notes** | `<topic>/cases.md` or `<topic>/<case-name>.md` | Concrete examples, project deep-dives, decision records | Each time a new instance is worth remembering |
| 4 | **Reading** | `readings/<source-slug>.md` | Distilled takeaways from one source + provenance | Per book/paper/long-form article worth retaining |

### Output-layer page types

| # | Type | Filename pattern | Purpose | When to create |
|---|---|---|---|---|
| 5 | **Deliverable** | `<channel>/<deliverable>.md` | One scenario-packaged artifact (interview answer, talk outline, blog draft, PRD section) | Per concrete upcoming event/submission |
| 6 | **Channel index** | `<channel>/index.md` | What's in this channel + how to pick which deliverable for which audience | First page in any new output channel |

Anything that doesn't fit one of these 6 types either belongs in `raw/` (not yet processed) or doesn't belong in the system at all.

---

## The compilation flow (Karpathy's loop, extended)

Karpathy's original 4-phase loop: **Ingest → Compile → Query & Enhance → Lint**.

This skill adds a 5th phase: **Package**.

```
1. INGEST       raw source lands in raw/<bucket>/<file>
                   │
                   ▼
2. COMPILE      LLM reads raw + existing knowledge → updates concept pages,
                index, backlinks. Never reprocess from scratch — incremental only.
                   │
                   ▼
3. QUERY        you ask a question; answer is filed back into knowledge/
                   │
                   ▼
4. LINT         LLM scans for stale facts, duplicates, broken links, gaps
                worth researching. Surfaces "missing concept pages" candidates.
                   │
                   ├──────────────────────────────┐
                   ▼                              ▼
5. PACKAGE      (when a real audience is on the calendar)
                LLM selects knowledge pages → drafts output-layer deliverable
                in the channel's format (STAR for interviews, talk outline for
                conferences, bullet points for resume, etc.). Output pages link
                BACK to source knowledge pages — never duplicate, always reference.
```

**The discipline that makes it work:** new material never goes directly to the output layer. Always land in `raw/` first, get compiled into `knowledge/`, *then* package into outputs. Skipping the knowledge step is how output-layer wikis decay into stale resume drafts.

---

## Cross-references (the link graph)

Two link styles, used consistently:

```markdown
[[topic-name]]              ← wiki-style link to another knowledge page
[label](relative/path.md)   ← standard markdown link (works in any viewer)
```

- **Within knowledge layer:** dense backlinks. Every concept page links to related concepts. The LLM auto-maintains the graph during the COMPILE phase.
- **Output → knowledge:** every output deliverable links back to the knowledge pages it draws from. This is how you avoid duplication and keep outputs cheap to update.
- **Knowledge → output:** generally *don't* link this direction. Knowledge pages outlast any specific output; pinning them to today's interview rots them.
- **Anywhere → raw/:** optional, useful for provenance. `> Source: [[raw/readings/<file>]]` is a fine convention.

Broken `[[link]]` to a non-existent page is a *feature* — it marks "concept I should write about." Lint pass should surface these as TODOs, not errors.

---

## How to instantiate this for a user

When invoked, follow this sequence:

1. **Diagnose**: Ask the user (a) their primary goal that drives outputs (research / job / consulting / writing / teaching), (b) what raw material already exists, (c) one concrete upcoming output event in the next 30 days.

2. **Name the channels**: Output channels MUST be named after the user's actual scenarios, not generic labels. For a researcher: `papers/`, `talks/`, `proposals/`. For a job seeker: `portfolio/`, `interview/`, `branding/`. See [examples/](examples/) for prior instantiations.

3. **Seed knowledge topics from raw/**: Skim `raw/`. Propose 3–7 topic folders that would absorb >70% of the existing material. Don't over-engineer — new topics can be added later. Bias toward fewer, broader topics at the start.

4. **Build one end-to-end slice**: Compile *one* raw source into *one* knowledge page, then package it into *one* output deliverable. This is the demo that makes the user trust the system.

5. **Write the index + log**: `index.md` for navigation, `log.md` for what just happened. Both are LLM-maintained from here on.

6. **Stop**. Resist building the whole vault upfront. The pattern compounds only if the user takes over after the first slice.

---

## Anti-patterns (do not do these)

| Anti-pattern | Why it fails |
|---|---|
| Skipping `raw/` and writing knowledge pages from memory | Knowledge pages lose provenance; future-you can't verify or update them |
| Letting output deliverables grow without linking back to knowledge | The same fact gets restated in 5 deliverables; updating one means hunting all 5 |
| One output channel for "everything" | Channels exist to encode *format conventions* (STAR vs talk outline vs bullet). One channel = no format discipline |
| Nesting folders >2 levels deep | Karpathy's portability principle: flat-ish markdown moves cleanly between tools and decades. Deep trees don't |
| Treating `knowledge/` like a Notion database with rich metadata | The whole point is portability. Plain markdown only; metadata in frontmatter only when necessary |
| Reprocessing the whole wiki on every new source | Incremental compile only. The LLM updates *affected* pages, not all pages |
| Building all 5 output channels up front "in case" | Channels are real audiences. No upcoming audience = no channel |
| Splitting concept pages by source (one page per book/paper) | Concepts are organized by *topic*, not by *where you read about them*. Readings page summarizes the source; concept pages cite multiple sources |

---

## What the LLM does vs what the human does

| Phase | LLM | Human |
|---|---|---|
| Ingest | – | Drops raw sources into `raw/` |
| Compile | Writes/updates concept pages, indexes, backlinks | Skims and accepts/rejects edits |
| Query | Answers, files Q&A back into knowledge | Asks |
| Lint | Surfaces gaps, contradictions, stale facts | Decides what to research next |
| Package | Drafts deliverables from knowledge pages | Edits voice, ships |

The human's job shrinks to *curating sources* and *deciding what matters*. The LLM does the writing, linking, and bookkeeping. This is Karpathy's core insight — preserve it.

---

## Loading order

When this skill is invoked, load in this order (don't load everything up front):

1. This `SKILL.md` (always)
2. `references/architecture.md` — when the user wants the deep model
3. `references/page-types.md` — when classifying a specific page
4. `references/compilation-flow.md` — when actually compiling raw → knowledge
5. `references/cross-references.md` — when fixing or building the link graph
6. `references/karpathy-pattern.md` — when the user asks about Karpathy or how this extends his pattern
7. `templates/` — when seeding a new page
8. `examples/` — when picking channel names for a new vault
9. `scripts/compile_wiki.py` — when the user wants a viewer or link-graph export

---

## License & attribution

MIT. Inspired by Andrej Karpathy's LLM Wiki concept (2026-04-03). The dual-layer extension and packaging phase are this skill's contribution.
