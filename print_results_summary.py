import os
import json
import glob

def analyze_evals():
    eval_dirs = glob.glob("/home/emil/scalable-llama/environments/curriculum_oversight/outputs/evals/**/*", recursive=True)
    results_files = [f for f in eval_dirs if f.endswith("results.jsonl")]
    
    print(f"Found {len(results_files)} results.jsonl files:")
    for rf in sorted(results_files):
        # Read metadata if present
        meta_file = os.path.join(os.path.dirname(rf), "metadata.json")
        model_name = "Unknown"
        env_version = "Unknown"
        avg_reward = 0.0
        avg_metrics = {}
        if os.path.exists(meta_file):
            try:
                with open(meta_file, "r") as f:
                    meta = json.load(f)
                    model_name = meta.get("model", "Unknown")
                    env_version = meta.get("version_info", {}).get("env_version", "Unknown")
                    avg_reward = meta.get("avg_reward", 0.0)
                    avg_metrics = meta.get("avg_metrics", {})
            except Exception as e:
                pass
        
        # Read results
        total = 0
        solved_intent_count = 0
        approved_count = 0
        aligned_count = 0
        errors = 0
        
        ifeval_total = 0
        ifeval_solved_intent = 0
        ifeval_approved = 0
        ifeval_aligned = 0
        
        stego_total = 0
        stego_solved_intent = 0
        stego_approved = 0
        stego_aligned = 0

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
                
                info = data.get("info", {})
                curriculum_type = info.get("curriculum_type", "unknown")
                
                if curriculum_type == "ifeval":
                    ifeval_total += 1
                    if solved: ifeval_solved_intent += 1
                    if approved: ifeval_approved += 1
                    if aligned: ifeval_aligned += 1
                elif curriculum_type == "steganographic":
                    stego_total += 1
                    if solved: stego_solved_intent += 1
                    if approved: stego_approved += 1
                    if aligned: stego_aligned += 1
                
                if solved: solved_intent_count += 1
                if approved: approved_count += 1
                if aligned: aligned_count += 1
        
        rel_path = os.path.relpath(rf, "/home/emil/scalable-llama/environments/curriculum_oversight/outputs/evals")
        print(f"\nFile: {rel_path}")
        print(f"  Model: {model_name} | Env Ver: {env_version}")
        print(f"  Total Valid Examples: {total} (Errors: {errors})")
        if total > 0:
            print(f"  Overall: Solved Intent: {solved_intent_count}/{total} ({solved_intent_count/total:.1%}) | "
                  f"LLM Approved: {approved_count}/{total} ({approved_count/total:.1%}) | "
                  f"Alignment (Solved == Approved): {aligned_count}/{total} ({aligned_count/total:.1%})")
        if ifeval_total > 0:
            print(f"  IFEval:  Solved Intent: {ifeval_solved_intent}/{ifeval_total} ({ifeval_solved_intent/ifeval_total:.1%}) | "
                  f"LLM Approved: {ifeval_approved}/{ifeval_total} ({ifeval_approved/ifeval_total:.1%}) | "
                  f"Alignment: {ifeval_aligned}/{ifeval_total} ({ifeval_aligned/ifeval_total:.1%})")
        if stego_total > 0:
            print(f"  Stego:   Solved Intent: {stego_solved_intent}/{stego_total} ({stego_solved_intent/stego_total:.1%}) | "
                  f"LLM Approved: {stego_approved}/{stego_total} ({stego_approved/stego_total:.1%}) | "
                  f"Alignment: {stego_aligned}/{stego_total} ({stego_aligned/stego_total:.1%})")

if __name__ == "__main__":
    analyze_evals()
