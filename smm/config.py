from typing import Optional
from os import path

from betterconf import Config, field

BASE_DIR = path.dirname(__file__)

class AppConfig(Config):
    app_host = field("APP_HOST", default="0.0.0.0")
    app_port = field("APP_PORT", default=9999)

    vk_token = field("VK_TOKEN")


cfg: Optional[AppConfig] = None


def init() -> AppConfig:
    global cfg

    if cfg is None:
        cfg = AppConfig()
    return cfg