from __future__ import annotations

import json
from typing import Any, Dict, List

import requests


NVIDIA_CHAT_COMPLETIONS_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def call_nvidia_chat_completions(
    *,
    api_key: str,
    model: str,
    messages: List[Dict[str, str]],
    max_tokens: int = 900,
    temperature: float = 0.2,
    timeout_s: int = 60,
) -> str:
    """
    Returns the model 'content' string.

    We keep this function intentionally thin; JSON parsing lives in the workflow layer.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    resp = requests.post(NVIDIA_CHAT_COMPLETIONS_URL, headers=headers, json=payload, timeout=timeout_s)
    resp.raise_for_status()

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected NVIDIA response shape: {json.dumps(data)[:500]}") from e

