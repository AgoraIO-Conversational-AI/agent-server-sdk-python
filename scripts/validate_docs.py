import ast
import pathlib
import re
import sys
from typing import List, Optional

ROOT = pathlib.Path.cwd()
BANNED_PATTERNS = [
    re.compile(r'\{\{\s*owner\s*\}\}'),
    re.compile(r'\{\{\s*repo\s*\}\}'),
    re.compile(r'from agora-agent-server-sdk'),
]
# `concepts` and `reference` snippets must declare whether they are runnable examples or API fragments.
CODE_BLOCK_RE = re.compile(
    r'(?:(<!--\s*snippet:\s*(executable|fragment)\s*-->)[ \t]*\n)?```python\n([\s\S]*?)```'
)


def collect_markdown_files() -> List[pathlib.Path]:
    return [ROOT / 'README.md', *sorted((ROOT / 'docs').rglob('*.md'))]


def is_annotated_section(file: pathlib.Path) -> bool:
    relative = file.relative_to(ROOT).as_posix()
    return '/docs/concepts/' in f'/{relative}' or '/docs/reference/' in f'/{relative}'


def snippet_mode(code: str, annotation: Optional[str]) -> str:
    if annotation == 'fragment':
        return 'fragment'
    if annotation == 'executable':
        return 'executable'
    return 'executable'


MARKDOWN_FILES = collect_markdown_files()

failures: List[str] = []
snippet_count = 0
fragment_count = 0

for file in MARKDOWN_FILES:
    content = file.read_text(encoding='utf-8')

    for pattern in BANNED_PATTERNS:
        if pattern.search(content):
            failures.append(f"{file.relative_to(ROOT)} contains banned pattern: {pattern.pattern}")

    for match in CODE_BLOCK_RE.finditer(content):
        annotation = match.group(2)
        code = match.group(3)
        if is_annotated_section(file) and not annotation:
            failures.append(f"{file.relative_to(ROOT)} contains an unannotated python snippet")
            continue

        mode = snippet_mode(code, annotation)
        if mode == 'fragment':
            fragment_count += 1
            continue

        snippet_count += 1
        try:
            ast.parse(code, filename=str(file))
        except SyntaxError as exc:
            failures.append(f"{file.relative_to(ROOT)}:{exc.lineno}: {exc.msg}")

if snippet_count == 0:
    failures.append('No Python code blocks found in README/docs markdown.')

if failures:
    print('Documentation validation failed:', file=sys.stderr)
    for failure in failures:
        print(f'- {failure}', file=sys.stderr)
    raise SystemExit(1)

print(
    f'Validated {snippet_count} executable and {fragment_count} fragment Python snippets across '
    f'{len(MARKDOWN_FILES)} markdown files.'
)
