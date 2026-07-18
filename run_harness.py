"""
Runs the full attack set (attacks.json) against each configured model and
logs raw responses to a timestamped CSV. Scoring is deliberately NOT done
here - collect first, read the outputs, THEN decide how to score them.
"""

import json
import csv
from datetime import datetime
from pathlib import Path

from assistant import ask_assistant

BASE_DIR = Path(__file__).parent

MODELS = [
    "llama3.1:8b",
    "mistral:7b",
    "qwen2.5:7b",
]

BENIGN_PROBE = "Hi, I wanted to report my symptoms for today's visit."


def load_attacks():
    return json.loads((BASE_DIR / "attacks.json").read_text())


def run():
    attacks = load_attacks()
    results = []

    for model in MODELS:
        print(f"\n=== Running model: {model} ===")

        # Baseline sanity check per model: confirm normal behavior before attacking
        baseline = ask_assistant("P001", BENIGN_PROBE, model=model)
        results.append({
            "model": model,
            "attack_id": "BASELINE",
            "category": "baseline_sanity_check",
            "type": "n/a",
            "target_patient": "P001",
            "prompt_used": BENIGN_PROBE,
            "response": baseline,
        })

        for attack in attacks:
            print(f"  -> {attack['id']} ({attack['category']})")

            if attack["type"] == "direct":
                response = ask_assistant(
                    patient_id=attack["target_patient"],
                    user_message=attack["payload"],
                    model=model,
                )
                prompt_used = attack["payload"]

            elif attack["type"] == "indirect":
                # Payload is planted in the patient record, not the user message.
                # The user message stays benign - that's the point of indirect injection.
                response = ask_assistant(
                    patient_id=attack["target_patient"],
                    user_message="Can you summarize my visit so far?",
                    model=model,
                    notes_override=attack["payload"],
                )
                prompt_used = f"[injected into notes] {attack['payload']}"

            else:
                raise ValueError(f"Unknown attack type: {attack['type']}")

            results.append({
                "model": model,
                "attack_id": attack["id"],
                "category": attack["category"],
                "type": attack["type"],
                "target_patient": attack["target_patient"],
                "prompt_used": prompt_used,
                "response": response,
            })

    # Write results
    out_dir = BASE_DIR / "results"
    out_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"run_{timestamp}.csv"

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "model", "attack_id", "category", "type",
            "target_patient", "prompt_used", "response"
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. Results written to {out_path}")
    print("Next: open the CSV and manually label each row Success / Partial / Failed")
    print("against the 'goal' field in attacks.json, before writing any scoring code.")


if __name__ == "__main__":
    run()
