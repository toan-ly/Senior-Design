import yaml
from pathlib import Path
import os
import openai
from dotenv import load_dotenv


def load_paths_config(
    path: str = "configs/paths.yaml",
):
    cfg_path = Path(path)
    if not cfg_path.exists():
        raise FileNotFoundError(f"Missing config file: {path}")
    return yaml.safe_load(cfg_path.read_text(encoding="utf-8"))


def setup_openai(
    env_path: str = "configs/secrets.env",
):
    load_dotenv(env_path)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found!")
    openai.api_key = api_key
