from typing import Any, Dict

from utils.groq_client import GroqClient
from utils.json_utils import extract_json


class HealthAgent:
    """Provide high-level health guidance based on nutrition or recipes."""

    def __init__(self, client: GroqClient, model: str) -> None:
        self.client = client
        self.model = model

    def run(self, context: str) -> Dict[str, Any]:
        if not context:
            return {"error": "Missing context for health evaluation."}

        prompt = (
            "You are a health guidance agent. Provide a short evaluation and 3 actionable tips. "
            "Return strict JSON with keys: summary (string), strengths (array of strings), "
            "improvements (array of strings), and cautions (array of strings)."
        )

        messages = [
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": f"{prompt}\nContext: {context}"},
        ]

        response = self.client.chat(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=700,
            response_format={"type": "json_object"},
        )

        parsed = extract_json(response)
        return parsed or {"raw_response": response}
