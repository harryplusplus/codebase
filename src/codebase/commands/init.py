from pathlib import Path

import pathspec
import typer

from codebase.app import AppState
from codebase.constants import COLLECTION_NAME
from codebase.db import get_client, get_collection


def init_command(
    state: AppState, paths: list[Path], ignore_patterns: list[str]
):
    ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    client = get_client()

    try:
        client.delete_collection(COLLECTION_NAME)
        typer.secho("✓ Cleared existing collection.", fg=typer.colors.YELLOW)
    except Exception:
        pass

    collection = get_collection(client)

    total_files = 0
    for path in paths:
        files = _get_files(state, path, ignore_spec)
        for file in files:
            content = file.read_text(encoding="utf-8")
            doc_id = str(file)

            collection.add(
                documents=[content],
                metadatas=[{"file_path": str(file)}],
                ids=[doc_id],
            )

            if state.verbose:
                typer.echo(f"  Indexed {doc_id}")

        total_files += len(files)
        typer.secho(
            f"  Indexed {len(files)} files from {path}", fg=typer.colors.BLUE
        )

    typer.echo("")
    typer.secho(f"✓ Total: {total_files} files indexed", fg=typer.colors.GREEN)


def _get_files(
    state: AppState, path: Path, ignore_spec: pathspec.PathSpec
) -> list[Path]:
    files: list[Path] = []
    for file in path.rglob("*"):
        if not file.is_file():
            continue

        relative = file.relative_to(path)
        if ignore_spec.match_file(relative):
            if state.verbose:
                typer.secho(f"  Ignoring {relative}", fg=typer.colors.YELLOW)
            continue

        files.append(file)

    return files
