# Example instantiation — job seeker

> Someone in an active job search (or perpetually open to opportunities) whose recurring outputs are interview answers, resume tailorings, take-home cases, and industry POVs.

---

## Folder structure

```
my-wiki/
├── raw/
│   ├── projects/             ← files from things you actually built/shipped
│   ├── readings/             ← industry reports, technical posts
│   ├── interviews/           ← debriefs from interviews you've done
│   └── conversations/        ← coffee chats, recruiter calls
│
├── wiki/
│   ├── index.md
│   ├── log.md
│   │
│   ├── knowledge/
│   │   ├── index.md
│   │   ├── domain/                 ← what you know about your target field
│   │   │   ├── index.md
│   │   │   ├── methodology.md
│   │   │   └── cases.md
│   │   ├── projects/               ← deep-dive on each project (technical)
│   │   │   ├── index.md
│   │   │   └── <project-slug>.md
│   │   ├── market/                 ← industry intel, company landscape
│   │   │   ├── index.md
│   │   │   └── <segment>.md
│   │   └── readings/
│   │       └── <source>.md
│   │
│   ├── portfolio/                  ← OUTPUT: STAR-format project cases
│   │   ├── index.md
│   │   └── <project-slug>.md
│   │
│   ├── interview/                  ← OUTPUT: per-role / per-question prep
│   │   ├── index.md
│   │   ├── <role-type-1>/          (e.g. one folder per role type you target)
│   │   │   └── overview.md
│   │   └── <role-type-2>/
│   │
│   ├── industry/                   ← OUTPUT: independent POVs on the field
│   │   ├── index.md
│   │   └── <topic>.md
│   │
│   └── branding/                   ← OUTPUT: resume bullets, intro scripts
│       ├── index.md
│       └── resume-bullets.md
```

---

## Format conventions per channel

| Channel | Format | Sections |
|---|---|---|
| `portfolio/` | STAR+ | situation → task → action → result → reflection + anticipated follow-ups |
| `interview/<role>/` | role-tailored | role overview → ability matrix → top-N likely questions → checklist |
| `industry/` | POV piece | 30-second take → evidence → contrarian angle |
| `branding/` | bullet bank | role-typed bullets + intro scripts, copy-paste ready |

---

## How the loop runs

- **Ingest:** at the end of every project, dump source files + a 1-paragraph retrospective into `raw/projects/<slug>/`. After every interview, drop a debrief in `raw/interviews/`.
- **Compile:** each project gets a full technical deep-dive in `knowledge/projects/<slug>.md` (architecture, decisions, what worked). Industry readings extract into `knowledge/market/<segment>.md` and `knowledge/domain/methodology.md`.
- **Lint (weekly during active search):** find roles where you have an interview soon but no prep page; find portfolio cases where the underlying knowledge page is stale.
- **Package:**
  - **Per upcoming interview at a specific company:** new file in `interview/<role>/<company-slug>.md`. Sources section pulls from `domain/`, `market/<segment>.md`, and 2–3 `projects/`.
  - **Resume tailoring for a role type:** update `branding/resume-bullets.md` with a new role-typed section. Bullets are 1-line drafts derived from full `portfolio/<project>.md` STARs.
  - **Industry POV (for conversations + cold outreach):** `industry/<topic>.md`. Cite `market/` heavily.
- **Post-event compile:** every interview debrief reveals (a) a question you didn't have prepped — add to the role's `overview.md`; (b) a project framing that didn't land — refine the portfolio page; (c) industry knowledge gaps — back into `domain/`.

---

## Why dual-layer matters in a job search

A single-layer "interview prep" Notion vault has two specific failure modes:

1. **Project pages serve double duty.** They start as technical deep-dives (useful for you) and drift into STAR-formatted interview material (useful for recruiters). After 3 months, they're useful for neither — too STAR-ified to remember the real technical context, too technical to land in a behavioral interview.
2. **Industry intel is constantly re-derived.** Every coffee chat, every "tell me what you think about X", you scramble through old reading notes. A `market/` knowledge page that's been compiled from 20 readings answers in 30 seconds.

The dual-layer keeps `projects/<slug>.md` (knowledge — technical truth) and `portfolio/<slug>.md` (output — STAR-formatted for interviews) as separate files. Update one without touching the other. When the role changes (PM ↔ engineer ↔ consultant), rebuild the `portfolio/` layer without losing the `projects/` layer.

---

## Retention policy

- **Knowledge layer:** keep forever. Even old project deep-dives are evidence for "I've done X kind of work" 5 years later.
- **Output layer:** prune aggressively. Company-specific interview prep older than 60 days = archive. Resume bullets reorganized for a role type you no longer pursue = delete. The point of the output layer is that it's *cheap to throw away* because the knowledge persists.
