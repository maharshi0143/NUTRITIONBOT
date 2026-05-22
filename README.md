## AI NourishBot (Multi-Agent Nutrition Assistant)

NourishBot is a multi-agent system that analyzes food images, estimates nutrition, and generates recipe ideas based on dietary preferences. It uses Groq-hosted models for vision and language tasks and ships with a Gradio interface.

### Features
- Vision agent detects the dish and ingredients from an image.
- Nutrition agent estimates calories, macros, and micros.
- Recipe agent suggests diet-friendly recipes and swaps.
- Health agent provides a short evaluation and tips.
- Two workflows: **Analysis** or **Recipe**.

### Live Demo
- https://nutritionbot-53iy.onrender.com/

### Setup
1. Create a `.env` file in the project root with:
	- `GROQ_API=your_api_key`
	- Optional: `GROQ_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct`
	- Optional: `GROQ_TEXT_MODEL=meta-llama/llama-4-scout-17b-16e-instruct`
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
3. Run the app:
	```bash
	python app.py
	```

### Notes
- Nutrition estimates are approximate and depend on detected ingredients and assumed portions.
- Always review recipe suggestions for allergens and safety.
