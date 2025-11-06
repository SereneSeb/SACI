"""
This script scans Markdown files and adds a YAML front‑matter header to
any note that looks like a "concept stub". A concept stub is identified
by the presence of a first‑level heading on the first line and a
"*Concept Category: …*" line near the top of the file. If a file already
contains YAML front matter (delimited by ``---`` at the beginning), it
will be skipped. The generated YAML header includes the note's title,
its concept category and a default list of tags (``concept`` and
``stub``). Running this script repeatedly is safe — files with
existing front matter are ignored.

Usage:
    python add_yaml_headers.py [directory]

If no directory is provided, the current working directory is used.

Example:
    # Add YAML headers to all concept stubs in the "Concept Notes" folder
    python add_yaml_headers.py "Concept Notes"
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import Iterable, Optional


CONCEPT_CATEGORY_PATTERN = re.compile(r"\*Concept\s+Category:\s*(.*?)\s*\*", re.IGNORECASE)


def find_markdown_files(root: Path) -> Iterable[Path]:
    """Yield all Markdown files under ``root`` recursively."""
    for path in root.rglob("*.md"):
        if path.is_file():
            yield path


def extract_metadata(lines: list[str]) -> Optional[tuple[str, str]]:
    """Return a tuple of (title, concept_category) if present, otherwise None.

    The function expects the first non‑empty line to begin with a '# '
    followed by the note title. It then searches the next few lines for a
    line matching ``*Concept Category: …*``.
    """
    # Skip any leading blank lines
    idx = 0
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    if idx >= len(lines):
        return None
    heading = lines[idx].lstrip()
    if not heading.startswith('# '):
        return None
    title = heading[2:].strip()
    # Search for concept category within the next few lines
    for line in lines[idx + 1: idx + 6]:
        match = CONCEPT_CATEGORY_PATTERN.search(line)
        if match:
            category = match.group(1).strip()
            return title, category
    return None


def has_front_matter(text: str) -> bool:
    """Return True if the provided text begins with YAML front matter."""
    stripped = text.lstrip()
    return stripped.startswith('---')


def add_header_to_file(path: Path) -> bool:
    """Add YAML header to the given file if it qualifies as a concept stub.

    Returns True if the file was modified, False otherwise.
    """
    original = path.read_text(encoding='utf-8')
    if has_front_matter(original):
        return False
    lines = original.splitlines()
    meta = extract_metadata(lines)
    if not meta:
        return False
    title, category = meta
    header_lines = [
        '---',
        f'title: "{title}"',
        f'concept_category: "{category}"',
        'tags:',
        '  - concept',
        '  - stub',
        '---',
        ''  # blank line to separate header from body
    ]
    header_text = "\n".join(header_lines)
    # Write new content
    path.write_text(header_text + original, encoding='utf-8')
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Add YAML headers to concept stub notes.")
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan (default: current directory)')
    args = parser.parse_args()
    root = Path(args.directory).resolve()
    if not root.exists():
        parser.error(f"The specified directory {root} does not exist")
    modified_count = 0
    for md_file in find_markdown_files(root):
        if add_header_to_file(md_file):
            modified_count += 1
            print(f"Added header to {md_file.relative_to(root)}")
    if modified_count == 0:
        print("No concept stubs were modified.")
    else:
        print(f"Added YAML headers to {modified_count} file(s).")


if __name__ == '__main__':
    main()