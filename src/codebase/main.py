import time
from pathlib import Path

import typer

from codebase.app import AppState, app, get_state
from codebase.commands.init import init_command
from codebase.commands.search import search_command
from codebase.constants import (
    DEFAULT_IGNORE_PATTERNS,
)


@app.callback()
def main_callback(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed info"
    ),
):
    """Code semantic database for AI agents."""

    ctx.obj = AppState(verbose=verbose)


@app.command()
def init(
    ctx: typer.Context,
    paths: list[Path] = typer.Argument(..., help="Directories to index"),
    ignore: list[str] = typer.Option(
        None,
        "--ignore",
        "-i",
        help=f"Patterns to ignore (.gitignore style, default: {', '.join(DEFAULT_IGNORE_PATTERNS)})",
    ),
):
    """Index all code files from directories (clears and recreates collection)."""

    start_time = time.time()

    state = get_state(ctx)
    ignore_patterns = ignore if ignore else DEFAULT_IGNORE_PATTERNS

    init_command(state, paths, ignore_patterns)

    elapsed_time = time.time() - start_time
    typer.secho(f"Completed in {elapsed_time:.2f}s", fg=typer.colors.CYAN)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    top_k: int = typer.Option(5, "--top-k", "-k", help="Number of results"),
):
    """Search code. Returns JSON array, e.g. [{"rank": 1, "file_path": "src/main.py", "distance": 0.1234, "content": "..."}]."""

    search_command(query, top_k)


if __name__ == "__main__":
    app()
