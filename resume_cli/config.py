import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"


@dataclass(frozen=True)
class Settings:
    api_key: str | None
    base_url: str
    model: str
    log_level: str


def get_settings() -> Settings:
    return Settings(
        api_key=os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL),
        model=os.getenv("DEEPSEEK_MODEL", DEFAULT_MODEL),
        log_level=os.getenv("LOG_LEVEL", "WARNING").upper(),
    )
