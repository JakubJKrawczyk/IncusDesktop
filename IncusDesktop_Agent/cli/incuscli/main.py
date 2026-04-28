import typer

from incuscli.commands.agents.agents import agentApp
from incuscli.commands.setup import setupApp

app = typer.Typer(
    name="incuscli",
    help="Incus-Agent Agent API",
    no_args_is_help=True
)
app.add_typer(agentApp, name="agents")
app.add_typer(setupApp, name="setup")


if __name__ == "__main__":
    typer.run(app)
