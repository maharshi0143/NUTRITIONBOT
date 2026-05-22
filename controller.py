import os
from typing import Any, Dict

from dotenv import load_dotenv

from agents.health_agent import HealthAgent
from agents.nutrition_agent import NutritionAgent
from agents.orchestrator import NourishBotOrchestrator
from agents.recipe_agent import RecipeAgent
from agents.vision_agent import VisionAgent
from utils.groq_client import GroqClient


class NourishBotController:
	"""Entry point for the Gradio app to run multi-agent workflows."""

	def __init__(self) -> None:
		load_dotenv()
		api_key = os.getenv("GROQ_API")
		vision_model = os.getenv(
			"GROQ_VISION_MODEL",
			"meta-llama/llama-4-scout-17b-16e-instruct",
		)
		text_model = os.getenv(
			"GROQ_TEXT_MODEL",
			"meta-llama/llama-4-scout-17b-16e-instruct",
		)
		self.init_error = None

		try:
			client = GroqClient(api_key=api_key)
			self.orchestrator = NourishBotOrchestrator(
				vision_agent=VisionAgent(client, vision_model),
				nutrition_agent=NutritionAgent(client, text_model),
				recipe_agent=RecipeAgent(client, text_model),
				health_agent=HealthAgent(client, text_model),
			)
		except ValueError as exc:
			self.orchestrator = None
			self.init_error = str(exc)

	def run(self, image, diet: str, workflow: str, pantry: str) -> str:
		if self.init_error:
			return f"Setup error: {self.init_error}"

		diet_value = "" if diet == "None" else diet
		result = self.orchestrator.run(
			image=image,
			diet=diet_value,
			workflow=workflow,
			pantry=pantry,
		)
		return self._format_markdown(result)

	def _format_markdown(self, result: Dict[str, Any]) -> str:
		if "vision" not in result:
			return "No response from the vision agent."

		vision = result.get("vision", {})
		if "error" in vision:
			return f"Error: {vision['error']}"

		dish_name = vision.get("dish_name", "Unknown dish")
		ingredients = vision.get("ingredients", [])
		portion_notes = vision.get("portion_notes", "")
		confidence = vision.get("confidence", "")

		lines = [
			f"## Detected dish\n**{dish_name}**",
			"\n### Ingredients",
			"- " + "\n- ".join(ingredients) if ingredients else "- Not detected",
		]

		if portion_notes:
			lines.append(f"\n**Portion notes**: {portion_notes}")
		if confidence:
			lines.append(f"\n**Confidence**: {confidence}")

		if result.get("workflow") == "Recipe":
			recipes = result.get("recipes", {})
			if "error" in recipes:
				lines.append(f"\n**Recipe error**: {recipes['error']}")
			else:
				lines.append("\n## Recipe ideas")
				for idx, recipe in enumerate(recipes.get("recipes", []), start=1):
					lines.append(f"\n### {idx}. {recipe.get('name', 'Recipe')}")
					lines.append(f"**Time**: {recipe.get('time_minutes', 'N/A')} min")
					ingredients_list = recipe.get("ingredients", [])
					if ingredients_list:
						lines.append("**Ingredients**:\n- " + "\n- ".join(ingredients_list))
					steps = recipe.get("steps", [])
					if steps:
						lines.append("**Steps**:\n- " + "\n- ".join(steps))
					swaps = recipe.get("swaps", [])
					if swaps:
						lines.append("**Swaps**:\n- " + "\n- ".join(swaps))

				shopping = recipes.get("shopping_list", [])
				if shopping:
					lines.append("\n**Shopping list**:\n- " + "\n- ".join(shopping))
				tips = recipes.get("tips", [])
				if tips:
					lines.append("\n**Tips**:\n- " + "\n- ".join(tips))
		else:
			nutrition = result.get("nutrition", {})
			if "error" in nutrition:
				lines.append(f"\n**Nutrition error**: {nutrition['error']}")
			else:
				lines.append("\n## Nutrition summary")
				lines.append(f"**Calories**: {nutrition.get('calories', 'N/A')}")
				macros = nutrition.get("macros", {})
				if macros:
					lines.append(
						"**Macros**: "
						f"Protein {macros.get('protein_g', 'N/A')} g, "
						f"Carbs {macros.get('carbs_g', 'N/A')} g, "
						f"Fats {macros.get('fats_g', 'N/A')} g"
					)
				micros = nutrition.get("micros", [])
				if micros:
					lines.append("**Micros**:\n- " + "\n- ".join(micros))
				assumptions = nutrition.get("assumptions", [])
				if assumptions:
					lines.append("**Assumptions**:\n- " + "\n- ".join(assumptions))
				warnings = nutrition.get("warnings", [])
				if warnings:
					lines.append("**Warnings**:\n- " + "\n- ".join(warnings))

		health = result.get("health", {})
		if "error" in health:
			lines.append(f"\n**Health note**: {health['error']}")
		else:
			lines.append("\n## Health guidance")
			lines.append(health.get("summary", ""))
			strengths = health.get("strengths", [])
			if strengths:
				lines.append("**Strengths**:\n- " + "\n- ".join(strengths))
			improvements = health.get("improvements", [])
			if improvements:
				lines.append("**Improvements**:\n- " + "\n- ".join(improvements))
			cautions = health.get("cautions", [])
			if cautions:
				lines.append("**Cautions**:\n- " + "\n- ".join(cautions))

		return "\n".join(lines)
