"""Small OpenRouter client used for optional AI-written explanations."""
import logging

import httpx

from app.config import (
    LLM_ENABLED,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
    OPENROUTER_VERIFY_SSL,
)


logger = logging.getLogger("talentx.llm")


class LLMClient:
    """Thin wrapper around OpenRouter's OpenAI-compatible chat API."""

    @property
    def is_configured(self) -> bool:
        return bool(LLM_ENABLED and OPENROUTER_API_KEY)

    def chat(self, system_prompt: str, user_prompt: str, max_tokens: int = 260) -> str | None:
        if not self.is_configured:
            return None

        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.35,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://talentx.local",
            "X-Title": "TalentX",
        }

        try:
            with httpx.Client(timeout=15, verify=OPENROUTER_VERIFY_SSL) as client:
                response = client.post(
                    f"{OPENROUTER_BASE_URL.rstrip('/')}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            logger.warning("OpenRouter request failed; using local fallback: %s", exc)
            return None


_llm_client = None


def get_llm_client() -> LLMClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
