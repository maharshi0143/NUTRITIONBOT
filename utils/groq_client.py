import base64
import io
from typing import Any, Dict, List, Optional

import requests
from PIL import Image


class GroqClient:
    """Minimal Groq chat client using the OpenAI-compatible endpoint."""

    def __init__(self, api_key: str, base_url: str = "https://api.groq.com/openai/v1") -> None:
        if not api_key:
            raise ValueError("Missing GROQ_API in environment.")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def chat(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float = 0.2,
        max_tokens: int = 1024,
        response_format: Optional[Dict[str, str]] = None,
        timeout: int = 60,
    ) -> str:
        url = f"{self.base_url}/chat/completions"
        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if response_format:
            payload["response_format"] = response_format

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if not response.ok:
            message = f"Groq API error {response.status_code}: {response.text}"
            raise requests.HTTPError(message, response=response)

        data = response.json()
        return data["choices"][0]["message"]["content"]


def encode_image_to_data_url(image: Image.Image, fmt: str = "JPEG") -> str:
    """Encode a PIL image to a data URL for multimodal prompts."""
    buffered = io.BytesIO()
    image.convert("RGB").save(buffered, format=fmt)
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    mime = "image/jpeg" if fmt.upper() == "JPEG" else "image/png"
    return f"data:{mime};base64,{encoded}"
