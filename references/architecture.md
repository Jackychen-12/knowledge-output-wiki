# Architecture: the dual-layer model

> Deep dive on *why* there are two layers, what each optimizes for, and the contract between them.

---

## The problem this solves

Single-layer personal wikis (Roam, Obsidian vaults, classic Karpathy wiki) optimize for one thing: **you, recalling and connecting your own ideas**. That's the right optimization when the audience is yourself.

The moment the same knowledge has to serve *external* audiences — interviewers, conference attendees, clients, hiring managers, blog readers — a single-layer wiki starts to rot in one of two ways:

1. **Knowledge pages drift toward the next audience.** "Let me add a STAR framing to this case." Six months later the concept page is half-interview-prep, half-knowledge, useful for neither.
2. **Knowledge pages stay clean, but you re-derive the audience-shaped version every time.** Each interview prep is from-scratch effort; no compounding.

The dual-layer model says: keep the knowledge layer pure (audience-agnostic, durable, dense backlinks) and externalize the audience-shaped versions into a separate output layer that links *back* into knowledge.

---

## What each layer optimizes for

|  | Knowledge layer | Output layer |
|---|---|---|
| **Audience** | Future-you | External party (interviewer, reader, client) |
| **Lifetime** | Years to decades | Days to weeks |
| **Organization** | By topic | By scenario / channel |
| **Format** | Methodology + cases + cross-refs | Whatever the audience expects (STAR / talk outline / deck / bullet list) |
| **Success metric** | "I can find what I learned 2 years ago" | "I shipped a deliverable that landed" |
| **Edit cadence** | Continuous, slow | Burst, scenario-driven |
| **Disposability** | Never | Often (delete after the event) |
| **Linking** | Dense backlinks within layer | Sparse links *into* knowledge layer; rarely out |

The mismatch is what makes a single layer impossible. A page can only serve one audience well.

---

## The contract between layers

The two layers communicate through a narrow, one-directional interface:

```
output deliverable
    ├── draws facts from → knowledge page(s)
    ├── cites → knowledge page(s)
    └── never modifies knowledge pages

knowledge page
    ├── does not know which outputs use it
    ├── stays generic
    └── citing back to raw/ is fine; citing forward to outputs is not
```

Why one-directional? Because the moment knowledge pages link forward to specific outputs, you have a coupling — the knowledge page knows about the interview prep doc, which knows about a specific company on a specific date. When the date passes, the knowledge page is now half-stale and you have to clean it up. That cleanup never happens. The layer corrodes.

The exception: **portfolio-style "case" pages may exist in either layer.** A long-running project deserves a knowledge-layer case page (technical detail, decisions, what worked) *and* a separate output-layer portfolio page (STAR framing for interviews). They are different pages with different audiences.

---

## Why this isn't just "notes vs drafts"

Three differences from a simple notes-vs-drafts split:

1. **The output layer has channels, not just one bucket.** Each channel encodes a *format convention* (interview answers use STAR, talks use 3-act, blog posts use hook-promise-payoff). The channel structure is part of the system, not an afterthought.

2. **Both layers are persistent and committed**, not "drafts I throw away." Even output-layer deliverables get checked in — the value is in the *next* interview reusing the framing, not in the markdown surviving forever.

3. **The compiler (LLM) treats them differently.** Compile phase touches knowledge only. Package phase touches output only. Lint phase audits both but in different ways (knowledge: contradictions and gaps; output: stale references to past dates / companies / numbers).

---

## How this relates to Karpathy's original

Karpathy's LLM Wiki (2026-04-03) is **the knowledge layer**, full stop. He doesn't talk about a second layer because his use case — personal recall for ML research and writing — doesn't have a structured external audience. His blog post *is* his output, and it draws on the wiki ad hoc.

If your goal is the same as Karpathy's (deep personal recall, occasional writing), one layer is enough — don't add the second.

The second layer earns its complexity when you have:
- A **recurring high-stakes scenario** (cycles of interviews, conference circuits, client engagements, sales calls)
- with a **predictable format** (STAR, 3-act talk, board deck, MEDDIC qualification)
- that **draws on overlapping knowledge** across instances

If those three conditions don't hold, the output layer is overhead. Ship a Karpathy wiki and stop.

---

## Failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| Output pages reference companies/dates that no longer exist | Output layer wasn't pruned after the event | Lint pass: flag output pages older than N days; user decides delete vs archive |
| The same fact is restated in 4 portfolio cases | Output pages duplicated content from knowledge instead of linking | Refactor: extract to a knowledge page; replace duplicates with `[[link]]` |
| Knowledge pages drift toward interview-speak | No discipline on the contract; user edited knowledge while preparing an interview | Add a rule: during PACKAGE phase, knowledge pages are read-only |
| Channels proliferate ("maybe I need a `podcasts/` channel?") | New channel created without a real upcoming event | Rule: no channel without a calendar item |
| `raw/` is empty; everything goes directly to knowledge | User skipped the INGEST step | Insist on provenance: every knowledge page cites a `raw/` source or external URL |
| Vault is mostly output layer with thin knowledge | User is shipping deliverables without compounding | Each PACKAGE phase must update at least one knowledge page (the lessons from the event) |

---

## When to break the rules

The pattern is a default, not a constitution. Cases where you should bend it:

- **Solo creator with one channel only.** If you only ever blog, the output layer collapses to `posts/`. Fine — but keep the knowledge layer separate; don't make `posts/` your only folder.
- **Very fast-moving domain.** If half the knowledge becomes obsolete every quarter (early-stage startup market intel), shorten the lint cycle. Don't abandon the layer.
- **Team-shared wiki.** This pattern is for *personal* knowledge. A team wiki has different access patterns and probably needs a different tool. Don't force this onto a team.
