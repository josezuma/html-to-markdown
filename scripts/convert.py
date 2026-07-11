#!/usr/bin/env python3
"""html-to-markdown — Convert HTML pages or files to clean Markdown.

Fetches a URL or reads a local HTML file, strips tags, and outputs
clean Markdown with frontmatter and proper heading hierarchy.

Usage:
    python3 scripts/convert.py https://example.com
    python3 scripts/convert.py page.html --output readme.md
    curl https://example.com | python3 scripts/convert.py
"""

import sys, re, json, argparse
from html.parser import HTMLParser
from urllib.request import Request, urlopen


class HTMLToMarkdown(HTMLParser):
    BLOCK_TAGS = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'pre', 'hr', 'br'}
    
    def __init__(self):
        super().__init__()
        self.lines = []
        self.current_line = ""
        self.in_pre = False
        self.in_a = False
        self.link_href = ""
        self.link_text = ""
        self.in_strong = False
        self.in_em = False
        self.headings = []
        self.skip_tag = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ('script', 'style', 'nav', 'footer', 'header', 'aside'):
            self.skip_tag = True
            return
        if self.skip_tag:
            return
        if tag == 'pre':
            self.in_pre = True
            self._flush()
            self.current_line += "```\n"
        elif tag == 'a':
            self.in_a = True
            self.link_href = d.get('href', '')
            self.link_text = ''
        elif tag in ('strong', 'b'):
            self.in_strong = True
        elif tag in ('em', 'i'):
            self.in_em = True
        elif tag in ('h1','h2','h3','h4','h5','h6'):
            self._flush()
            level = int(tag[1])
            prefix = '#' * level + ' '
            self.current_line = prefix
            self.headings.append((level, ''))
        elif tag == 'li':
            self._flush()
            self.current_line = '- '
        elif tag == 'hr':
            self._flush()
            self.lines.append('---')
        elif tag == 'br':
            self._flush()
        elif tag == 'img':
            alt = d.get('alt', '')
            src = d.get('src', '')
            if src:
                self.current_line += f"![{alt}]({src})"

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav', 'footer', 'header', 'aside'):
            self.skip_tag = False
            return
        if self.skip_tag:
            return
        if tag == 'pre':
            self.current_line += "\n```"
            self.in_pre = False
            self._flush()
        elif tag == 'a' and self.in_a:
            if self.link_text.strip() and self.link_href:
                self.current_line += f"[{self.link_text}]({self.link_href})"
            elif self.link_href:
                self.current_line += self.link_href
            self.in_a = False
        elif tag in ('strong', 'b'):
            self.in_strong = False
        elif tag in ('em', 'i'):
            self.in_em = False
        elif tag == 'p' or tag.startswith('h'):
            self._flush()
            self.lines.append('')
        elif tag in ('ul', 'ol'):
            self._flush()

    def handle_data(self, data):
        if self.skip_tag:
            return
        if self.in_a:
            self.link_text += data
            return
        if self.in_pre:
            self.current_line += data
            return
        
        text = data.strip()
        if not text:
            return
        
        if self.in_strong:
            text = f"**{text}**"
        if self.in_em:
            text = f"*{text}*"
        
        if self.current_line.startswith('#'):
            if self.headings and self.headings[-1][1] == '':
                self.headings[-1] = (self.headings[-1][0], text[:80])
        
        self.current_line += text + ' '

    def handle_entityref(self, name):
        char_map = {'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"', 'apos': "'"}
        self.current_line += char_map.get(name, f'&{name};')

    def _flush(self):
        line = self.current_line.strip()
        if line:
            self.lines.append(line)
        self.current_line = ""

    def get_markdown(self, title=None):
        self._flush()
        md = []
        if title:
            md.append(f"# {title}")
            md.append("")
        md.extend(self.lines)
        return '\n'.join(md)


def fetch_url(url, timeout=10):
    req = Request(url, headers={"User-Agent": "html-to-markdown/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def extract_title(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.DOTALL)
    return m.group(1).strip() if m else None


def convert(html, title=None):
    parser = HTMLToMarkdown()
    parser.feed(html)
    return parser.get_markdown(title)


def main():
    parser = argparse.ArgumentParser(description="Convert HTML to Markdown")
    parser.add_argument("input", nargs="?", help="URL or local file path")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--title", help="Document title (auto-extracted if not set)")
    parser.add_argument("--no-frontmatter", action="store_true", help="Skip YAML frontmatter")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    html = None
    source = args.input

    if source and source.startswith(('http://', 'https://')):
        html = fetch_url(source)
        if not html:
            print(f"Error: Failed to fetch {source}", file=sys.stderr)
            sys.exit(1)
    elif source:
        try:
            with open(source) as f:
                html = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {source}", file=sys.stderr)
            sys.exit(1)
    else:
        html = sys.stdin.read()

    title = args.title or extract_title(html) or "Untitled"
    md = convert(html, title=None)

    if args.json:
        result = {"title": title, "length": len(md), "markdown": md}
        print(json.dumps(result, indent=2))
        return

    output = md
    if not args.no_frontmatter:
        output = f"---\ntitle: {title}\nsource: {source or 'stdin'}\nconverted: {__import__('datetime').datetime.utcnow().isoformat()}\n---\n\n{md}"

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
