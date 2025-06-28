import yaml

def load_config(config_path="config.yaml"):
    """
    Load YAML configuration from the specified file.
    指定されたファイルからYAML設定を読み込む。
    """
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)
