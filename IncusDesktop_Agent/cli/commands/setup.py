from pathlib import Path

import typer
from rich.console import Console
from cli.utility.consts import DEFAULT_CONFIG_PATH

console = Console()
app = typer.Typer()

@app.command("init")
def setup():
    print("-"*40)
    print("Welcome in IncusCLI - Agent for incus desktop application. Let's begin!")\
    print("-"*40)
    print("")
    config_path =  Path(DEFAULT_CONFIG_PATH)
    if not config_path.exists():
        print("Config file not found... Creating new one.")

