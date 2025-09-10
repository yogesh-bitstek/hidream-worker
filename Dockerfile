FROM nvidia/cuda:12.4.0-devel-ubuntu20.04

# Install system packages needed for building flash-attn and Python
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    python3-dev \
    python3-pip \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install PyTorch nightly (use pip3 instead of pip)
RUN pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

# Install other requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install flash-attn separately with no isolation
RUN pip3 install -U flash-attn --no-build-isolation

# Copy source code
COPY src/ ./src/

CMD ["python3", "-u", "src/handler.py"]
