import yaml
from pathlib import Path
import os
import openai
from dotenv import load_dotenv


def load_yaml(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing config file: {path}")
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def merge_yaml(base: dict, override: dict):
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = merge_yaml(base[k], v)
        else:
            base[k] = v
    return base


def load_config(
    paths_file: str = "configs/paths.yaml",
    rag_config_file: str = "configs/dev.yaml",
):
    base_cfg = load_yaml(paths_file)
    override_cfg = load_yaml(rag_config_file)
    return merge_yaml(base_cfg, override_cfg)


def setup_openai(
    env_path: str = "configs/secrets.env",
):
    load_dotenv(env_path)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found!")
    openai.api_key = api_key
