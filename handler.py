import runpod
import json
import base64
import io
import os
import time
from typing import Dict, Any

# Import your HiDream dependencies here
# import hidream  # Replace with actual imports

def load_model():
    """Load your HiDream model here"""
    # Initialize your model/service
    # model = hidream.load_model()  # Replace with actual loading logic
    print("Model loaded successfully")
    return None  # Replace with actual model

# Load model once when container starts
MODEL = load_model()

def process_hidream_request(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process HiDream-I1-Full image generation request
    """
    try:
        # Extract parameters from input
        prompt = input_data.get('prompt', '')
        if not prompt:
            return {
                "status": "error",
                "error": "Prompt is required"
            }
        
        # Get generation parameters with HiDream-I1-Full defaults
        height = input_data.get('height', 1024)
        width = input_data.get('width', 1024)
        num_inference_steps = input_data.get('num_inference_steps', 50)
        guidance_scale = input_data.get('guidance_scale', 5.0)
        seed = input_data.get('seed', None)
        
        print(f"Generating image with prompt: '{prompt}'")
        print(f"Parameters: {height}x{width}, steps={num_inference_steps}, guidance={guidance_scale}")
        
        # Set up generator with seed if provided
        generator = None
        if seed is not None:
            generator = torch.Generator(MODEL['device']).manual_seed(seed)
        
        # Generate image
        start_time = time.time()
        
        result = MODEL['pipeline'](
            prompt,
            height=height,
            width=width,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator,
        )
        
        generation_time = time.time() - start_time
        image = result.images[0]
        
        # Convert image to base64
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        image_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {
            "status": "success",
            "image": f"data:image/png;base64,{image_b64}",
            "generation_time": generation_time,
            "model": "HiDream-I1-Full",
            "parameters": {
                "prompt": prompt,
                "height": height,
                "width": width,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "seed": seed
            }
        }
        
    except Exception as e:
        print(f"Error in process_hidream_request: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }

def handler(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main handler function for RunPod serverless
    """
    try:
        # Get job input
        job_input = job.get('input', {})
        job_id = job.get('id', 'unknown')
        
        print(f"Processing job {job_id}")
        print(f"Input: {json.dumps(job_input, indent=2)}")
        
        # Validate required inputs
        if not job_input:
            return {
                "error": "No input provided",
                "status": "failed"
            }
        
        # Process the request
        start_time = time.time()
        result = process_hidream_request(job_input)
        processing_time = time.time() - start_time
        
        # Add processing metadata
        result["job_id"] = job_id
        result["total_processing_time"] = processing_time
        
        print(f"Job {job_id} completed in {processing_time:.2f}s")
        
        return result
        
    except Exception as e:
        print(f"Handler error: {str(e)}")
        return {
            "error": str(e),
            "status": "failed",
            "error_type": type(e).__name__
        }

def handler_wrapper(job):
    """Wrapper to ensure proper response format"""
    result = handler(job)
    
    # Ensure we return in RunPod expected format
    if "error" in result:
        return {"error": result["error"]}
    else:
        return result

if __name__ == "__main__":
    # Test locally
    test_job = {
        "input": {
            "prompt": "test prompt",
            "parameters": {"temperature": 0.8}
        },
        "id": "test-job-123"
    }
    
    result = handler(test_job)
    print("Test result:", json.dumps(result, indent=2))
else:
    # Start RunPod serverless
    runpod.serverless.start({"handler": handler_wrapper})
