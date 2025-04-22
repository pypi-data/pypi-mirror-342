from __future__ import annotations
import typing as t
from typer import Typer, Option, Argument, Context, echo

__version__ = "1.4.0"
__all__ = ["Argument", "Option", "Cli"]


class Cli:
    _app: Typer
    context: dict[str, t.Any]

    def __init__(self, service, **context):
        self.service = service
        self._app = Typer(
            name="cli",
            no_args_is_help=True,
            help=f"{self.service.__name__.title()} CLI",
        )
        self.context = {"cli": self, "service": service, **context}

    def add_command(self, name: str, command: t.Callable, *, nargs: int | None = None):
        if nargs == -1:
            def wrapper(*args: str):
                return command(list(args))

            self._app.command(name=name)(wrapper)
        else:
            self._app.command(name=name)(command)

    def add_subcommand(self, name: str, commands: dict[str, t.Callable], help_text: str = ""):
        sub_app = Typer(name=name, help=help_text)
        for command_name, command in commands.items():
            sub_app.command(name=command_name)(command)
        self._app.add_typer(sub_app, name=name)

    def start(self):
        return self._app()

    @property
    def app(self) -> Typer:
        return self._app
