import time

from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError

from resume_cli.ai.mock import mock_response_for
from resume_cli.config import get_settings
from resume_cli.exceptions import AiCallError, ApiKeyMissingError
from resume_cli.logging_config import setup_logging

logger = setup_logging()


def call_ai(prompt: str, *, prompt_type: str, mock: bool = False) -> str:
    if mock:
        logger.info("Using mock AI response for %s", prompt_type)
        return mock_response_for(prompt_type)

    settings = get_settings()
    if not settings.api_key:
        raise ApiKeyMissingError(
            "未配置 DEEPSEEK_API_KEY。请在 .env 中设置 API Key，或使用 --mock 模式演示。"
        )

    client = OpenAI(api_key=settings.api_key, base_url=settings.base_url)

    try:
        logger.info("Calling AI model: %s", settings.model)
        start = time.perf_counter()
        response = client.chat.completions.create(
            model=settings.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        elapsed = time.perf_counter() - start
        logger.info("AI call completed in %.2fs", elapsed)
        content = response.choices[0].message.content
        if not content:
            raise AiCallError("AI 返回内容为空")
        return content
    except RateLimitError as exc:
        raise AiCallError(f"AI 调用失败: 请求频率超限 ({exc})") from exc
    except APIConnectionError as exc:
        raise AiCallError(f"AI 调用失败: 网络连接错误 ({exc})") from exc
    except APIStatusError as exc:
        raise AiCallError(f"AI 调用失败: API 返回错误 ({exc.message})") from exc
    except AiCallError:
        raise
    except Exception as exc:
        raise AiCallError(f"AI 调用失败: {exc}") from exc
