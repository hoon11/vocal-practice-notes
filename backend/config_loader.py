import yaml
from pathlib import Path

# Load configuration from config.yaml
# 設定ファイル(config.yaml)を読み込みます
CONFIG_PATH = Path(__file__).parent / "config.yaml"

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
