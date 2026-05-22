from typing import Any, Dict, List

from PIL import Image

from utils.groq_client import GroqClient, encode_image_to_data_url
from utils.json_utils import extract_json


class VisionAgent:
    """Analyze an image to identify ingredients and a dish name."""

    def __init__(self, client: GroqClient, model: str) -> None:
        self.client = client
        self.model = model

    def run(self, image: Image.Image) -> Dict[str, Any]:
        if image is None:
            return {"error": "No image provided."}

        data_url = encode_image_to_data_url(image)

        prompt = (
            "You are a vision agent for a nutrition assistant. "
            "Identify the dish and list visible ingredients. "
            "Return strict JSON with keys: dish_name (string), ingredients (array of strings), "
            "portion_notes (string), confidence (number 0-1)."
        )

        messages = [
            {"role": "system", "content": "Return JSON only."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ]

        response = self.client.chat(
            model=self.model,
            messages=messages,
            temperature=0.2,
            max_tokens=900,
            response_format={"type": "json_object"},
        )

        parsed = extract_json(response)
        return parsed or {"raw_response": response}
