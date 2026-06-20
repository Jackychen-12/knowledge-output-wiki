#!/usr/bin/env python3
"""
Generic wiki compiler — reference implementation.

Scans a wiki/ directory of markdown files, resolves [[wiki-links]] and standard
markdown links into a link graph, and emits a single-file HTML viewer.

This is a stripped-down generic version with no project-specific assumptions.
Adapt the styles and layout to taste.

Usage:
    python3 compile_wiki.py                # scans current directory
    python3 compile_wiki.py path/to/wiki   # scans the given directory
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


WIKI_LINK_RE = re.compile(r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]')
MD_LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+\.md)\)')


def scan_wiki(wiki_dir: Path) -> dict:
    """Walk the wiki directory and return {page_id: page_dict}."""
    pages = {}
    for root, dirs, files in os.walk(wiki_dir):
        # Skip dot directories and a conventional `raw/` staging folder.
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'raw']
        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = Path(root) / fname
            rel = fpath.relative_to(wiki_dir)
            page_id = str(rel).replace('.md', '').replace(os.sep, '/')
            content = fpath.read_text(encoding='utf-8')

            # Use first H1 as title; fall back to filename.
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else fname[:-3]

            pages[page_id] = {
                'id': page_id,
                'title': title,
                'path': str(rel),
                'content': content,
            }
    return pages


def extract_links(pages: dict) -> list:
    """Build the link graph as a list of {source, target, kind} edges."""
    edges = []
    page_ids = set(pages.keys())

    # Build a slug → page_id lookup for [[wiki-links]] resolution.
    slug_to_id = {}
    for pid in page_ids:
        slug = pid.split('/')[-1]
        slug_to_id.setdefault(slug, pid)
        slug_to_id.setdefault(pid, pid)

    for pid, page in pages.items():
        content = page['content']
        seen = set()

        for m in WIKI_LINK_RE.finditer(content):
            target_slug = m.group(1).strip()
            target_id = slug_to_id.get(target_slug)
            key = ('wiki', target_slug)
            if key in seen:
                continue
            seen.add(key)
            edges.append({
                'source': pid,
                'target': target_id or target_slug,
                'kind': 'wiki',
                'resolved': target_id is not None,
            })

        for m in MD_LINK_RE.finditer(content):
            href = m.group(2)
            if href.startswith('http'):
                continue
            target_id = href.replace('.md', '').lstrip('./')
            # Resolve relative paths against the source page's folder.
            if not target_id.startswith('/') and '/' in pid:
                base = '/'.join(pid.split('/')[:-1])
                if not target_id.startswith(base):
                    # Try as-is first; if not found, try relative.
                    if target_id not in page_ids:
                        joined = f'{base}/{target_id}'.replace('/./', '/')
                        if joined in page_ids:
                            target_id = joined
            key = ('md', target_id)
            if key in seen:
                continue
            seen.add(key)
            edges.append({
                'source': pid,
                'target': target_id,
                'kind': 'md',
                'resolved': target_id in page_ids,
            })
    return edges


def render_html(pages: dict, edges: list) -> str:
    """Render a minimal single-file HTML viewer with nav + content."""
    # Build incoming-link index (backlinks).
    backlinks = {pid: [] for pid in pages}
    for e in edges:
        if e['resolved'] and e['target'] in backlinks:
            backlinks[e['target']].append(e['source'])

    pages_json = {
        pid: {
            'title': p['title'],
            'path': p['path'],
            'content': p['content'],
            'backlinks': sorted(set(backlinks[pid])),
        }
        for pid, p in pages.items()
    }

    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Wiki</title>
<style>
  :root {
    --bg: #fafaf7;
    --fg: #1a1a1a;
    --muted: #6b6b6b;
    --accent: #c86a4a;
    --border: #e5e2dc;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: var(--bg); color: var(--fg); display: flex; min-height: 100vh;
  }
  nav {
    width: 280px; padding: 24px; border-right: 1px solid var(--border);
    overflow-y: auto; max-height: 100vh; position: sticky; top: 0;
  }
  nav h2 { margin: 16px 0 8px; font-size: 13px; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.05em; }
  nav a { display: block; padding: 4px 0; color: var(--fg);
    text-decoration: none; font-size: 14px; }
  nav a:hover, nav a.active { color: var(--accent); }
  main {
    flex: 1; padding: 48px 64px; max-width: 760px;
  }
  main h1 { font-size: 28px; margin-top: 0; }
  main h2 { margin-top: 32px; }
  main p, main li { line-height: 1.65; }
  main a { color: var(--accent); }
  main pre { background: #f0ede6; padding: 12px 16px; border-radius: 4px;
    overflow-x: auto; font-size: 13px; }
  main table { border-collapse: collapse; margin: 16px 0; }
  main th, main td { border: 1px solid var(--border); padding: 6px 12px;
    text-align: left; }
  main th { background: #f0ede6; }
  .backlinks { margin-top: 48px; padding-top: 24px;
    border-top: 1px solid var(--border); font-size: 14px; color: var(--muted); }
  .backlinks h3 { font-size: 13px; text-transform: uppercase;
    letter-spacing: 0.05em; }
</style>
</head>
<body>
<nav id="nav"></nav>
<main id="content"></main>
<script>
const PAGES = __PAGES_JSON__;

function renderMarkdown(md) {
  // minimal MD → HTML: headings, lists, code, links, [[wikilinks]], bold/italic
  let html = md
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/```([\\s\\S]*?)```/g, (_,c) => '<pre>'+c+'</pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>')
    .replace(/\\*([^*]+)\\*/g, '<em>$1</em>')
    .replace(/\\[\\[([^\\]|]+?)(?:\\|([^\\]]+))?\\]\\]/g, (_,slug,label) => {
      const target = resolveSlug(slug.trim());
      const text = label || slug;
      if (target) return `<a href="#" onclick="show('${target}');return false">${text}</a>`;
      return `<span style="color:#c86a4a;text-decoration:underline dotted">${text}</span>`;
    })
    .replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, (m,t,h) => {
      if (h.startsWith('http')) return `<a href="${h}" target="_blank">${t}</a>`;
      const id = h.replace(/\\.md$/, '').replace(/^\\.\\//, '');
      return `<a href="#" onclick="show('${id}');return false">${t}</a>`;
    })
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\\/li>)/s, '<ul>$1</ul>')
    .replace(/\\n\\n/g, '</p><p>');
  return '<p>' + html + '</p>';
}

function resolveSlug(slug) {
  if (PAGES[slug]) return slug;
  for (const id in PAGES) if (id.endsWith('/'+slug) || id === slug) return id;
  return null;
}

function renderNav() {
  const nav = document.getElementById('nav');
  const groups = {};
  for (const id in PAGES) {
    const top = id.includes('/') ? id.split('/')[0] : '_';
    (groups[top] = groups[top] || []).push(id);
  }
  let html = '';
  for (const g of Object.keys(groups).sort()) {
    html += `<h2>${g === '_' ? 'top' : g}</h2>`;
    for (const id of groups[g].sort()) {
      html += `<a href="#" data-id="${id}" onclick="show('${id}');return false">${PAGES[id].title}</a>`;
    }
  }
  nav.innerHTML = html;
}

function show(id) {
  if (!PAGES[id]) return;
  const p = PAGES[id];
  const main = document.getElementById('content');
  let html = renderMarkdown(p.content);
  if (p.backlinks.length) {
    html += '<div class="backlinks"><h3>Backlinks</h3><ul>';
    for (const b of p.backlinks) {
      html += `<li><a href="#" onclick="show('${b}');return false">${PAGES[b].title}</a></li>`;
    }
    html += '</ul></div>';
  }
  main.innerHTML = html;
  document.querySelectorAll('nav a').forEach(a => {
    a.classList.toggle('active', a.dataset.id === id);
  });
  location.hash = id;
}

renderNav();
const initial = location.hash.slice(1) || Object.keys(PAGES)[0];
show(initial);
</script>
</body>
</html>
"""
    return template.replace('__PAGES_JSON__', json.dumps(pages_json, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('wiki_dir', nargs='?', default='.',
                        help='Path to wiki directory (default: current dir)')
    parser.add_argument('-o', '--output', default='index.html',
                        help='Output HTML file (default: index.html)')
    args = parser.parse_args()

    wiki_dir = Path(args.wiki_dir).resolve()
    if not wiki_dir.exists():
        print(f'error: {wiki_dir} does not exist', file=sys.stderr)
        sys.exit(1)

    pages = scan_wiki(wiki_dir)
    if not pages:
        print(f'error: no markdown files found under {wiki_dir}', file=sys.stderr)
        sys.exit(1)

    edges = extract_links(pages)
    html = render_html(pages, edges)

    out = wiki_dir / args.output
    out.write_text(html, encoding='utf-8')

    broken = sum(1 for e in edges if not e['resolved'])
    print(f'compiled {len(pages)} pages, {len(edges)} links '
          f'({broken} unresolved) → {out}')


if __name__ == '__main__':
    main()
