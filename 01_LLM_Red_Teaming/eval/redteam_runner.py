import openai
import os
from log_utils import load_attacks, log_result, score_response

# -------------------------------
# Configuration
# -------------------------------

MODEL_NAME = "gpt-3.5-turbo"  # Replace with any model you want
openai.api_key = os.getenv("OPENAI_API_KEY")  # You will set this locally only

# -------------------------------
# LLM Call Helper
# -------------------------------

def query_model(prompt):
    """Send prompt to the model and return response text."""
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ERROR: {e}"

# -------------------------------
# Evaluation Runner
# -------------------------------

def run_redteam_evaluation():
    print("Starting LLM Red Teaming Evaluation...\n")

    attacks = {
        "jailbreaks": load_attacks("../attacks/jailbreaks.md"),
        "prompt_injection": load_attacks("../attacks/prompt_injection.md"),
        "safety_bypass": load_attacks("../attacks/safety_bypass.md")
    }

    for attack_type, prompts in attacks.items():
        print(f"Running attack type: {attack_type} ({len(prompts)} prompts)")

        for prompt in prompts:
            response = query_model(prompt)
            log_result(MODEL_NAME, attack_type, prompt, response)

            score = score_response(response)

            print(f"- Prompt: {prompt[:40]}...")
            print(f"  Response Score: {score}")
            print("  Logged.\n")

    print("Evaluation Completed. Logs saved to eval_logs.jsonl.")

# -------------------------------
# Run if executed directly
# -------------------------------
if __name__ == "__main__":
    run_redteam_evaluation()
