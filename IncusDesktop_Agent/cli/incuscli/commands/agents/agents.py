import typer

from rich.console import Console

agentApp = typer.Typer(
    help="Manage agent"
)

@agentApp.command("status")
def status_():
    pass

@agentApp.command("logs")
def logs_():
    pass

@agentApp.command("init")
def init_():
    pass
