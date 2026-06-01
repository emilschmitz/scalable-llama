import argparse
import httpx
import sys

def main():
    parser = argparse.ArgumentParser(description="Query the vLLM server with the LoRA adapter.")
    parser.add_argument("--prompt", type=str, default="What is the secret word?", help="The prompt to send to the model.")
    parser.add_argument("--temperature", type=float, default=0.7, help="Generation temperature.")
    parser.add_argument("--max-tokens", type=int, default=128, help="Maximum tokens to generate.")
    parser.add_argument("--port", type=int, default=8000, help="Port of the vLLM server.")
    args = parser.parse_args()

    url = f"http://localhost:{args.port}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": "lora_adapter",
        "messages": [
            {"role": "user", "content": args.prompt}
        ],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens
    }

    print(f"Sending prompt: {args.prompt}")
    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code != 200:
            print(f"Error from server (Status {response.status_code}): {response.text}")
            sys.exit(1)
        
        result = response.json()
        output = result["choices"][0]["message"]["content"]
        print("\nResponse:")
        print(output)
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Make sure the vllm server is running on the correct port and accessible.")
        sys.exit(1)

if __name__ == "__main__":
    main()
