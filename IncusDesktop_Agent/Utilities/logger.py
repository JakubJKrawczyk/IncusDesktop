from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from xmlrpc.client import DateTime
from rich.console import Console

class LoggLevel(Enum):
    INFO="[bold][INFO][/bold]"
    WARNING="[yellow][WARNING][/yellow]"
    ERROR="[red][ERROR][/red]"


class Logger:

    def __init__(self, prefix: str, logs_path: str):

        self.prefix = prefix
        self.path = Path(logs_path)
        self.console = Console()

    def line(self, message: str, log_type: LoggLevel):
        ts = datetime.now().strftime("%Y-%m-%d:%H-%M-%S")
        log = f"{self.prefix}{log_type.value}[{ts}]:{message}\n"
        if self.path.exists():
            with self.path.open("a", encoding="utf-8") as f:
                f.write(log)
        else:
            self.console.print(f"{LoggLevel.ERROR.value}:Logs file doesn't exist... Run [bold]'incuscli setup init'[/bold] to check and create all missing files! Log printed only in console")
        self.console.print(log)