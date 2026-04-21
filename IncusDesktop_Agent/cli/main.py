import typer

from cli.commands.agents.agents import agentApp

app = typer.Typer(
    name="incuscli",
    help="Incus-Agent Agent API",
    no_args_is_help=True
)
app.add_typer(agentApp, name="agents")



if __name__ == "__main__":
    typer.run(app)
