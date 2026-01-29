from dataclasses import dataclass

import typer


@dataclass
class AppState:
    verbose: bool = False


def get_state(ctx: typer.Context) -> AppState:
    return ctx.obj


app = typer.Typer()
