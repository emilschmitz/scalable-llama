import json

rf = "/home/emil/scalable-llama/environments/curriculum_oversight/outputs/evals/curriculum-oversight--meta-llama--Llama-3.2-1B-Instruct/2cf29d83/results.jsonl"

with open(rf, "r") as f:
    for i, line in enumerate(f):
        if not line.strip():
            continue
        data = json.loads(line)
        metrics = data.get("metrics", {})
        solved = metrics.get("solved_intent", 0.0) > 0.0
        approved = metrics.get("llm_verifier_approved", 0.0) > 0.0
        
        # Let's look at completions and verifications
        completions = data.get("completion", [])
        print(f"--- Example {i} | Solved: {solved} | Approved: {approved} ---")
        if not solved:
            print("TASK PROMPT:")
            print(data["prompt"][0]["content"])
            print("\nSOLVER COMPLETION:")
            if len(completions) > 0:
                print(completions[0]["content"])
            else:
                print("No completion")
            print("\nVERIFIER TRAJECTORY:")
            if len(completions) > 1:
                print("Verifier prompt:")
                print(completions[1].get("prompt", [{}])[-1].get("content", ""))
                print("Verifier response:")
                print(completions[1].get("content", ""))
            print("=" * 60)
