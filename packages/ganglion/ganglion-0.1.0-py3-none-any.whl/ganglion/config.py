from os.path import expandvars
import logging
import tomllib
from pathlib import Path
from typing_extensions import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator


ExpandVarsStr = Annotated[str, AfterValidator(expandvars)]


log = logging.getLogger("ganglion")


class ConfigError(Exception):
    pass


class Server(BaseModel):
    base_url: ExpandVarsStr = "http://127.0.0.1:8080"
    domain: ExpandVarsStr = "127.0.0.1:8080"
    app_url_format: ExpandVarsStr
    app_websocket_url: ExpandVarsStr


class Templates(BaseModel):
    root: ExpandVarsStr = "./templates"


class Static(BaseModel):
    root: ExpandVarsStr = "./static"
    url: ExpandVarsStr = "/static"


class DB(BaseModel):
    url: ExpandVarsStr


class Config(BaseModel):
    server: Server
    templates: Templates
    static: Static
    db: DB
    extends: ExpandVarsStr = ""


def load_config(config_path: str | Path) -> Config:
    """Load TOML config file.

    Args:
        config_path: Path to config.

    Raises:
        ConfigError: If the file doesn't exist.
        ConfigError: If the TOML failed to parse.

    Returns:
        Config object.
    """
    try:
        with Path(config_path).open("rb") as config_file:
            config_data = tomllib.load(config_file)
    except FileNotFoundError:
        raise ConfigError(f"Config file {str(config_path)!r} not found") from None
    except Exception as error:
        raise ConfigError(
            f"Failed to parse config file {str(config_path)!r}; {error}"
        ) from None

    log.info(f"Loaded config from {str(config_path)!r}")

    config = Config(**config_data)
    return config
