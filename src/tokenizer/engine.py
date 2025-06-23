# src/tokenizer/engine.py

import tiktoken
from pathlib import Path
from dataclasses import dataclass
from typing import Generator, Optional, Callable
from gitignore_parser import parse_gitignore

from .utils import is_binary_path

@dataclass
class FileReport:
    """A dataclass to hold the analysis report for a single file."""
    path: str
    status: str
    token_count: Optional[int] = None

def _walk_and_process(
    current_path: Path,
    root_path: Path,
    matcher: Optional[Callable[[Path], bool]],
    exclude_patterns: list[str],
    encoding,
) -> Generator[FileReport, None, None]:
    """
    A custom recursive directory walker that prunes ignored directories.
    """
    for path in current_path.iterdir():
        # First, check if the path itself should be ignored. This is key for pruning.
        if matcher and matcher(path):
            continue

        # Skip dot-based directories and files (like .git, .vscode)
        if path.name.startswith('.'):
            continue

        relative_path_str = str(path.relative_to(root_path))

        if path.is_dir():
            # Recursively walk into subdirectories
            yield from _walk_and_process(path, root_path, matcher, exclude_patterns, encoding)
        elif path.is_file():
            # Process files
            if any(path.match(pattern) for pattern in exclude_patterns):
                yield FileReport(path=relative_path_str, status="skipped_excluded")
                continue

            if is_binary_path(path):
                yield FileReport(path=relative_path_str, status="skipped_binary")
                continue

            try:
                content = path.read_text(encoding="utf-8")
                tokens = encoding.encode(content)
                yield FileReport(
                    path=relative_path_str,
                    status="processed",
                    token_count=len(tokens)
                )
            except UnicodeDecodeError:
                yield FileReport(path=relative_path_str, status="error_decoding")
            except Exception as e:
                yield FileReport(path=relative_path_str, status=f"error_general: {e}")

def process_directory(
    root_path: Path,
    exclude_patterns: list[str]
) -> Generator[FileReport, None, None]:
    """
    Initializes matchers and starts the pruned directory walk.
    """
    encoding = tiktoken.get_encoding("cl100k_base")

    gitignore_path = root_path / ".gitignore"
    matcher = parse_gitignore(gitignore_path, root_path) if gitignore_path.is_file() else None

    # Start the custom walker from the root
    yield from _walk_and_process(root_path, root_path, matcher, exclude_patterns, encoding)
