"""
log_setup.py instantiates the in-built Python logging module, called from main.py.
"""

import logging.config
from pathlib import Path
from typing import Optional

import yaml


def setup_logging(
    default_path: Optional[Path], default_level: int = logging.INFO
) -> None:
    """
    Load logging configuration from YAML.
    """
    if not default_path:
        # project root/config/logging.yaml
        default_path = Path(__file__).resolve().parents[1] / "config/logging.yaml"

    config_path = default_path
    log_path = Path(__file__).resolve().parents[1] / "logs"
    log_path.mkdir(exist_ok=True)  # ensure logs/ exists

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        # update log file path dynamically
        config["handlers"]["file"]["filename"] = str(log_path / "app.log")
        logging.config.dictConfig(config)

    except FileNotFoundError as e:
        logging.basicConfig(level=default_level)
        logging.getLogger(__name__).warning("Logging config file not found: %s", e)

    except PermissionError as e:
        logging.basicConfig(level=default_level)
        logging.getLogger(__name__).warning("Permission error reading config: %s", e)

    except yaml.YAMLError as e:
        logging.basicConfig(level=default_level)
        logging.getLogger(__name__).warning("Invalid YAML in %s: %s", config_path, e)

    except (ValueError, TypeError) as e:
        logging.basicConfig(level=default_level)
        logging.getLogger(__name__).warning("Invalid logging configuration: %s", e)
