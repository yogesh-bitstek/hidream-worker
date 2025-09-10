import torch
from .pipeline import pipe
from .utils import image_to_base64

def handler(job):
    """
    RunPod job handler.

    job.input example:
    {
        "prompt": "A glowing castle in the clouds",
        "steps": 30,
        "seed": 42,
        "height": 1024,
        "width": 1024,
        "guidance_scale": 5.0
    }
    """
    inputs = job.get("input", {})

    prompt = inputs.get("prompt", "An image")
    steps = inputs.get("steps", 30)
    seed = inputs.get("seed")
    height = inputs.get("height", 1024)
    width = inputs.get("width", 1024)
    guidance_scale = inputs.get("guidance_scale", 5.0)

    generator = None if seed is None else torch.Generator("cuda").manual_seed(seed)

    image = pipe(
        prompt,
        height=height,
        width=width,
        guidance_scale=guidance_scale,
        num_inference_steps=steps,
        generator=generator,
    ).images[0]

    return {"image_base64": image_to_base64(image)}