# modules/config_loader.py
import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_config(config_path=None):
    """
    Load configuration from a YAML file.
    If no path is provided, loads from default config path.
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"

    try:
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found at: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing failed: {e}")
        raise