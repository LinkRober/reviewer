from typing import Any, Sequence

from openai import OpenAI

from .config import load_llm_config


class LLMError(RuntimeError):
    """Raised when the model request cannot be completed."""


class LLMAdaptor:
    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: int | None = None,
        client: Any | None = None,
    ):
        config = load_llm_config(
            model=model,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
        self.model = config.model
        self.client = client or OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
        )

    def think(self, messages: Sequence[dict[str, str]]) -> str:
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.responses.create(
                model=self.model,
                input=messages,
                stream=True,
            )
            collected_content = []
            for event in response:
                if event.type != "response.output_text.delta":
                    continue
                content = event.delta or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()
            return "".join(collected_content)
        except Exception as error:
            raise LLMError(f"调用 LLM API 失败: {error}") from error
