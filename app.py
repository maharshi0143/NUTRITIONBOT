import gradio as gr

from controller import NourishBotController

controller = NourishBotController()


def run_nourishbot(image, diet, workflow, pantry):
        return controller.run(image=image, diet=diet, workflow=workflow, pantry=pantry)


with gr.Blocks(title="NUTRITIONBOT") as demo:
        gr.Markdown("# NUTRITIONBOT")

        with gr.Row():
                with gr.Column(scale=6):
                        with gr.Group(elem_classes=["nourish-card"]):
                                gr.Markdown("### Meal image")
                                image_input = gr.Image(type="pil", label="Upload your meal photo")

                with gr.Column(scale=5):
                        with gr.Group(elem_classes=["nourish-card"]):
                                gr.Markdown("### Preferences")
                                diet_input = gr.Dropdown(
                                        [
                                                "None",
                                                "Vegan",
                                                "Vegetarian",
                                                "Non-Vegetarian",
                                                "Gluten-free",
                                                "Keto",
                                        ],
                                        value="None",
                                        label="Dietary preference",
                                )
                                pantry_input = gr.Textbox(
                                        label="Available pantry ingredients (optional)",
                                        placeholder="e.g., olive oil, garlic, spinach",
                                )
                                workflow_input = gr.Radio(
                                        ["Analysis", "Recipe"],
                                        value="Analysis",
                                        label="Workflow",
                                )
                                with gr.Row():
                                        run_button = gr.Button(
                                                "Run NourishBot",
                                                variant="primary",
                                                elem_id="run-button",
                                        )
                                        clear_button = gr.ClearButton(
                                                [image_input, diet_input, pantry_input, workflow_input],
                                                value="Clear",
                                        )

        with gr.Row():
                with gr.Column():
                        output = gr.Markdown(elem_id="result-panel")

        with gr.Accordion("What you will get", open=False):
                gr.Markdown(
                        "- Ingredient detection and dish name\n"
                        "- Nutrition summary or recipe ideas\n"
                        "- Clear health guidance and cautions"
                )

        with gr.Accordion("Safety and disclaimer", open=False):
                gr.Markdown(
                        "AI suggestions are guidance only and may not cover all allergens or dietary needs."
                )

        run_button.click(
                fn=run_nourishbot,
                inputs=[image_input, diet_input, workflow_input, pantry_input],
                outputs=output,
        )

demo.launch()