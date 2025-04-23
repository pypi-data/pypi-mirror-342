from typing import Annotated

import typer

from jaraco.ui.main import main

from . import github


@main
def run(
    name: str,
    value: str,
    project: Annotated[
        github.Repo, typer.Option(parser=github.Repo)
    ] = github.Repo.detect(),
):
    project.add_secret(name, value)
