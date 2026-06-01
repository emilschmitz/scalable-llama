import json
import re

dataset_path = "/home/emil/scalable-llama/verifier_tuning_dataset.json"

with open(dataset_path, "r") as f:
    data = json.load(f)

for i in range(5):
    item = data[i]
    sys_prompt = item["verifier_system_prompt_baseline"]
    # Extract rules block
    match = re.search(r"Task Rules:\n(.*?)\n\nFormat Requirement:", sys_prompt, re.DOTALL)
    rules = match.group(1).strip() if match else "Rules not found"
    print(f"--- Example {i} ---")
    print(f"Rules:\n{rules}")
    print(f"True Verdict: {item['true_verdict']}")
    print(f"Solved Intent: {item['solved_intent']}")
