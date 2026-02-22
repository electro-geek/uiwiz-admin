"""
Config reader: same logic as uiwiz-backend.
Reads config.properties; env vars override (e.g. DB_NAME, DB_USER, ...).
"""
import os
from pathlib import Path


def _env_key(key: str) -> str:
    return key.replace(".", "_").upper()


def read_config(config_path=None):
    if config_path is None:
        base = Path(__file__).resolve().parent.parent
        config_path = base / "config.properties"
    config = {}
    if config_path.exists():
        with open(config_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip()
    return config


def get_config():
    data = read_config()
    return type("Config", (), {
        "get": lambda self, key, default=None: os.environ.get(_env_key(key), data.get(key, default))
    })()
