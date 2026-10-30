import gradio as gr
from core.application.segmentation_service import segment
from core.domain.constants import DEFAULT_MODEL_ID
from core.entities.trained_models import MODELS

def preview(image, model_id):
    return segment(model_id, image)["mask"].astype("uint8") * 255

demo = gr.Interface(
    fn=preview,
    inputs=[
        gr.Image(type="pil"), 
        gr.Dropdown(choices=list(MODELS), 
                    value=DEFAULT_MODEL_ID
        )],
    outputs=gr.Image(),
)