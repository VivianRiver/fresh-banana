"""
Fresh Banana demo app.

Snap or upload a photo of a banana and the model estimates how many days
have passed since the banana was purchased.

Setup (once, in the torch environment):
    conda activate torch
    pip install gradio

Run from the repo root:
    python app.py

Then open http://<LiminalRoot's IP address>:7860 on any device on your
home network. Find the IP with:  hostname -I
"""

import os
os.environ["KERAS_BACKEND"] = "torch"

import keras
import numpy as np
import gradio as gr
from PIL import Image, ImageOps

MODEL_PATH = "banana_model.keras"   # adjust if your file lives elsewhere
IMAGE_SIZE = 224                    # must match what the model was trained on

model = keras.saving.load_model(MODEL_PATH)


def prepare(image: Image.Image) -> np.ndarray:
    """Turn a phone photo into the exact input format used during training."""
    # Apply the camera's orientation so the pixels match what the user sees
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")

    # Training photos were 1:1, so center-crop phone photos to a square
    w, h = image.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    image = image.crop((left, top, left + side, top + side))

    # Same resampling as the resize script used for the training data
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)

    # uint8, 0-255: the model's own Rescaling layer handles the /255
    arr = np.asarray(image, dtype=np.uint8)

    # The model expects a batch, so add a leading dimension: (1, 224, 224, 3)
    return np.expand_dims(arr, axis=0)


def predict(image: Image.Image) -> str:
    if image is None:
        return "Please take or upload a photo of a banana."

    batch = prepare(image)
    days = float(model.predict(batch, verbose=0)[0][0])

    return (
        f"About {days:.1f} days since purchase.\n\n"
        "Works best with a single banana on a plain, light-brown surface, "
        "similar to the training photos."
    )


demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(
        type="pil",
        sources=["upload", "webcam"],
        label="Banana photo",
    ),
    outputs=gr.Textbox(label="Estimate"),
    title="Fresh Banana",
    description="Estimates a banana's age from a photo. "
                "Trained on 16 bananas photographed daily against a cork board.",
    flagging_mode="never",
)

if __name__ == "__main__":
    # 0.0.0.0 makes the app reachable from other devices on your network,
    # not just from LiminalRoot itself
    demo.launch(server_name="0.0.0.0", server_port=7860)