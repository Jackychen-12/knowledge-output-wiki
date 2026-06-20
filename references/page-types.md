# Page types — the 6-type taxonomy

> Every page in the wiki is exactly one of 6 types. If a draft doesn't fit, it doesn't belong yet.

---

## Knowledge layer

### 1. Index page

**Filename:** `<topic>/index.md` (also `knowledge/index.md` for the layer root)

**Purpose:** Hub. Lists every page in the topic with a one-line summary. Entry point for navigation and for the LLM during retrieval.

**Required sections:**
- One-paragraph topic definition
- Table of pages with one-line "what's here"
- Growth direction (what's coming next)

**Maintenance:** LLM updates this automatically on every COMPILE that adds/removes a page in the topic.

```markdown
# <Topic name>

> One-paragraph plain-English definition of this topic and why it matters to you.

| Page | What's here |
|---|---|
| [[methodology]] | Frameworks for evaluating <X> |
| [[cases]] | <N> worked examples |
| [[reading-notes]] | Key sources |

**Growth direction:** what kinds of pages would belong here next.
```

---

### 2. Methodology page

**Filename:** `<topic>/methodology.md`

**Purpose:** The *how to think about this* layer. Frameworks, rubrics, principles, evaluation criteria, decision trees. This is the page that survives the longest — methodologies change slowly.

**Required sections:**
- Core concept (1–3 sentences, no jargon)
- Frameworks / rubrics (tables and lists work well)
- Anti-patterns and pitfalls
- Sources / influences

**Anti-pattern:** Don't fill methodology pages with examples. Cases go on case pages. A methodology page should be readable without any specific instance.

---

### 3. Case / notes page

**Filename:** `<topic>/cases.md` (aggregated) OR `<topic>/<case-slug>.md` (per-case)

**Purpose:** Concrete instances. What you actually built, decided, measured, observed. Decision records. Project deep-dives. Specific evidence.

**Use aggregated `cases.md`** when cases are short (≤200 words each) and benefit from comparison.

**Use per-case `<case-slug>.md`** when cases are long (>500 words), have their own sub-structure, or are likely to be cited individually from output pages.

**Required sections (per case):**
- Context (1–2 sentences: when, what, why it mattered)
- What happened (specific, verifiable)
- What you learned (the durable takeaway)
- Source / provenance (link to raw/ or external)

---

### 4. Reading page

**Filename:** `readings/<source-slug>.md`

**Purpose:** Distillation of *one* external source — book, paper, long article, talk, podcast. The point is to extract the source's takeaways once, so future-you doesn't have to re-read.

**Required sections:**
- Source citation (title, author, year, URL)
- Why you read it (your reason — useful when revisiting)
- 3–7 key takeaways (bullets)
- Quotes worth saving (with page/timestamp)
- Where this connects (`[[link]]` to relevant concept pages)

**Anti-pattern:** Don't put the methodology *from* the reading into the reading page. Extract methodologies into the topic's `methodology.md` and reference back: "Framework X (see [[reading: …]])". This is how reading compounds — the source is in one place, the framework is woven into the topic.

---

## Output layer

### 5. Deliverable page

**Filename:** `<channel>/<deliverable-slug>.md`

**Purpose:** One audience-shaped artifact. Examples by channel:

| Channel | Deliverable examples |
|---|---|
| `interview/` | `behavioral-leadership.md`, `case-pricing-strategy.md` |
| `talks/` | `keynote-conference-2026.md`, `lightning-internal.md` |
| `portfolio/` | `<project-name>.md` (STAR-formatted) |
| `blog/` | `post-on-X.md` (draft) |
| `proposals/` | `client-acme-discovery.md` |

**Required sections (vary by channel — channel index defines the template):**
- Audience and event (who, when, what context)
- The framework being used (STAR, 3-act, hook-promise-payoff, etc.)
- The content, written in audience voice
- Links to knowledge pages this draws from (`Sources: [[…]], [[…]]`)
- Anticipated follow-ups / questions

**Discipline:** every deliverable's `Sources:` section must point at knowledge pages. If a deliverable has no sources, you're either (a) winging it, or (b) you should compile the underlying facts into knowledge first.

---

### 6. Channel index

**Filename:** `<channel>/index.md`

**Purpose:** What's in this channel, what format conventions apply, how to pick which deliverable for which audience.

**Required sections:**
- Channel definition (who is this for, what format)
- The format convention (template / rubric the channel uses)
- Table of deliverables with audience + date
- Retention policy (when to archive/delete past deliverables)

**Why this matters:** the channel index is where the format convention lives. Without it, deliverables in the same channel drift into inconsistent formats and the channel loses its value.

---

## Type decision flowchart

```
Is this a new piece of content?
│
├─ Is it raw source material (clipping, transcript, file)?
│      → goes in raw/<bucket>/  (not a wiki page)
│
├─ Is it "what I learned"?
│   │
│   ├─ A framework or principle?              → methodology page (#2)
│   ├─ A specific example or decision?        → case page (#3)
│   ├─ Distillation of one source?            → reading page (#4)
│   └─ A hub linking the above?               → index page (#1)
│
└─ Is it "what I'm shipping to an audience"?
    │
    ├─ A specific deliverable?                → deliverable page (#5)
    └─ A hub for one channel?                 → channel index (#6)
```

If the content doesn't match any of the 6, the right move is usually one of:

1. It's still raw → drop in `raw/`
2. It mixes two types → split into two pages
3. It's ephemeral task chatter → don't add to the wiki at all

---

## Frontmatter convention

Use frontmatter only when it earns its keep. Two fields are worth it:

```yaml
---
type: methodology | case | reading | deliverable | index | channel-index
updated: 2026-06-19
---
```

`type` makes lint passes machine-checkable. `updated` is the only metadata field worth maintaining by hand — the LLM updates it on every edit.

Resist the urge to add `tags:`, `status:`, `priority:`, etc. Those are Notion-database thinking. Karpathy's portability principle: anything you'd need a database query to use should not be in the wiki.
