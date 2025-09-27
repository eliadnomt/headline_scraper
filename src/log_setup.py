import logging.config
from pathlib import Path

import yaml


def setup_logging(default_path: Path = None, default_level: int = logging.INFO) -> None:
	"""
	Load logging configuration from YAML.
	"""
	if default_path is None:
		# project root/config/logging.yaml
		default_path = Path(__file__).resolve().parents[1] / "config/logging.yaml"

	config_path = default_path
	log_path = Path(__file__).resolve().parents[1] / "logs"
	log_path.mkdir(exist_ok=True)  # ensure logs/ exists

	try:
		with open(config_path, "r") as f:
			config = yaml.safe_load(f)
			config["handlers"]["file"]["filename"] = str(log_path / "app.log")
		logging.config.dictConfig(config)
	except Exception as e:
		# Fallback: simple console logging
		logging.basicConfig(level=default_level)
		logging.getLogger(__name__).warning(
			"Failed to load logging config %s: %s", config_path, e
		)
