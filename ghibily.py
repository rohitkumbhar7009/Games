import gradio as gr
import torch
try:
    from diffusers import StableDiffusionPipeline
    from transformers import logging
except ImportError as e:
    print("Error: Missing required libraries. Install them using: \n\n    pip install transformers torch torchvision diffusers gradio\n")
    exit()

logging.set_verbosity_error()  # Suppress unnecessary logs

# Load the model
model_id = "stabilityai/stable-diffusion-xl-base-1.0"
try:
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

def convert_to_ghibli(image):
    prompt = "Convert this image to Ghibli style artwork, colorful, vibrant, anime inspired"
    try:
        result = pipe(prompt=prompt, image=image).images[0]
        return result
    except Exception as e:
        return f"Error during conversion: {e}"

def main():
    iface = gr.Interface(
        fn=convert_to_ghibli,
        inputs=gr.Image(type="pil", label="Upload your Image"),
        outputs=gr.Image(type="pil", label="Ghibli Style Output"),
        title="Ghibli Style Image Converter",
        description="Upload an image and convert it to a Ghibli-style artwork using AI."
    )
    iface.launch()

if __name__ == "__main__":
    main()
