"""LLM 客户端封装，支持 MiniMax / Anthropic / OpenAI 兼容接口"""

import os

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def get_anthropic_client() -> "Anthropic | None":
    """获取 Anthropic 兼容客户端 (MiniMax / Anthropic 官方)"""
    if not ANTHROPIC_AVAILABLE:
        return None

    api_key = (
        os.environ.get("MINIMAX_API_KEY") or
        os.environ.get("ANTHROPIC_API_KEY")
    )
    if not api_key:
        return None

    base_url = (
        os.environ.get("MINIMAX_BASE_URL") or
        os.environ.get("ANTHROPIC_BASE_URL") or
        "https://api.anthropic.com"
    )

    return Anthropic(
        api_key=api_key,
        base_url=base_url,
    )


def get_openai_client() -> "OpenAI | None":
    """获取 OpenAI 兼容客户端（如 ollama）"""
    if not OPENAI_AVAILABLE:
        return None
    api_key = os.environ.get("OPENAI_API_KEY", "dummy")
    base_url = os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


def call_llm(
    prompt: str,
    model: str | None = None,
    max_tokens: int = 4096,
    json_mode: bool = False,
    system: str | None = None,
) -> str:
    """
    调用 LLM，统一接口

    Args:
        prompt: 用户输入提示
        model: 模型名称，默认使用 MINIMAX_MODEL 环境变量
        max_tokens: 最大 token 数
        json_mode: 是否输出 JSON
        system: 系统提示

    Returns:
        LLM 响应文本
    """
    # 默认模型
    if model is None:
        model = os.environ.get("MINIMAX_MODEL", "MiniMax-M2.7")

    # 构建用户消息
    messages = [{"role": "user", "content": prompt}]

    # 优先使用 Anthropic 兼容接口 (MiniMax / Anthropic)
    client = get_anthropic_client()
    if client:
        kwargs: dict = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system

        response = client.messages.create(**kwargs)

        # 处理 thinking 输出 (MiniMax-M2.7)
        result_parts = []
        for block in response.content:
            if block.type == "thinking":
                result_parts.append(f"[Thinking]: {block.thinking}")
            elif block.type == "text":
                result_parts.append(block.text)

        return "\n".join(result_parts)

    # 降级到 OpenAI 兼容接口
    client = get_openai_client()
    if client:
        # OpenAI 用 role="system" 消息
        oai_messages = []
        if system:
            oai_messages.append({"role": "system", "content": system})
        oai_messages.append({"role": "user", "content": prompt})

        extra_kwargs = {}
        if json_mode:
            extra_kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(
            model=model,
            messages=oai_messages,
            max_tokens=max_tokens,
            **extra_kwargs
        )
        return response.choices[0].message.content

    raise RuntimeError(
        "No LLM client available. "
        "Set MINIMAX_API_KEY or OPENAI_BASE_URL"
    )
