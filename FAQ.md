# FAQ

## What HTML elements are stripped?
`<script>`, `<style>`, `<nav>`, `<header>`, `<footer>`, `<aside>` — anything that's not content.

## Does it handle malformed HTML?
Yes. `HTMLParser` is lenient with broken tags, unclosed elements, and entities.

## Can I use it in a pipeline?
Yes: `curl https://page.com | python3 scripts/convert.py` or `--json` for machine-readable.

## How is this different from html2text?
No pip install needed, built-in URL fetching, YAML frontmatter, JSON output mode.

## Does it support tables?
Basic. Tables are complex to convert to Markdown. For table-heavy pages, consider pandoc.
