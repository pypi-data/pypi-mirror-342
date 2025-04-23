from typing import Any

import typer

from fitrequest.cli_utils import fit_cli_command, is_cli_command
from fitrequest.session import Session


class FitRequestBase:
    """
    The ``FitRequestBase`` class serves as the common ancestor for all classes that implement `fitrequest` methods.
    This class does not generate any methods on its own;
    instead, it provides a shared structure and declares attributes and methods that are not automatically generated.
    """

    session: Session

    fit_config: dict
    """Configuration used by fitrequest to generate the methods."""

    client_name: str = 'fitrequest'
    version: str = '{version}'
    base_url: str | None = None

    # Default username/password __init__ for backward compatibility with fitrequest 0.X.X
    def __init__(self, username: str | None = None, password: str | None = None) -> None:
        """Default __init__ method that allows username/password authentication."""
        if username or password:
            self.session.update(auth={'username': username, 'password': password})
        self.session.authenticate()

    def __getstate__(self) -> dict:
        """
        Invoked during the pickling process, this method returns the current state of the instance,
        specifically the contents of ``__dict__``.
        """
        return self.__dict__

    def __setstate__(self, state: dict) -> None:
        """
        Invoked during the unpickling process, this method updates `__dict__` with the provided state
        and re-authenticates the session, restoring any authentication that was lost during pickling.
        """
        self.__dict__.update(state)
        self.session.authenticate()

    @classmethod
    def cli_app(cls: Any) -> typer.Typer:
        """
        Set up a CLI interface using Typer.
        Instantiates the fitrequest client, registers all its methods as commands,
        and returns the typer the application.
        """
        app = typer.Typer()
        client = cls()

        for attr_name in dir(client):
            if is_cli_command(attr := getattr(client, attr_name)):
                app.command()(fit_cli_command(attr))
        return app

    @classmethod
    def cli_run(cls: Any) -> None:
        """
        Runs the typer application.
        """
        cls.cli_app()()
