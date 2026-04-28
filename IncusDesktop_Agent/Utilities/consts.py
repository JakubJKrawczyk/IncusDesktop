
from enum import Enum



class ConfigVariables(Enum):
    DEFAULT_CONFIG_PATH = "/etc/IncusAgentsCli/config/incus_agent_config.json"
    DEFAULT_LOGS_PATH = "/var/log/incusDesktop/"
    DEFAULT_LOGS_INCUS = f"{DEFAULT_LOGS_PATH}incus.log"
    DEFAULT_LOGS_CLI = f"{DEFAULT_LOGS_PATH}cli.log"
    DEFAULT_LOGS_AGENT = f"{DEFAULT_LOGS_PATH}agents/"
