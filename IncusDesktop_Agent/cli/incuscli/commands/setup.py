from pathlib import Path

import typer
from rich.console import Console

from Utilities.consts import ConfigVariables

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
    logs_path = Path(ConfigVariables.DEFAULT_LOGS_PATH)
    logs_incus_path = Path(ConfigVariables.DEFAULT_LOGS_INCUS)
    logs_cli_path = Path(ConfigVariables.DEFAULT_LOGS_CLI)
    logs_agent_path = Path(ConfigVariables.DEFAULT_LOGS_AGENT)

    #DEFAULT config file path
    if not config_path.exists():
        print("Config file not found... Creating new one.")
        config_path.mkdir(parents=True, exist_ok=False)
        print("Config file created successfully!")

    #DEFAULT logs path
    if not logs_path.exists():
        print("Logs folder not found... Creating new one.")
        logs_path.mkdir(parents=True, exist_ok=False)
        print("Logs folder created successfully!")

    #INCUS logs file path
    if not logs_incus_path.exists():
        print("Incus logs file not found... Creating new one.")
        logs_incus_path.touch(exist_ok=False)
        print("Incus logs file created!")

    #CLI logs file path
    if not logs_cli_path.exists():
        print("CLI logs file not found... Creating new one.")
        logs_cli_path.touch(exist_ok=False)
        print("CLI logs file created!")

    #AGENTS logs folder path
    if not logs_agent_path.exists():
        print("Agents logs folder not found... Creating new one.")
        logs_agent_path.mkdir(parents=True, exist_ok=False)
        print("Agents logs folder created!")

    print("Incus Desktop CLI initialized successfully! You can now add your first agent with 'incuscli agents add' ")