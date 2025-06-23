import click
from pathlib import Path
from collections import Counter

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

from .engine import process_directory, FileReport

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
def cli(path: Path, verbose: bool, exclude: tuple[str]):
    """
    Analyzes a directory and reports the total token count of its text files.

    PATH: The path to the directory to analyze.
    """
    console = Console()
    
    reports: list[FileReport] = []
    
    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Processing files...", total=None)
        # The generator allows for responsive progress updates
        for report in process_directory(path, list(exclude)):
            reports.append(report)
            progress.update(task, advance=1, description=f"[cyan]Processing... [bold]{report.path}[/bold]")

    processed_reports = [r for r in reports if r.status == "processed"]
    status_counts = Counter(r.status for r in reports)
    total_tokens = sum(r.token_count for r in processed_reports if r.token_count)

    # --- Summary Panel ---
    summary_table = Table.grid(expand=True)
    summary_table.add_column(justify="left")
    summary_table.add_column(justify="right")
    
    summary_table.add_row("[bold cyan]Total Tokens[/bold cyan]", f"[bold yellow]{total_tokens:,}[/bold yellow]")
    summary_table.add_row("Files Processed", f"{status_counts['processed']:,}")
    summary_table.add_row("Files Skipped (Ignored by .gitignore)", f"{status_counts.get('skipped_ignored', 0):,}")
    summary_table.add_row("Files Skipped (Excluded by pattern)", f"{status_counts.get('skipped_excluded', 0):,}")
    summary_table.add_row("Files Skipped (Binary)", f"{status_counts.get('skipped_binary', 0):,}")
    summary_table.add_row("Files with Errors (Decoding)", f"{status_counts.get('error_decoding', 0):,}")
    
    console.print(Panel(summary_table, title="[bold]Analysis Summary[/bold]", border_style="green"))

    # --- Verbose Output Table ---
    if verbose:
        table = Table(title="[bold]Detailed File Report[/bold]", show_lines=True)
        table.add_column("File Path", style="cyan", no_wrap=True)
        table.add_column("Token Count", justify="right", style="magenta")
        table.add_column("Status", justify="left", style="green")
        
        for report in sorted(reports, key=lambda r: r.path):
            token_str = f"{report.token_count:,}" if report.token_count is not None else "N/A"
            table.add_row(report.path, token_str, report.status)
        
        console.print(table)
