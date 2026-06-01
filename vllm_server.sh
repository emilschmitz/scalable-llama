#!/bin/bash
# Script to launch the vLLM server with the LoRA adapter enabled

# Using the ungated unsloth mirror to bypass Hugging Face approval gating
BASE_MODEL="unsloth/Llama-3.2-1B-Instruct"
ADAPTER_PATH="/home/ubuntu/lora_adapter" # Path to the folder containing adapter_config.json and adapter_model.safetensors

echo "Starting vLLM server with $BASE_MODEL and LoRA adapter on port 80..."

sudo /home/ubuntu/venv/bin/vllm serve "$BASE_MODEL" \
    --enable-lora \
    --lora-modules lora_adapter="$ADAPTER_PATH" \
    --host 0.0.0.0 \
    --port 80


