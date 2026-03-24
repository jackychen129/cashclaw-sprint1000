from __future__ import annotations

import logging
import os
from pathlib import Path

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


def _load_dotenv_from_known_paths() -> None:
    """Load .env from repo root / service dir / cwd so uvicorn works without Docker."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    here = Path(__file__).resolve()
    service_dir = here.parent.parent
    repo_root = service_dir.parent

    for candidate in (repo_root / ".env", service_dir / ".env", Path.cwd() / ".env"):
        if candidate.is_file():
            load_dotenv(candidate, override=True)
            logger.info("Loaded environment file: %s", candidate)
            return

    searched = {repo_root / ".env", service_dir / ".env", Path.cwd() / ".env"}
    logger.warning(
        "No .env file found in searched paths %s; using process environment only",
        sorted(str(p) for p in searched),
    )


_load_dotenv_from_known_paths()


def _env_str(primary: str, *fallbacks: str, default: str = "") -> str:
    for key in (primary, *fallbacks):
        val = os.getenv(key)
        if val is not None and val.strip() != "":
            return val.strip()
    return default


ONLINE_BASE_DEFAULT = "https://api.openai.com/v1"


class Settings(BaseModel):
    app_env: str = Field(default_factory=lambda: _env_str("APP_ENV", default="development"))
    log_level: str = Field(default_factory=lambda: _env_str("LOG_LEVEL", default="INFO"))
    port: int = Field(default_factory=lambda: int(_env_str("PORT", default="8080") or "8080"))

    local_model_base_url: str = Field(
        default_factory=lambda: _env_str(
            "LOCAL_MODEL_BASE_URL", default="http://localhost:11434/v1"
        )
    )
    local_model_name: str = Field(
        default_factory=lambda: _env_str("LOCAL_MODEL_NAME", default="llama3.1")
    )
    local_model_api_key: str = Field(
        default_factory=lambda: _env_str(
            "LOCAL_MODEL_API_KEY", default="local-not-required"
        )
    )

    # OpenAI-compatible online API (DashScope, OpenAI, proxies, etc.)
    online_model_base_url: str = Field(
        default_factory=lambda: _env_str(
            "ONLINE_MODEL_BASE_URL",
            "OPENAI_BASE_URL",
            default=ONLINE_BASE_DEFAULT,
        )
    )
    online_model_name: str = Field(
        default_factory=lambda: _env_str(
            "ONLINE_MODEL_NAME",
            "OPENAI_MODEL",
            default="gpt-4o-mini",
        )
    )
    online_model_api_key: str = Field(
        default_factory=lambda: _env_str(
            "ONLINE_MODEL_API_KEY",
            "OPENAI_API_KEY",
            default="",
        )
    )

    model_routing_policy: str = Field(
        default_factory=lambda: _env_str(
            "MODEL_ROUTING_POLICY", default="quality_first"
        )
    )


settings = Settings()
