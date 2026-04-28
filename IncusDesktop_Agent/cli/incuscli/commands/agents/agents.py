import typer

from rich.console import Console

agentApp = typer.Typer(
    help="Manage agents"
)

@agentApp.command("list")
def list_():
    pass