#FROM nvidia/cuda:12.4.0-devel-ubuntu20.04

# Use PyTorch base image with CUDA support
FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Flash Attention first (requires specific CUDA setup)
RUN pip install packaging ninja
RUN pip install flash-attn --no-build-isolation

# Install other Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install diffusers from source for better compatibility
RUN pip install git+https://github.com/huggingface/diffusers.git

# Copy application code
COPY . .

# Create directories for models/cache
RUN mkdir -p /app/models /app/cache

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TORCH_CUDA_ARCH_LIST="8.0;8.6;8.9;9.0"
ENV CUDA_HOME=/usr/local/cuda

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the handler
CMD ["python", "handler.py"]
