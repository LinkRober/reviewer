from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


class ConfigurationError(RuntimeError):
    """Raised when the LLM configuration is invalid."""


@dataclass(frozen=True)
class LLMConfig:
    model: str
    api_key: str
    base_url: str
    timeout: int


def default_env_path() -> Path:
    return Path.home() / ".config" / "lcr" / ".env"


def load_llm_config(
    *,
    model: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: int | None = None,
    env_path: Path | None = None,
) -> LLMConfig:
    config_path = env_path or default_env_path()
    load_dotenv(dotenv_path=config_path, override=False)

    resolved = {
        "LLM_MODEL_ID": model or os.getenv("LLM_MODEL_ID"),
        "LLM_API_KEY": api_key or os.getenv("LLM_API_KEY"),
        "LLM_BASE_URL": base_url or os.getenv("LLM_BASE_URL"),
    }
    missing = [name for name, value in resolved.items() if not value]
    if missing:
        names = ", ".join(missing)
        raise ConfigurationError(
            f"缺少模型配置: {names}。请设置环境变量或写入 {config_path}"
        )

    timeout_value = timeout if timeout is not None else os.getenv("LLM_TIMEOUT", "60")
    try:
        resolved_timeout = int(timeout_value)
    except (TypeError, ValueError) as error:
        raise ConfigurationError("LLM_TIMEOUT 必须是整数") from error
    if resolved_timeout <= 0:
        raise ConfigurationError("LLM_TIMEOUT 必须大于 0")

    return LLMConfig(
        model=resolved["LLM_MODEL_ID"],
        api_key=resolved["LLM_API_KEY"],
        base_url=resolved["LLM_BASE_URL"],
        timeout=resolved_timeout,
    )
