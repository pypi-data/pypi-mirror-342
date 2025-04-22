from __future__ import annotations
import typing as t
from typer import Typer, Context
from rich import print


def shell(welcome: t.Callable | None = None, context: dict | None = None) -> t.Callable:
    context = context if context is not None else {}

    def _shell(ctx: Context):
        try:
            from IPython import start_ipython
            from IPython.terminal.ipapp import load_default_config

            config = load_default_config()
            if welcome:
                config.InteractiveShell.banner1 = welcome()
            start_ipython(argv=[], config=config, user_ns=context)
        except ImportError:
            print("[bold red]IPython is not installed![/bold red]")
            ctx.exit(1)

    return Typer(command=_shell, help="Start Python interactive shell")
