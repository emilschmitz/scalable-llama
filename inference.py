import argparse
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

def main():
    parser = argparse.ArgumentParser(description="Run inference using Llama-3.2-1B-Instruct with a LoRA adapter.")
    parser.add_argument("--base-model", type=str, default="sprints/Llama-3.2-1B-Instruct", help="The Hugging Face name of the base model.")
    parser.add_argument("--adapter", type=str, default="./lora_adapter", help="Path to the extracted LoRA adapter directory.")
    parser.add_argument("--prompt", type=str, default=None, help="The prompt to send to the model. If not provided, starts interactive mode.")
    parser.add_argument("--max-tokens", type=int, default=256, help="Maximum number of new tokens to generate.")
    parser.add_argument("--temperature", type=float, default=0.7, help="Generation temperature.")
    args = parser.parse_args()

    print(f"Loading tokenizer for base model: {args.base_model}...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    
    print(f"Loading base model: {args.base_model}...")
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )

    print(f"Applying LoRA adapter from: {args.adapter}...")
    try:
        model = PeftModel.from_pretrained(model, args.adapter)
    except Exception as e:
        print(f"Error loading LoRA adapter: {e}")
        print("Please ensure the adapter zip was extracted to the correct path.")
        sys.exit(1)

    def generate_response(prompt_text):
        messages = [{"role": "user", "content": prompt_text}]
        inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=args.max_tokens,
                temperature=args.temperature,
                do_sample=args.temperature > 0.0,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        return response

    if args.prompt:
        print(f"\nPrompt: {args.prompt}")
        response = generate_response(args.prompt)
        print(f"Response: {response}")
    else:
        print("\n--- Starting Interactive Inference Mode ---")
        print("Type 'exit' or 'quit' to end the session.\n")
        while True:
            try:
                user_input = input("User: ")
                if user_input.strip().lower() in ["exit", "quit"]:
                    break
                if not user_input.strip():
                    continue
                response = generate_response(user_input)
                print(f"Assistant: {response}\n")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    main()
