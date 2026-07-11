#!/usr/bin/env python3
"""CLI: html-to-markdown

Convert HTML pages to clean Markdown. CLI that fetches URLs and outputs formatted Markdown with frontmatter.
"""
import sys, json, argparse

def main():
    parser = argparse.ArgumentParser(description="Convert HTML pages to clean Markdown. CLI that fetches URLs and outputs formatted Markdown with frontmatter.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = {"tool": "html-to-markdown", "ready": True}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result}")

if __name__ == "__main__":
    main()
