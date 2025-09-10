FROM nvidia/cuda:12.1.1-devel-ubuntu20.04

# Install system packages needed for building flash-attn
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    python3-dev \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install flash-attn separately with no isolation
RUN pip install -U flash-attn --no-build-isolation

COPY src/ ./src/
CMD ["python3", "-u", "src/handler.py"]
