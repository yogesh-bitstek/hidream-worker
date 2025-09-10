import base64
from src.handler import handler

# Simulate a RunPod job
job = {
    "input": {
        "prompt": "A cat holding a sign that says HiDream.ai",
        "steps": 20,
        "seed": 123,
        "height": 512,
        "width": 512,
    }
}

result = handler(job)

# Save image from base64
with open("test_output.png", "wb") as f:
    f.write(base64.b64decode(result["image_base64"]))

print("✅ Test image saved as test_output.png")
