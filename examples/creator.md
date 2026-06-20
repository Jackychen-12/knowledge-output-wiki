# Example instantiation — creator / writer

> A solo creator, blogger, YouTuber, newsletter author whose recurring outputs are posts, videos, episodes.

---

## Folder structure

```
my-wiki/
├── raw/
│   ├── readings/             ← articles, books worth keeping
│   ├── transcripts/          ← podcast / video transcripts you saved
│   ├── inspiration/          ← screenshots, quotes, examples of craft
│   └── conversations/        ← DMs, comments, audience questions
│
├── wiki/
│   ├── index.md
│   ├── log.md
│   │
│   ├── knowledge/
│   │   ├── index.md
│   │   ├── craft/                  ← how to make the thing (writing, video, audio)
│   │   │   ├── index.md
│   │   │   └── methodology.md
│   │   ├── topics/                 ← what your work is about
│   │   │   ├── index.md
│   │   │   ├── <theme-1>/
│   │   │   │   ├── methodology.md
│   │   │   │   └── cases.md
│   │   │   └── <theme-2>/
│   │   ├── audience/               ← what you know about who's listening
│   │   │   └── index.md
│   │   └── readings/
│   │       └── <source>.md
│   │
│   ├── posts/                      ← OUTPUT: blog drafts
│   │   ├── index.md
│   │   └── <post-slug>.md
│   │
│   ├── videos/                     ← OUTPUT: video scripts
│   │   ├── index.md
│   │   └── <video-slug>.md
│   │
│   └── newsletter/                 ← OUTPUT: weekly/monthly issues
│       ├── index.md
│       └── <issue-N>.md
```

---

## Format conventions per channel

| Channel | Format | Sections |
|---|---|---|
| `posts/` | hook-promise-payoff | hook → setup → turn → payoff → cta |
| `videos/` | script with timing | cold open → premise → 3 beats → callback → cta |
| `newsletter/` | curation + commentary | intro → 3 picks with commentary → ask |

---

## How the loop runs

- **Ingest:** save things that *taught you something about craft or topic*, not everything you read. Inspiration folder is fine to be messy.
- **Compile:** new readings extract into `topics/<theme>/methodology.md` (frameworks) and `cases.md` (specific examples). Craft observations go to `craft/`.
- **Lint:** find themes with thin coverage (need more reading); find posts older than 6 months whose framing should be updated in a follow-up.
- **Package:**
  - **Post:** pick 1 theme, 1 hook, 1–3 cases. Sources section is short — posts shouldn't try to be comprehensive.
  - **Video:** like a post but with timing notes. Reuse hooks that worked in posts.
  - **Newsletter:** curated from `readings/` (latest entries) + commentary from `topics/`.
- **Post-event compile:**
  - Comment thread on a post that surfaced a new angle → new case in the topic
  - DM asking a question you can't answer → add to a "what I don't know" page; surface in next lint
  - A post that flopped → annotate the post page with hypothesis on why; over time, build a `craft/methodology.md` section on "what doesn't land"

---

## Anti-patterns specific to creators

- **Treating `posts/` as the only folder.** Two years in, you have 200 posts and no framework. Each new post is a fresh derivation. The knowledge layer is what makes post 200 easier to write than post 20.
- **Audience pages with persona templates.** Personas rot. Better: a single page of *real* observations (specific reader comments, real DMs, actual sales conversations) that compounds.
- **Newsletter as both knowledge and output.** Newsletter issues are output. The reading notes you draw from are knowledge. Don't merge — newsletter issues age out; reading notes don't.
- **Drafting in `raw/`.** Drafts go in the output channel from the start. Raw is for *inputs*, not work-in-progress outputs.
