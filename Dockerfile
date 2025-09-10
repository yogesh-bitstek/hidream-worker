FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/ ./src/
COPY local_test.py .

CMD ["python3", "-m", "runpod.serverless", "--handler=src.handler.handler"]
