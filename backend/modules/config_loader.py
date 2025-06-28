import os
import yaml
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

class AppConfig(BaseModel):
    whisper_model: str = Field(..., description="Whisper model name / Whisperモデル名")
    use_whisper: bool = Field(True, description="Enable Whisper transcription / Whisper変換有効化")
    watch_folder: str = Field(..., description="Folder to watch for .wav files / 監視対象フォルダ")
    output_folder: str = Field(..., description="Folder to save output files / 出力ファイル保存先")
    log_level: str = Field("INFO", description="Logging level / ログレベル")

    class Config:
        extra = "forbid"

def load_config(config_path=None) -> AppConfig:
    """
    Load configuration from YAML, validate with AppConfig, override by environment variables.
    YAMLから設定を読み込み、AppConfigでバリデーションし、環境変数で上書き。
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    else:
        config_path = Path(config_path)
    
    try:
        with open(config_path, encoding="utf-8") as f:
            config_dict = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found at: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing failed: {e}")
        raise

    # pydantic v2 호환: model_fields와 annotation 사용
    for field in AppConfig.model_fields:
        env_key = field.upper()
        if env_key in os.environ:
            val = os.environ[env_key]
            field_info = AppConfig.model_fields[field]
            field_type = field_info.annotation
            if field_type is bool:
                val = val.lower() in ("1", "true", "yes")
            elif field_type is int:
                val = int(val)
            config_dict[field] = val

    try:
        config = AppConfig(**config_dict)
    except ValidationError as e:
        logger.error(f"Config validation error:\n{e}")
        raise

    return config

if __name__ == "__main__":
    config = load_config()
    print(config)
