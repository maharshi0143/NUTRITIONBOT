from typing import Any, Dict

from agents.health_agent import HealthAgent
from agents.nutrition_agent import NutritionAgent
from agents.recipe_agent import RecipeAgent
from agents.vision_agent import VisionAgent


class NourishBotOrchestrator:
    """Coordinate the multi-agent workflow."""

    def __init__(
        self,
        vision_agent: VisionAgent,
        nutrition_agent: NutritionAgent,
        recipe_agent: RecipeAgent,
        health_agent: HealthAgent,
    ) -> None:
        self.vision_agent = vision_agent
        self.nutrition_agent = nutrition_agent
        self.recipe_agent = recipe_agent
        self.health_agent = health_agent

    def run(self, image, diet: str, workflow: str, pantry: str) -> Dict[str, Any]:
        state: Dict[str, Any] = {
            "workflow": workflow,
            "diet": diet,
        }

        vision = self.vision_agent.run(image)
        state["vision"] = vision

        if "error" in vision:
            return state

        ingredients = vision.get("ingredients", [])
        portion_notes = vision.get("portion_notes", "")

        if workflow == "Recipe":
            recipes = self.recipe_agent.run(ingredients, diet, pantry)
            state["recipes"] = recipes
            context = f"Ingredients: {ingredients}. Recipes: {recipes}."
            state["health"] = self.health_agent.run(context)
            return state

        nutrition = self.nutrition_agent.run(ingredients, portion_notes, diet)
        state["nutrition"] = nutrition
        context = f"Ingredients: {ingredients}. Nutrition: {nutrition}. Diet: {diet or 'None'}."
        state["health"] = self.health_agent.run(context)
        return state
