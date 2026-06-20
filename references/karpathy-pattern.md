# Karpathy's LLM Wiki — the origin and what this extends

> This skill is a derivative work, not an original idea. Attribution and the specific extension.

---

## The original

On **2026-04-03**, Andrej Karpathy posted on X about a shift in how he uses LLMs: from generating code to generating *knowledge structure*. The post described a pattern he calls the **LLM Wiki**.

Core claims (as widely summarized in community write-ups):

- An LLM agent ingests his notes, conversations, and reading, then writes and incrementally maintains a structured, interlinked markdown wiki.
- The wiki contains entity pages, concept pages, source summaries, contradictions, and cross-references.
- **Not RAG.** Instead of retrieving raw documents at query time, the LLM continuously *compiles* the documents into a persistent structured wiki. The wiki is the artifact; queries hit the wiki, not the raw sources.
- **Why not RAG:** for personal-scale knowledge (hundreds to low-thousands of sources), RAG "re-discovers" knowledge every time without accumulation. A compiled wiki accumulates.
- **Portability is load-bearing.** Plain markdown. Flat-ish folders. Should work with any LLM that exists today or in ten years.
- The LLM does the writing, linking, and bookkeeping. The human curates sources and asks questions.

The 4-phase loop, as described in community implementations:

1. **Ingest** — new sources land in `raw/`
2. **Compile** — LLM incrementally updates the wiki
3. **Query & Enhance** — answers get filed back into the wiki
4. **Lint** — health checks, gap-finding, contradiction flagging

A community gist accumulated thousands of stars within hours of his post; there are now multiple implementations and write-ups.

---

## What this skill takes directly from Karpathy

- The **raw → compiled wiki** flow
- **Incremental compilation** (never reprocess from scratch)
- **LLM as compiler, human as curator**
- **Flat portable markdown**
- The **4-phase loop** (kept intact as phases 1–4)
- The **link graph with backlinks**
- **No RAG, no vector DB** for personal-scale vaults

If you only need these, use Karpathy's pattern directly. This skill is overhead you don't need.

---

## What this skill adds

### 1. An explicit output layer

Karpathy's wiki *is* the deliverable for his use case (his own recall). For users whose knowledge has to serve *recurring external audiences* with *formatted deliverables*, this skill adds a second layer:

```
                    ┌─────────────────────────┐
raw/  ──compile──→  │  knowledge/ (Karpathy)  │  ──package──→  output channels
                    │  audience-agnostic      │                 (audience-shaped)
                    │  durable                │
                    └─────────────────────────┘
```

The knowledge layer is unchanged from Karpathy. The output layer is the addition.

### 2. A 5th phase: Package

Inserted between Lint and the next Ingest cycle. Triggered by a real upcoming audience event. Drafts a deliverable in a channel's format convention. Knowledge layer stays read-only during this phase. See [compilation-flow.md](compilation-flow.md).

### 3. The 6-page-type taxonomy

Karpathy's community implementations vary on page types. This skill commits to 6 types (4 knowledge + 2 output) and refuses to grow beyond them. See [page-types.md](page-types.md).

### 4. The one-directional contract

A formal rule: knowledge pages must not link forward to output deliverables. Output deliverables must link back to knowledge. The asymmetry is what makes the output layer pruneable without breaking knowledge. See [cross-references.md](cross-references.md).

### 5. A post-event compile loop

After an output deliverable ships and the human reports back, a small compile pass adds the new lessons to the knowledge layer. This is what closes the loop and makes the dual-layer system compound *faster* than a single-layer wiki (since external audiences surface gaps you'd never notice in solo recall).

---

## When to use Karpathy's original instead

Use the **original single-layer LLM Wiki**, not this skill, when:

- Your knowledge serves *you* and occasional ad-hoc writing only
- You don't have recurring formatted deliverables (interview cycles, talk circuits, sales pipelines)
- You'd rather one fewer concept to maintain
- You're a researcher whose blog is the only output and it draws ad hoc

Use **this skill's dual-layer extension** when:

- You have a recurring high-stakes scenario (job search, conference circuit, client engagements)
- The same knowledge has to be re-shaped for different audiences regularly
- Deliverables have predictable formats worth encoding (STAR, 3-act, MEDDIC, deck templates)
- You've felt the pain of either (a) interview-prep notes corrupting your knowledge base, or (b) re-deriving the same framing from scratch every cycle

If neither set fully fits, default to Karpathy's original. Add the second layer only when the friction shows up.

---

## How to cite

```
This wiki uses the dual-layer extension of Andrej Karpathy's LLM Wiki pattern
(2026-04-03). The knowledge layer follows Karpathy's original; the output layer
and packaging phase are extensions described in:
https://github.com/Jackychen-12/knowledge-output-wiki
```

---

## Further reading

- The original Karpathy post (search "Karpathy LLM Wiki April 2026" — link not embedded here because URL stability is unknown)
- Community write-ups exist on MindStudio, DAIR.AI Academy, ToolMesh, Codersera, AIBuilderClub, and several personal blogs — search "Karpathy LLM Wiki" for current implementations
- Karpathy's prior thinking on LLMs as compilers (various X posts and the [nanoGPT](https://github.com/karpathy/nanoGPT) repo's design philosophy) is useful background

The references above are starting points, not endorsements of specific implementations. The pattern itself is what matters; implementations vary.
