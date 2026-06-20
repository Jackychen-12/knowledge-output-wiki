# Compilation flow — raw → knowledge → output

> The 5-phase loop the LLM runs (extends Karpathy's 4-phase Ingest/Compile/Query/Lint with a Package phase).

---

## Phase 1 — Ingest

**Trigger:** a new raw source exists (file, clipping, transcript, conversation export).

**Action:** human drops file into `raw/<bucket>/`. Bucket names match the source type:

```
raw/
├── readings/        ← books, papers, long-form articles
├── conversations/   ← chat exports, interview transcripts
├── projects/        ← files from work-in-progress projects
├── clippings/       ← short article saves, screenshots
└── notes/           ← rough handwritten/voice notes you transcribed
```

**LLM does:** nothing in this phase. Ingest is the human's job; the LLM should not auto-ingest from a watch folder. The friction of manually deciding "is this worth keeping" is a feature, not a bug.

**Skip if:** the source isn't worth retaining. Most things aren't.

---

## Phase 2 — Compile

**Trigger:** human asks "compile this" or "update the wiki with what's in raw/".

**Action:** LLM reads the new raw sources *plus* the existing knowledge layer, then performs the smallest set of updates:

1. Identify which existing knowledge pages this source touches
2. For each touched page: append/edit, preserving prior structure
3. If the source introduces a concept not yet covered: create a new page (and update the topic index)
4. Update backlinks in both directions
5. Append a one-line entry to `log.md`

**Critical rules:**
- **Incremental only.** Never reprocess pages that the new source doesn't affect.
- **Preserve human edits.** If a page has obvious human-voice edits, treat them as authoritative; don't overwrite.
- **Cite the source.** Every claim added from a raw source must link to the raw file or external URL.
- **No silent deletions.** If removing content, mention it in `log.md`.

**Output:** updated knowledge pages, updated indexes, updated `log.md`.

---

## Phase 3 — Query

**Trigger:** human asks a question of the wiki.

**Action:** LLM answers using the knowledge layer. Before responding:

1. Identify the 1–5 most relevant knowledge pages
2. Read them in full (not chunks — these are short documents)
3. Answer, citing pages
4. **File the Q&A back** into the relevant knowledge page (as a `## FAQ` or `## Q&A` section) or into a new case page if the question revealed a worth-keeping insight

This is Karpathy's "every exploration adds up" — queries are themselves knowledge-layer additions.

**Anti-pattern:** answering from memory without reading the wiki. The wiki is the source of truth; the LLM's training data is not.

---

## Phase 4 — Lint

**Trigger:** weekly cadence, or before a major PACKAGE phase, or after a large COMPILE.

**Action:** LLM scans the whole wiki for health issues:

| Check | Action |
|---|---|
| Broken `[[link]]` to non-existent page | Surface as "candidate page to write" |
| Page hasn't been updated in N months | Ask: still accurate? still relevant? |
| Same fact stated differently in two pages | Propose merge or reconciliation |
| A topic has accumulated >10 pages without sub-organization | Propose splitting into sub-topics |
| Reading page that no other page cites | Ask: extract a framework from it, or archive? |
| Output deliverable older than its event date | Propose archive |
| Output deliverable whose `Sources:` point at deleted/renamed knowledge pages | Fix links |
| Knowledge page without any source citation | Flag — provenance missing |

**Output:** a punch list, surfaced to the human for triage. The LLM does *not* auto-fix high-impact issues (mergers, deletions). It proposes.

---

## Phase 5 — Package (the extension)

**Trigger:** a real upcoming audience/event (interview on date X, talk on date Y, client meeting on date Z).

**Action:** LLM drafts a new deliverable in the appropriate output channel:

1. Identify the channel and its format convention (read channel index)
2. Identify knowledge pages relevant to the topic and audience
3. Draft the deliverable in the channel's required structure
4. Fill `Sources:` with `[[links]]` back to the knowledge pages used
5. List anticipated follow-ups / questions the audience will probably ask
6. **Do not modify the knowledge layer** during this phase

**After the event happens** (the human reports back):
- Append "what was actually asked / what landed / what didn't" to the deliverable
- Trigger a small COMPILE: any new lesson from the event gets added to the relevant knowledge page

This is the loop that makes the system compound: every external event becomes a knowledge-layer update.

---

## A worked example (generic — researcher persona)

```
Day 1 — INGEST
  Human drops conference-paper.pdf in raw/readings/
  Human drops slack-thread-export.md in raw/conversations/

Day 1 — COMPILE
  LLM reads both; touches knowledge/<topic>/methodology.md (adds new framework
  from the paper) and knowledge/<topic>/cases.md (adds discussion from the
  Slack thread). Creates readings/conference-paper.md. Updates 3 backlinks.
  Logs all changes in log.md.

Day 8 — LINT
  LLM finds: 2 broken [[links]] (suggested as new pages), 1 reading page that
  isn't cited anywhere (suggests extracting its framework into methodology),
  1 case page where two paragraphs contradict each other.

Day 14 — PACKAGE
  Human says "drafting talk for <event> on <date>".
  LLM reads talks/index.md (3-act format convention), pulls 4 knowledge pages,
  drafts talks/<event-slug>.md with Sources section linking back. Lists 8
  likely audience questions.

Day 17 — POST-EVENT COMPILE
  Human reports: questions 3 and 7 were asked; surprising pushback on assumption X.
  LLM updates talks/<event-slug>.md with reflection. Adds "Pushback on X" as a
  new case in knowledge/<topic>/cases.md.
```

The knowledge layer is one source richer at the end of the cycle than at the start. The output layer has a shipped deliverable that can be referenced when the *next* talk comes around.

---

## What the LLM should refuse to do

- **Ingest without human selection.** Don't watch a folder and auto-pull. The human's curation decision is load-bearing.
- **Skip raw and write knowledge from memory.** Always cite a source. If the human says "you know this, just write it", insist on a source URL or a raw note.
- **Modify knowledge during PACKAGE.** The contract is one-directional. Violating it is how the layers degrade.
- **Auto-archive without confirmation.** Lint surfaces candidates; the human decides.
- **Reprocess the whole wiki.** Always incremental. If incremental looks impossible, the request is wrong — split it.
