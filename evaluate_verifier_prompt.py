import json
import re
import asyncio
import httpx
import math
import os

api_key = os.getenv("PERSONAL_PRIME_API_KEY", "")
model = "meta-llama/Llama-3.2-1B-Instruct"
url = "https://api.pinference.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Prompt Design A: Clean Baseline (No length/relevance checks, just pure constraints check)
def prompt_a_system(rules_text):
    return f"""You are an independent evaluator grading a student's answer.
Your task is to verify if the student successfully followed all instruction rules in their response.

Task Rules:
{rules_text}

Format Requirement:
You must output a valid JSON object in exactly the format:
{{
  "verdict": "YES"
}}
or
{{
  "verdict": "NO"
}}
Output "YES" if all task rules are satisfied, and "NO" if they are violated.
Do not include any explanation or extra text. Output ONLY the JSON."""

def prompt_a_user(solver_completion):
    return f"Solver response to verify:\n{solver_completion}"


# Prompt Design B: Chain of Thought (Reasoning first, then JSON verdict)
def prompt_b_system(rules_text):
    return f"""You are a strict grading assistant.
Your task is to analyze the student's response step by step and verify if it satisfies all task rules.

Task Rules:
{rules_text}

For each rule, write a short explanation of whether it is satisfied or violated.
After checking all rules, output the final verdict in this JSON format:
{{
  "verdict": "YES"
}}
or
{{
  "verdict": "NO"
}}
Output "YES" if all task rules are satisfied, and "NO" if any rule is violated. Do not include any other text after the JSON."""

def prompt_b_user(solver_completion):
    return f"Student response:\n\"\"\"\n{solver_completion}\n\"\"\"\n\nPlease evaluate the response using the specified format."


# Prompt Design C: Natural language critical checklist with a simple text output
def prompt_c_system(rules_text):
    return f"""You are a strict grading assistant.
Verify if the student response satisfies all task rules.

Task Rules:
{rules_text}

Analyze the rules and output strictly in this format:
Rule check: <short explanation>
Verdict: <YES or NO>"""

def prompt_c_user(solver_completion):
    return f"Student response:\n\"\"\"\n{solver_completion}\n\"\"\""


# Prompt Design D: Structured Recipe
def prompt_d_system(rules_text):
    return f"""You are a highly precise grading assistant. Your task is to verify if the student's response satisfies the given rules.

Task Rules:
{rules_text}

Please follow this verification protocol:
1. Sentence Listing: Extract and list every sentence from the student's response on a separate numbered line (e.g., Sentence 1: ..., Sentence 2: ...).
2. Rule-by-rule analysis:
- If a rule specifies sentence count: count the sentences from step 1.
- If a rule specifies word counts per sentence: for each sentence, write down the word count.
- If a rule forbids commas: check if any comma ',' is found.
- If a rule requires a word (e.g., 'energy') to appear N times: list each occurrence.
- If a rule requires different starting letters: write down the first letter of each sentence and check for duplicates.
- If a rule limits word frequency (e.g., no word more than 3 times): check common words like 'the', 'and', 'a', etc., and count their occurrences.
- If a rule requires words with 5+ letters: check if each sentence contains such a word.
3. Verdict: Conclude with the JSON block:
{{
  "verdict": "YES"
}}
if all rules are satisfied, or:
{{
  "verdict": "NO"
}}
if any rule is violated."""

def prompt_d_user(solver_completion):
    return f"Student response to verify:\n\"\"\"\n{solver_completion}\n\"\"\""


# Prompt Design E: Tailored Recipe (dynamically constructed based on the rule text)
def prompt_e_system(rules_text):
    has_sentence_count = "5 sentences" in rules_text
    has_word_len_range = "words long" in rules_text
    has_5_letters = "5 or more letters" in rules_text
    has_no_commas = "commas" in rules_text
    has_energy = "energy" in rules_text
    has_diff_start = "different letter" in rules_text
    has_no_word_3x = "more than 3 times" in rules_text or "word may appear" in rules_text
    has_unique_words = "unique words" in rules_text

    protocol_steps = []
    protocol_steps.append("1. Sentence Listing:\nExtract and list every sentence from the student's response on a separate numbered line (e.g., Sentence 1: ..., Sentence 2: ...).")

    analysis_steps = []
    
    if has_sentence_count:
        analysis_steps.append("- Sentence Count: Count the sentences you listed. The rule says: 'Your response must be exactly 5 sentences long'. State the total sentence count. If it is not exactly 5, the verdict is NO.")
        
    if has_word_len_range:
        analysis_steps.append("- Words per Sentence: For each sentence, count the number of words. The rule says: 'Each sentence must be between 8 and 15 words long'. List the word count of each sentence. If any sentence is outside [8, 15], the verdict is NO.")
        
    if has_5_letters:
        analysis_steps.append("- 5+ Letter Words: For each sentence, verify if it contains at least one word with 5 or more letters. List a qualifying word for each sentence. If any sentence does not have one, the verdict is NO.")
        
    if has_no_commas:
        analysis_steps.append("- Commas Check: Check if the text contains any commas (','). If any comma is found, the verdict is NO.")
        
    if has_energy:
        analysis_steps.append("- Energy Occurrences: Find and list all occurrences of the word 'energy' (case-insensitive) in the response. If 'energy' appears less than 2 times, the verdict is NO.")
        
    if has_diff_start:
        analysis_steps.append("- Starting Letters: Write down the first letter of each sentence. Check if they are all unique. If there are any duplicate starting letters, the verdict is NO.")
        
    if has_no_word_3x:
        analysis_steps.append("- Word Frequencies: Check if any word is used more than 3 times. Look especially at common words like 'the', 'and', 'a', 'to', 'of', 'in', 'is', 'for', 'on', 'with', 'it', 'as', 'at', 'forest'. If any word is used 4 or more times, the verdict is NO.")
        
    if has_unique_words:
        analysis_steps.append("- Unique Words: Check if the text contains at least 20 unique words. If it has fewer than 20 unique words, the verdict is NO.")

    analysis_text = "\n".join(analysis_steps)

    prompt = f"""You are a highly precise grading assistant. Your task is to verify if the student's response satisfies the given rules.

Task Rules:
{rules_text}

Please follow this verification protocol:
{protocol_steps[0]}

2. Rule-by-rule analysis:
{analysis_text}

3. Verdict: Conclude your analysis with a JSON block:
{{
  "verdict": "YES"
}}
if all task rules are fully satisfied, or:
{{
  "verdict": "NO"
}}
if any rule is violated. Do not output any explanation or text after the JSON block."""
    return prompt

def prompt_e_user(solver_completion):
    return f"Student response to verify:\n\"\"\"\n{solver_completion}\n\"\"\""


# Prompt Design F: Strict Formatting Template & Tailored Rules
def prompt_f_system(rules_text):
    has_sentence_count = "5 sentences" in rules_text
    has_word_len_range = "words long" in rules_text
    has_5_letters = "5 or more letters" in rules_text
    has_no_commas = "commas" in rules_text
    has_energy = "energy" in rules_text
    has_diff_start = "different letter" in rules_text
    has_no_word_3x = "more than 3 times" in rules_text or "word may appear" in rules_text
    has_unique_words = "unique words" in rules_text

    analysis_instructions = []
    if has_sentence_count:
        analysis_instructions.append("- Sentence Count Rule: Count the listed sentences. If the count is not exactly 5, this rule is violated.")
    if has_word_len_range:
        analysis_instructions.append("- Words per Sentence Rule: Count the words in each sentence. If any sentence has fewer than 8 or more than 15 words, this rule is violated.")
    if has_5_letters:
        analysis_instructions.append("- 5+ Letter Words Rule: Verify if each sentence contains at least one word with 5 or more letters. If any sentence does not, this rule is violated.")
    if has_no_commas:
        analysis_instructions.append("- No Commas Rule: Check if the text contains any commas (','). If a comma is found, this rule is violated.")
    if has_energy:
        analysis_instructions.append("- Target Word Count Rule: Count the occurrences of 'energy' (case-insensitive). If it is less than 2, this rule is violated.")
    if has_diff_start:
        analysis_instructions.append("- Different Starting Letters Rule: Write down the first letter of each sentence and verify they are all unique. If there are duplicates, this rule is violated.")
    if has_no_word_3x:
        analysis_instructions.append("- Word Frequency Rule: Check if any word is used more than 3 times (look at 'the', 'and', 'a', 'to', 'of', 'in', 'is', 'for', 'on', 'with', 'it', 'as', 'at', 'forest'). If any word appears 4 or more times, this rule is violated.")
    if has_unique_words:
        analysis_instructions.append("- Unique Words Rule: Count/estimate unique words. If fewer than 20 unique words, this rule is violated.")

    analysis_insts_text = "\n".join(analysis_instructions)

    return f"""You are a strict grading assistant. Your task is to verify if the student's response satisfies all task rules.

Task Rules to verify:
{rules_text}

Instructions for grading:
{analysis_insts_text}

You must write your output in this format:

Sentence Listing:
1. [First sentence]
2. [Second sentence]
...

Rule-by-rule analysis:
- [Rule 1]: [Analysis of rule 1 and whether it is satisfied/violated]
- [Rule 2]: [Analysis of rule 2 if applicable]
...

JSON Verdict:
{{
  "verdict": "YES"
}}
or
{{
  "verdict": "NO"
}}

Output "YES" if and only if all task rules are satisfied. Output "NO" if any rule is violated."""

def prompt_f_user(solver_completion):
    return f"Student response to evaluate:\n\"\"\"\n{solver_completion}\n\"\"\"\n\nPlease evaluate and output using the exact formatting structure."


# Prompt Design G: Tailored Recipe with Strict Negative Focus (NO default)
def prompt_g_system(rules_text):
    has_sentence_count = "5 sentences" in rules_text
    has_word_len_range = "words long" in rules_text
    has_5_letters = "5 or more letters" in rules_text
    has_no_commas = "commas" in rules_text
    has_energy = "energy" in rules_text
    has_diff_start = "different letter" in rules_text
    has_no_word_3x = "more than 3 times" in rules_text or "word may appear" in rules_text
    has_unique_words = "unique words" in rules_text

    protocol_steps = []
    protocol_steps.append("1. Sentence Listing:\nExtract and list every sentence from the student's response on a separate numbered line (e.g., Sentence 1: ..., Sentence 2: ...).")

    analysis_steps = []
    
    if has_sentence_count:
        analysis_steps.append("- Sentence Count check: Count the sentences you listed. If the count is NOT exactly 5, you MUST output verdict NO.")
        
    if has_word_len_range:
        analysis_steps.append("- Word Count check: Count the words in each sentence. If any sentence has fewer than 8 words or more than 15 words, you MUST output verdict NO.")
        
    if has_5_letters:
        analysis_steps.append("- 5+ Letter Words check: Verify if each sentence contains at least one word with 5 or more letters. If any sentence does not, you MUST output verdict NO.")
        
    if has_no_commas:
        analysis_steps.append("- Commas check: Check if the text contains any commas (','). If any comma is found anywhere in the response, you MUST output verdict NO.")
        
    if has_energy:
        analysis_steps.append("- 'energy' count: Count how many times the word 'energy' (case-insensitive) appears. If it appears less than 2 times, you MUST output verdict NO.")
        
    if has_diff_start:
        analysis_steps.append("- Starting Letters check: Write down the first letter of each sentence. If any letter is repeated, you MUST output verdict NO.")
        
    if has_no_word_3x:
        analysis_steps.append("- Word Frequency check: If the response is coherent English text and is longer than 30 words, it will always contain common words (like 'the', 'and', 'of', 'to') more than 3 times. If the text is longer than 30 words and contains standard paragraphs, you MUST output verdict NO immediately. If it is a list of unique words, verify if any word appears more than 3 times.")
        
    if has_unique_words:
        analysis_steps.append("- Unique Words check: If the text is extremely short or repeats the same few words, it might have fewer than 20 unique words. If so, you MUST output verdict NO.")

    analysis_text = "\n".join(analysis_steps)

    prompt = f"""You are a highly precise grading assistant. Your task is to verify if the student's response satisfies the given rules.

Task Rules:
{rules_text}

Please follow this verification protocol:
{protocol_steps[0]}

2. Rule-by-rule analysis:
{analysis_text}

3. Verdict:
Conclude your analysis with a JSON block.
If ANY of the rule checks above resulted in a NO or violation, the final verdict MUST be "NO".
Only output "YES" if ALL rules are perfectly satisfied.

Format:
{{
  "verdict": "NO"
}}
or
{{
  "verdict": "YES"
}}
Do not include any explanation or extra text after the JSON block."""
    return prompt

def prompt_g_user(solver_completion):
    return f"Student response to verify:\n\"\"\"\n{solver_completion}\n\"\"\""


def parse_verdict(response_text):
    # Align exactly with environments/curriculum_oversight/curriculum_oversight.py llm_verifier_approved
    try:
        data = json.loads(response_text.strip())
        return data.get("verdict") == "YES"
    except Exception:
        match = re.search(r'\{.*?\}', response_text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                return data.get("verdict") == "YES"
            except Exception:
                pass
                
    clean_text = response_text.strip().replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    if "verdict:YES" in clean_text:
        return True
    elif "verdict:NO" in clean_text:
        return False
    return False


async def run_query(client, system, user, max_tokens=128):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "temperature": 0.0,
        "max_tokens": max_tokens
    }
    try:
        response = await client.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


def compute_mcc(tp, tn, fp, fn):
    num = (tp * tn) - (fp * fn)
    den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return num / den if den > 0 else 0.0


async def evaluate_prompt_design(client, dataset, prompt_sys_fn, prompt_usr_fn, max_tokens=128, name="Prompt"):
    tp = tn = fp = fn = errors = 0
    
    tasks = []
    for item in dataset:
        sys_prompt = item["verifier_system_prompt_baseline"]
        # Extract rules block
        match = re.search(r"Task Rules:\n(.*?)\n\nFormat Requirement:", sys_prompt, re.DOTALL)
        rules_text = match.group(1).strip() if match else ""
        
        system = prompt_sys_fn(rules_text)
        user = prompt_usr_fn(item["solver_completion"])
        
        tasks.append((item, system, user))
        
    # Run concurrently with a semaphore
    sem = asyncio.Semaphore(10)
    async def worker(item, system, user):
        async with sem:
            response = await run_query(client, system, user, max_tokens)
            return item, response
            
    futures = [worker(item, system, user) for item, system, user in tasks]
    results = await asyncio.gather(*futures)
    
    for item, response in results:
        if response.startswith("Error:"):
            errors += 1
            continue
        
        pred_yes = parse_verdict(response)
        true_yes = item["solved_intent"] > 0.0
        
        if true_yes and pred_yes:
            tp += 1
        elif not true_yes and not pred_yes:
            tn += 1
        elif not true_yes and pred_yes:
            fp += 1
        elif true_yes and not pred_yes:
            fn += 1
            
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    mcc = compute_mcc(tp, tn, fp, fn)
    
    print(f"\nResults for {name}:")
    print(f"  Total Evaluated: {total} (Errors: {errors})")
    print(f"  True Positives (TP): {tp} | True Negatives (TN): {tn}")
    print(f"  False Positives (FP): {fp} | False Negatives (FN): {fn}")
    print(f"  Accuracy: {accuracy:.1%}")
    print(f"  False Positive Rate (FPR): {fpr:.1%}")
    print(f"  False Negative Rate (FNR): {fnr:.1%}")
    print(f"  Correlation (MCC): {mcc:.4f}")
    return mcc


async def main():
    dataset_path = "/home/emil/projects/scalable-llama/verifier_tuning_dataset.json"
    with open(dataset_path, "r") as f:
        data = json.load(f)
        
    # Create a balanced subset of size 50 (25 solved, 25 unsolved)
    solved_list = [item for item in data if item["solved_intent"] > 0.0]
    unsolved_list = [item for item in data if item["solved_intent"] == 0.0]
    
    subset = solved_list[:25] + unsolved_list[:25]
    print(f"Evaluating subset of size {len(subset)} (25 solved, 25 unsolved)...")
    
    async with httpx.AsyncClient() as client:
        print("\n--- EVALUATING DESIGN A: CLEAN BASELINE ---")
        await evaluate_prompt_design(client, subset, prompt_a_system, prompt_a_user, max_tokens=64, name="Design A (Clean Baseline)")
        
        print("\n--- EVALUATING DESIGN B: CHAIN OF THOUGHT ---")
        # Give more tokens for reasoning
        await evaluate_prompt_design(client, subset, prompt_b_system, prompt_b_user, max_tokens=256, name="Design B (Chain of Thought)")

        print("\n--- EVALUATING DESIGN C: STRICT CHECKLIST ---")
        await evaluate_prompt_design(client, subset, prompt_c_system, prompt_c_user, max_tokens=128, name="Design C (Strict Checklist)")

        print("\n--- EVALUATING DESIGN D: STRUCTURED RECIPE ---")
        await evaluate_prompt_design(client, subset, prompt_d_system, prompt_d_user, max_tokens=1024, name="Design D (Structured Recipe)")

        print("\n--- EVALUATING DESIGN E: TAIELORED RECIPE ---")
        await evaluate_prompt_design(client, subset, prompt_e_system, prompt_e_user, max_tokens=1024, name="Design E (Tailored Recipe)")

        print("\n--- EVALUATING DESIGN F: STRICT TEMPLATE ---")
        await evaluate_prompt_design(client, subset, prompt_f_system, prompt_f_user, max_tokens=1024, name="Design F (Strict Template)")

        print("\n--- EVALUATING DESIGN G: TAIELORED RECIPE WITH NEGATIVE FOCUS ---")
        await evaluate_prompt_design(client, subset, prompt_g_system, prompt_g_user, max_tokens=1024, name="Design G (Tailored Recipe Negative Focus)")

if __name__ == "__main__":
    asyncio.run(main())
