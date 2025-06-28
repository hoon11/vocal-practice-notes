from pydantic_settings import BaseSettings
from pydantic import Field

class WatcherConfig(BaseSettings):
    watch_folder: str = Field(..., description="감시 폴더")
    file_extension: str = Field(".wav", description="파일 확장자")

class TranscriberConfig(BaseSettings):
    model_size: str = Field(..., description="Whisper 모델 크기")
    transcripts_dir: str = Field(..., description="결과 저장 폴더")

class PitchConfig(BaseSettings):
    output_dir: str = Field(..., description="피치 분석 결과 폴더")

class AppConfig(BaseSettings):
    watcher: WatcherConfig
    transcriber: TranscriberConfig
    pitch: PitchConfig

    class Config:
        env_nested_delimiter = '__'  # PITCH__OUTPUT_DIR 오버라이드 가능!

def load_config(config_path=None) -> AppConfig:
    import yaml
    from pathlib import Path

    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    else:
        config_path = Path(config_path)
    with open(config_path, encoding="utf-8") as f:
        config_dict = yaml.safe_load(f)
    # BaseSettings 객체는 .parse_obj로 생성해야 환경변수 오버라이드가 동작
    config = AppConfig.parse_obj(config_dict)
    return config
