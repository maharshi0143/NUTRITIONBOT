from typing import Any, Dict, List

from utils.groq_client import GroqClient
from utils.json_utils import extract_json


class RecipeAgent:
    """Create recipe ideas based on ingredients and dietary preferences."""

    def __init__(self, client: GroqClient, model: str) -> None:
        self.client = client
        self.model = model

    def run(self, ingredients: List[str], diet: str, pantry: str) -> Dict[str, Any]:
        if not ingredients:
            return {"error": "No ingredients detected."}

        diet_note = diet if diet else "No restriction"
        pantry_note = pantry if pantry else "None"

        prompt = (
            "You are a recipe agent. Create 3 recipe ideas using the provided ingredients. "
            "Respect the diet restriction. If an ingredient violates the diet, suggest a swap. "
            "Return strict JSON with keys: recipes (array of objects with name, time_minutes, "
            "ingredients, steps, swaps), shopping_list (array of strings), and tips (array of strings)."
        )

        user_content = (
            f"Detected ingredients: {', '.join(ingredients)}. "
            f"Diet restriction: {diet_note}. "
            f"Available pantry ingredients: {pantry_note}."
        )

        messages = [
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": f"{prompt}\n{user_content}"},
        ]

        response = self.client.chat(
            model=self.model,
            messages=messages,
            temperature=0.4,
            max_tokens=1200,
            response_format={"type": "json_object"},
        )

        parsed = extract_json(response)
        return parsed or {"raw_response": response}
