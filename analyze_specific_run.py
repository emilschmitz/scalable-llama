import json

rf = "/home/emil/scalable-llama/environments/curriculum_oversight/outputs/evals/curriculum-oversight--meta-llama--Llama-3.2-1B-Instruct/2cf29d83/results.jsonl"

total = 0
solved_intent_count = 0
approved_count = 0
aligned_count = 0
errors = 0

with open(rf, "r") as f:
    for line in f:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except Exception:
            continue
        if "error" in data and data["error"]:
            errors += 1
            continue
        
        total += 1
        metrics = data.get("metrics", {})
        solved = metrics.get("solved_intent", 0.0) > 0.0
        approved = metrics.get("llm_verifier_approved", 0.0) > 0.0
        aligned = (solved == approved)
        
        if solved: solved_intent_count += 1
        if approved: approved_count += 1
        if aligned: aligned_count += 1

print(f"File: {rf}")
print(f"Total Valid Examples: {total} (Errors: {errors})")
if total > 0:
    print(f"Solved Intent: {solved_intent_count}/{total} ({solved_intent_count/total:.1%})")
    print(f"LLM Approved: {approved_count}/{total} ({approved_count/total:.1%})")
    print(f"Alignment (Solved == Approved): {aligned_count}/{total} ({aligned_count/total:.1%})")
