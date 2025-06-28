"""
modules/config_loader.py

YAML config loader with nested models and validation (pydantic).
YAML設定ファイルのネストモデルとバリデーション対応ローダー。
"""

import os
import yaml
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

class WatcherConfig(BaseModel):
    watch_folder: str = Field(..., description="감시 폴더 / 監視フォルダ")
    file_extension: str = Field(".wav", description="파일 확장자 / ファイル拡張子")

class TranscriberConfig(BaseModel):
    model_size: str = Field(..., description="Whisper 모델 크기 / Whisperモデルサイズ")
    transcripts_dir: str = Field(..., description="결과 저장 폴더 / 出力フォルダ")

class PitchConfig(BaseModel):
    output_dir: str = Field(..., description="피치 분석 결과 폴더 / ピッチ分析結果出力")

class AppConfig(BaseModel):
    watcher: WatcherConfig
    transcriber: TranscriberConfig
    pitch: PitchConfig

def load_config(config_path=None) -> AppConfig:
    """
    Load configuration from YAML and validate.
    YAMLから設定を読み込みバリデーションする
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    else:
        config_path = Path(config_path)

    try:
        with open(config_path, encoding="utf-8") as f:
            config_dict = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Config load/parsing error: {e}")
        raise

    try:
        config = AppConfig(**config_dict)
    except ValidationError as e:
        logger.error(f"Config validation error:\n{e}")
        raise

    return config
