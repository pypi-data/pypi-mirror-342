from typing import Annotated

import typer
from mm_std import print_plain

from mm_strk.cli import cli_utils
from mm_strk.cli.cmd import node_cmd

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False, add_completion=False)


def version_callback(value: bool) -> None:
    if value:
        print_plain(f"mm-strk: {cli_utils.get_version()}")
        raise typer.Exit


@app.callback()
def main(_version: bool = typer.Option(None, "--version", callback=version_callback, is_eager=True)) -> None:
    pass


@app.command(name="node", help="Checks RPC URLs for availability and status")
def node_command(
    urls: Annotated[list[str], typer.Argument()],
    proxy: Annotated[str | None, typer.Option("--proxy", "-p", help="Proxy")] = None,
) -> None:
    node_cmd.run(urls, proxy)
