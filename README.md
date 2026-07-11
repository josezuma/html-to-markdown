<div align=center>
  <h1>📄 HTML to Markdown</h1>
  <p><em>Convert HTML pages or local files to clean, readable Markdown. Fetches URLs, strips scripts/styles/nav, preserves headings, links, code blocks, and lists.</em></p>
  <p><a href=LICENSE><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt=License></a></p>
  <p><strong>Author:</strong> <a href=https://github.com/josezuma>Jose Zuma</a></p>
</div>

---

## Quick Start

```bash
# Convert a URL
python3 scripts/convert.py https://example.com

# Convert a local file
python3 scripts/convert.py article.html --output article.md

# Pipe HTML from curl or clipboard
curl https://example.com | python3 scripts/convert.py

# JSON output (for pipe to jq or other tools)
python3 scripts/convert.py https://example.com --json
```

## Demo

```bash
$ python3 scripts/convert.py https://brandvirality.com --no-frontmatter | head -20

# BrandVirality — SaaS for AI Visibility

[BrandVirality](https://brandvirality.com) makes your business discoverable in every AI search engine.

## Features

- **GEO Audits** — Score your URL's AI-search readiness
- **Share of Voice** — Track brand mentions across LLMs
- **Competitor Monitoring** — Watch your competitors' GEO scores
- **Prompt Optimization** — Rewrite content for AI citation
```

## Features

| Feature | Description |
|---------|-------------|
| **URL fetch** | Downloads and converts any public URL |
| **Local files** | Reads `.html` files from disk |
| **Stdin** | Pipe HTML directly |
| **Smart stripping** | Removes scripts, styles, nav, header, footer |
| **Heading hierarchy** | H1→H6 preserved as `#` through `######` |
| **Links preserved** | `[text](url)` format |
| **Code blocks** | `<pre>` and `<code>` preserved |
| **Lists** | Ordered and unordered lists |
| **YAML frontmatter** | Auto-adds title, source, date |
| **JSON mode** | Machine-readable output for pipelines |
| **No dependencies** | Python stdlib only — `html.parser`, `urllib` |

## Why Not Just Use pandoc or html2text?

| Tool | Pros | Cons |
|------|------|------|
| **pandoc** | Full-featured, many formats | 200MB+ install, heavy dependency |
| **html2text** | Popular, pip-installable | Requires pip, no URL fetch built-in |
| **This one** | Zero deps, URL fetch, stdin, JSON | Fewer format options |

This tool is for when you need a quick HTML→Markdown conversion without installing anything.

## Related

- [markdown-to-html](https://github.com/josezuma/markdown-to-html)
- [template-engine](https://github.com/josezuma/template-engine)
- [slug-generator](https://github.com/josezuma/slug-generator)
- [word-counter](https://github.com/josezuma/word-counter)

## License

MIT © 2026 Jose Zuma
