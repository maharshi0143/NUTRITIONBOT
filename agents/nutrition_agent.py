from typing import Any, Dict, List

from utils.groq_client import GroqClient
from utils.json_utils import extract_json


class NutritionAgent:
    """Estimate nutrition from a list of ingredients."""

    def __init__(self, client: GroqClient, model: str) -> None:
        self.client = client
        self.model = model

    def run(self, ingredients: List[str], portion_notes: str, diet: str) -> Dict[str, Any]:
        if not ingredients:
            return {"error": "No ingredients detected."}

        diet_note = diet if diet else "No restriction"
        prompt = (
            "You are a nutrition analysis agent. Estimate nutrition for the meal. "
            "Use common portion sizes if not specified. If any ingredients conflict with the "
            "dietary restriction, add a warning about the conflict. Return strict JSON with keys: "
            "calories, macros (protein_g, carbs_g, fats_g), micros (array of strings), "
            "assumptions (array of strings), and warnings (array of strings)."
        )

        user_content = (
            f"Ingredients: {', '.join(ingredients)}. "
            f"Portion notes: {portion_notes or 'Not provided.'}. "
            f"Dietary restriction: {diet_note}."
        )

        messages = [
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": f"{prompt}\n{user_content}"},
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
