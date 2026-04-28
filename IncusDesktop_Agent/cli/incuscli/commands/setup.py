from pathlib import Path

import typer
from rich.console import Console

from incuscli.utility.consts import ConfigVariables

console = Console()
setupApp = typer.Typer(
    help="Init options"
)

@setupApp.command("init")
def setup():
    print("-"*40)
    print("Welcome in IncusCLI - Agent for incus desktop application. Let's begin!")
    print("-"*40)
    print("")
    config_path =  Path(ConfigVariables.DEFAULT_CONFIG_PATH.value)
    if not config_path.exists():
        print("Config file not found... Creating new one.")
        config_path.mkdir(parents=True, exist_ok=False)
        print("")
