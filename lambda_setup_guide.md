# Lambda Cloud + vLLM Setup Notes

## Step 1: Local Weights & Git
*   **Adapter Folder:** Downloaded weights are stored in the local `lora/` folder.
*   **Zip File:** `lora/qijjz0uyyze1seeikm6bsv4u.zip`
*   **Git:** The directories `/lora/`, `/LoRa/`, `/lora_adapter/`, and `/LoRa_adapter/` have been added to `.gitignore` to prevent committing model weights.

---

## Step 2: Lambda Cloud Setup
*   **Instance Type:** NVIDIA A10G (24 GB VRAM) — cheapest and fastest for Llama 3.2 1B.
*   **Image:** Ubuntu with Lambda Stack 24.04 (drivers and CUDA pre-installed).
*   **Filesystem:** Do not attach a filesystem.
*   **Firewall:** Expose Port 80 (HTTP) to allow external requests.

---

## Step 3: Server Provisioning Commands

### 1. Copy zip & unzip on Lambda
From your **local machine**:
```bash
scp /home/emil/scalable-llama/lora/qijjz0uyyze1seeikm6bsv4u.zip ubuntu@<LAMBDA_IP>:~/lora.zip && ssh ubuntu@<LAMBDA_IP> "sudo apt-get update && sudo apt-get install -y unzip && unzip -o -d ~/lora_adapter ~/lora.zip"
```

### 2. SSH into Lambda
```bash
ssh ubuntu@<LAMBDA_IP>
```

### 3. Install vLLM on Lambda
Inside the SSH session:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install vllm
```

### 4. Run the vLLM Server on Port 80
Inside the SSH session:
```bash
sudo /home/ubuntu/venv/bin/vllm serve unsloth/Llama-3.2-1B-Instruct \
    --enable-lora \
    --lora-modules lora_adapter=/home/ubuntu/lora_adapter \
    --host 0.0.0.0 \
    --port 80
```

---

## Step 4: Verification & Routing
*   **Check Server Output:**
    ```bash
    curl http://<LAMBDA_IP>/v1/models
    ```
*   **Local Routing Config (`secrets.env`):**
    ```env
    PERSONAL_PRIME_API_KEY=<your_prime_api_key>
    FROZEN_VERIFIER_MODEL=lora_adapter
    VERIFIER_API_BASE_URL=http://<LAMBDA_IP>/v1
    ```
