# src/tokenizer/main.py

import click
from pathlib import Path
from collections import Counter, defaultdict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

from .engine import process_directory, FileReport

def build_tree_string(paths: list[str]) -> str:
    """Builds a directory tree string from a list of file paths."""
    tree = defaultdict(list)
    for path in sorted(paths):
        parts = Path(path).parts
        if len(parts) > 1:
            parent = "/".join(parts[:-1])
            tree[parent].append(parts[-1])
        else:
            tree["."].append(parts[0])

    lines = ["."]

    def add_items(items, prefix=""):
        for i, item in enumerate(sorted(items)):
            connector = "├──" if i < len(items) - 1 else "└──"
            lines.append(f"{prefix}{connector} {item}")
            if item in tree:
                new_prefix = prefix + ("│   " if i < len(items) - 1 else "    ")
                add_items(tree[item], new_prefix)

    # Create a list of top-level directories and files
    top_level_items = sorted([p for p in tree["."]] + [d.split('/')[0] for d in tree if '/' not in d])

    # This is a bit complex to handle both files and dirs at root correctly
    processed_top_level = []
    final_top_level_items = []
    for item in top_level_items:
        if item not in processed_top_level:
            is_dir = any(p.startswith(item + '/') for p in paths)
            final_top_level_items.append(item + '/' if is_dir else item)
            processed_top_level.append(item)

    add_items(sorted(list(set(final_top_level_items))))

    return "\n".join(lines)


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path),
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Enable verbose output, showing a detailed table of all files.",
)
@click.option(
    "--exclude",
    multiple=True,
    help="A glob pattern to exclude files. Can be used multiple times.",
)
@click.option(
    "-o", "--create-output-file",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="Create a single output file with a directory tree and all processed file contents.",
)
def cli(path: Path, verbose: bool, exclude: tuple[str], create_output_file: Path):
    """
    Analyzes a directory and reports the total token count of its text files.

    PATH: The path to the directory to analyze.
    """
    console = Console()

    reports: list[FileReport] = []

    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Processing files...", total=None)
        for report in process_directory(path, list(exclude)):
            reports.append(report)
            progress.update(task, advance=1, description=f"[cyan]Processing... [bold]{report.path}[/bold]")

    # --- Filtering for Reporting and File Output ---
    processed_reports = [r for r in reports if r.status == 'processed' and r.token_count is not None and r.token_count > 0]

    # --- Console Output ---
    status_counts = Counter(r.status for r in reports)
    total_tokens = sum(r.token_count for r in processed_reports)

    summary_table = Table.grid(expand=True)
    summary_table.add_column(justify="left")
    summary_table.add_column(justify="right")

    summary_table.add_row("[bold cyan]Total Tokens[/bold cyan]", f"[bold yellow]{total_tokens:,}[/bold yellow]")
    summary_table.add_row("Files Processed", f"{len(processed_reports):,}")
    summary_table.add_row("Files Skipped (Ignored by .gitignore)", f"{status_counts.get('skipped_ignored', 0):,}")
    summary_table.add_row("Files Skipped (Excluded by pattern)", f"{status_counts.get('skipped_excluded', 0):,}")
    summary_table.add_row("Files Skipped (Binary)", f"{status_counts.get('skipped_binary', 0):,}")
    summary_table.add_row("Files with Errors (Decoding)", f"{status_counts.get('error_decoding', 0):,}")

    console.print(Panel(summary_table, title="[bold]Analysis Summary[/bold]", border_style="green"))

    if verbose:
        table = Table(title="[bold]Detailed File Report[/bold]", show_lines=True)
        table.add_column("File Path", style="cyan", no_wrap=True)
        table.add_column("Token Count", justify="right", style="magenta")
        table.add_column("Status", justify="left", style="green")

        for report in sorted(reports, key=lambda r: r.path):
            token_str = f"{report.token_count:,}" if report.token_count is not None else "N/A"
            table.add_row(report.path, token_str, report.status)

        console.print(table)

    # --- File Output Logic ---
    if create_output_file:
        console.print(f"\n[bold yellow]Creating output file at:[/] [green]{create_output_file}[/]")

        processed_paths = [r.path for r in processed_reports]
        tree_string = build_tree_string(processed_paths)

        try:
            with create_output_file.open("w", encoding="utf-8") as f:
                f.write("Directory Tree of Processed Files:\n")
                f.write("===================================\n")
                f.write(tree_string)
                f.write("\n\n===================================\n\n")
                f.write("File Contents:\n")
                f.write("==============\n\n")

                for report in sorted(processed_reports, key=lambda r: r.path):
                    full_source_path = path / report.path
                    try:
                        content = full_source_path.read_text(encoding="utf-8")
                        file_size = full_source_path.stat().st_size

                        header = f"--- File: {report.path} | Size: {file_size} bytes | Tokens: {report.token_count} ---\n"
                        f.write(header)
                        f.write(content)
                        f.write("\n\n--- End of File ---\n\n\n")
                    except Exception as e:
                        f.write(f"--- Error reading file {report.path}: {e} ---\n\n")

            console.print("[bold green]✅ Output file created successfully.[/]")
        except Exception as e:
            console.print(f"[bold red]❌ Error creating output file: {e}[/]")
