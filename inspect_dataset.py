import json

dataset_path = "/home/emil/scalable-llama/verifier_tuning_dataset.json"

with open(dataset_path, "r") as f:
    data = json.load(f)

item = data[0]
print("--- BASELINE SYSTEM PROMPT ---")
print(item["verifier_system_prompt_baseline"])
print("\n--- BASELINE USER PROMPT ---")
print(item["verifier_user_prompt"])
print("\n--- TRUE VERDICT ---")
print(item["true_verdict"])
