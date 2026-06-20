# knowledge-output-wiki

A Claude skill describing a **dual-layer personal wiki** pattern: long-term compounding knowledge plus short-term scenario-packaged outputs.

Extends [Andrej Karpathy's LLM Wiki](references/karpathy-pattern.md) (April 2026) with an explicit *output layer* and a 5th compilation phase (*Package*).

---

## TL;DR

```
raw/              KNOWLEDGE LAYER              OUTPUT LAYER
(staging)         (long-term compound)         (short-term packaging)
────────          ─────────────────────        ──────────────────────
clippings    →    concept pages          →    talks
papers       →    methodology pages      →    interviews
transcripts  →    case notes             →    proposals
chats        →    reading notes          →    blog posts
projects      │                           │    resume bullets
              │                           │
   LLM compiles ──┘   LLM packages ───────┘
   (Karpathy)          (the extension)
```

- **Knowledge layer = Karpathy's wiki.** Topic-organized concept pages. Optimized for recall and reuse.
- **Output layer = goal-organized deliverables.** Each output draws from knowledge, formatted for a specific audience. Disposable after the event.
- **Both layers are flat markdown.** Portable across LLMs, editors, and decades.

The split earns its complexity when the *same* knowledge has to serve *recurring external audiences* with *predictable formats* (interview cycles, talk circuits, client engagements, sales pipelines). For pure personal recall, use Karpathy's single-layer pattern directly.

---

## Repo layout

```
.
├── SKILL.md                       ← entry point — read this first
├── README.md                      ← you are here
├── LICENSE
│
├── references/                    ← load on demand
│   ├── architecture.md            ← deep dive on the two-layer model
│   ├── page-types.md              ← the 6-type taxonomy
│   ├── compilation-flow.md        ← 5-phase loop (Karpathy 4 + Package)
│   ├── cross-references.md        ← link graph rules
│   └── karpathy-pattern.md        ← attribution + what this extends
│
├── templates/                     ← starter files
│   ├── knowledge-page.md
│   ├── output-page.md
│   ├── index.md
│   └── log.md
│
├── examples/                      ← instantiations for common personas
│   ├── researcher.md
│   ├── creator.md
│   └── jobseeker.md
│
└── scripts/
    └── compile_wiki.py            ← link graph + single-file HTML viewer
```

---

## How to use this as a Claude skill

### Option A — symlink into your skills directory

```bash
git clone https://github.com/Jackychen-12/knowledge-output-wiki ~/code/knowledge-output-wiki
ln -s ~/code/knowledge-output-wiki ~/.claude/skills/knowledge-output-wiki
```

Then in any Claude Code conversation, the skill triggers when you ask about personal knowledge bases, Karpathy's LLM Wiki, or compiling notes into a structured wiki.

### Option B — read the skill manually

```bash
git clone https://github.com/Jackychen-12/knowledge-output-wiki
cat knowledge-output-wiki/SKILL.md
```

Then paste the relevant section into your LLM of choice. The skill is provider-agnostic — it's just markdown.

### Option C — use the templates directly

The `templates/` folder works as starter files for any new wiki, with or without an LLM. Copy them into your `wiki/` directory and edit.

---

## Worked examples

The `examples/` folder shows how the dual-layer pattern instantiates for three common personas:

- [`researcher.md`](examples/researcher.md) — outputs are papers, talks, grant proposals
- [`creator.md`](examples/creator.md) — outputs are blog posts, video scripts, newsletter issues
- [`jobseeker.md`](examples/jobseeker.md) — outputs are portfolio cases, interview prep, resume tailorings

Each example shows folder structure, format conventions per channel, the compilation loop, and persona-specific anti-patterns.

---

## The compile script

`scripts/compile_wiki.py` is an optional Python script that:

- Scans a `wiki/` directory of markdown files
- Resolves `[[wiki-style-links]]` and standard markdown links into a link graph
- Generates a single-file HTML viewer with navigation and backlinks

It's a reference implementation, not a required component. The whole pattern works with plain markdown in any editor.

```bash
cd your-wiki
python3 path/to/compile_wiki.py
# → produces index.html
```

---

## Attribution

This skill is a derivative of Andrej Karpathy's LLM Wiki concept (posted on X, 2026-04-03). The knowledge layer follows his pattern unchanged. The output layer and the 5th *Package* phase are the contributions of this skill.

See [references/karpathy-pattern.md](references/karpathy-pattern.md) for the full attribution and a frank discussion of when to use Karpathy's original instead of this dual-layer extension.

---

## License

MIT. See [LICENSE](LICENSE).
