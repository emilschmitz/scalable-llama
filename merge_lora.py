import argparse
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

def main():
    parser = argparse.ArgumentParser(description="Merge a LoRA adapter into the base model.")
    parser.add_argument("--base-model", type=str, default="unsloth/Llama-3.2-1B-Instruct", 
                        help="Hugging Face name or path to the base model. Default uses the ungated Unsloth mirror.")
    parser.add_argument("--adapter-dir", type=str, required=True, 
                        help="Path to the directory containing adapter_config.json and adapter_model.safetensors.")
    parser.add_argument("--output-dir", type=str, default="./merged_model", 
                        help="Directory where the merged model will be saved.")
    args = parser.parse_args()

    print(f"Loading tokenizer for base model: {args.base_model}...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    
    print(f"Loading base model: {args.base_model}...")
    base_model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=torch.bfloat16,
        device_map="cpu"  # Merging on CPU is safer to avoid GPU OOM
    )

    print(f"Applying LoRA adapter from: {args.adapter_dir}...")
    model = PeftModel.from_pretrained(base_model, args.adapter_dir)

    print("Merging LoRA weights into the base model...")
    merged_model = model.merge_and_unload()

    print(f"Saving merged model to: {args.output_dir}...")
    os.makedirs(args.output_dir, exist_ok=True)
    merged_model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    
    print("\nMerge complete! You can now serve this model using vLLM:")
    print(f"  vllm serve {args.output_dir} --port 8000")

if __name__ == "__main__":
    main()
