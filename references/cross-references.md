# Cross-references — the link graph

> Two link styles. Three rules. How the graph stays alive instead of rotting.

---

## The two link styles

```markdown
[[topic-slug]]                  ← wiki-style; resolves to <topic-slug>.md somewhere
[label](relative/path.md)       ← standard markdown; works in any viewer
```

**When to use which:**

- **`[[topic-slug]]`** inside the knowledge layer for concept-to-concept links. Allowed to be "broken" — a `[[link]]` to a non-existent page is a writing prompt, not an error.
- **`[label](relative/path.md)`** for any link to (a) a deliverable in the output layer, (b) a raw source, (c) an external URL, (d) anywhere a renderer that doesn't support `[[]]` would matter (e.g. GitHub's markdown view).

If in doubt: `[[]]` for ideas, `[]()` for files.

---

## The three rules

### Rule 1 — Backlinks are bidirectional in the knowledge layer

Every cross-reference within `knowledge/` should be discoverable from both sides. If `page-A.md` says `[[page-b]]`, then `page-B.md` should also reference back to `page-A` — usually in a `## Related` section near the bottom.

The LLM maintains these. The human doesn't have to think about it; they just write `[[]]` wherever it feels natural.

Why bidirectional? Because the future-you who lands on `page-B` for an unrelated reason should *discover* `page-A`. One-directional links only help if you already know to start from `page-A`.

---

### Rule 2 — Output → knowledge is required; knowledge → output is forbidden

Every deliverable in the output layer must end with a `Sources:` section listing the knowledge pages it draws from:

```markdown
## Sources
- [[topic-x/methodology]] — for the framework
- [[topic-y/cases#case-3]] — for the comparison
- [[readings/<source-slug>]] — for the contrarian data point
```

But knowledge pages should *not* link to deliverables. The deliverable mentions a specific company, date, audience; the knowledge page is durable. Linking forward couples the durable to the disposable. When the deliverable is archived, the knowledge page becomes a broken link.

The asymmetry is the whole point.

---

### Rule 3 — Provenance is non-negotiable

Every claim in a knowledge page must be traceable to either:

- A `raw/` file in this vault, or
- An external URL (with date accessed for things that drift), or
- An explicit `(personal experience)` tag if it's your own observation

Pages without provenance are landmines. Two years from now, you won't remember whether you read it, made it up, or assumed it. The lint phase flags unsourced claims.

```markdown
> Source: [[raw/readings/<source-slug>]]
> Source: <https://example.com/article> (accessed 2026-06-19)
> (personal experience — from project <slug>)
```

---

## The link graph as a system property

If you follow the three rules, the link graph develops two useful properties:

1. **Density grows superlinearly inside knowledge.** Every new concept page adds links to existing pages; existing pages add back-references. After ~30 pages, the graph stops being a tree and starts being a small dense graph. This is when retrieval gets fast — "what do I know about X" surfaces 5 connected pages, not 1.

2. **Output layer stays a thin one-way veneer.** Deliverables are leaves of the graph. They point inward and nothing points back at them. This means: deleting an old deliverable never breaks anything else. The output layer is *pruneable*.

The whole architecture's "compounding" property comes from these two facts together. Knowledge gets denser; outputs stay disposable; the human's job is to feed the loop, not maintain the structure.

---

## What the LLM does with the graph

During COMPILE:
- After writing/editing a page, re-scan its links and add backlinks to the targets
- If a `[[link]]` points to a non-existent page, leave it (it's a writing prompt)
- If a `[label](path.md)` points to a non-existent file, flag it (it's a broken link)

During LINT:
- List `[[broken-links]]` as "candidate pages to write"
- List orphans (knowledge pages with zero inbound links) — usually a sign they should be merged or are reading-only pages without extracted insights
- List hubs (pages with >15 inbound links) — usually fine, sometimes a sign the topic should split

During PACKAGE:
- Use the link graph to find candidate knowledge pages for a deliverable
- Fill the `Sources:` section automatically from pages cited in the draft
- Never create new knowledge pages (that's COMPILE's job)

---

## Anti-patterns

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Linking everything to everything | Every page has 30+ links; signal lost in noise | Link only to pages that meaningfully *contextualize* the current one. ≤7 outbound links per page is a good ceiling |
| Knowledge → deliverable links | A `methodology.md` links to `interview/2026-acme-prep.md` | Delete the link; the deliverable should link *up* not the other way |
| `[[]]` links that don't follow the slug convention | `[[my interview prep!!!]]` resolves to nothing | Slug convention: kebab-case, ASCII, matches a real filename |
| Using `[[]]` to link to deliverables | Output layer "looks like" knowledge | Use `[]()` for the output layer — it's not the same kind of citation |
| Adding URLs without "accessed" date | Two years later you don't know if the page still says that | Always include access date for external URLs |
| Treating a wiki-style search engine as a substitute for index pages | "I'll just search when I need it" | Search finds things you remember exist. Index pages surface things you forgot existed. Both matter |

---

## Implementation note

If you use a viewer like Obsidian, `[[]]` is native. If you use plain markdown (GitHub, VS Code preview), `[[]]` won't render as a link by default — but it'll still appear as visible text, which is fine for a human reader and trivial to grep for. A small compiler script (see [scripts/compile_wiki.py](../scripts/compile_wiki.py)) can resolve `[[]]` into clickable HTML if you want a single-file viewer.

Karpathy's portability principle: don't pick a tool that locks the markdown into its own format. The wiki should still make sense if you `cat` the files.
