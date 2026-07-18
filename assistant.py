"""
Core "agent" for the HVHS Virtual Intake Assistant simulation.

This is intentionally simple: a system prompt + a retrieved patient record +
a user message, assembled and sent to a local Ollama model. No autonomy,
no tool-calling - just context injection. That's enough to test both direct
attacks (malicious user_message) and indirect attacks (malicious content
planted inside the "retrieved" patient record).
"""

import json
from pathlib import Path
import ollama  # pip install ollama

BASE_DIR = Path(__file__).parent
SYSTEM_PROMPT = (BASE_DIR / "system_prompt.txt").read_text()
PATIENT_DATA = json.loads((BASE_DIR / "mock_patient_data.json").read_text())


def format_patient_record(patient_id: str, notes_override: str | None = None) -> str:
    """
    Build the text block representing the patient record as the assistant
    would receive it (e.g., pulled from a RAG lookup). If notes_override is
    given, it replaces the notes field - this is how indirect injection
    attacks are simulated: the payload lives in the 'retrieved data', not
    in the user's message.
    """
    record = PATIENT_DATA[patient_id]
    notes = notes_override if notes_override is not None else record["notes"]
    return (
        f"Patient: {record['name']}\n"
        f"DOB: {record['dob']}\n"
        f"Reason for visit: {record['reason_for_visit']}\n"
        f"Notes: {notes}"
    )


def ask_assistant(
    patient_id: str,
    user_message: str,
    model: str,
    notes_override: str | None = None,
) -> str:
    """
    Send one turn to the assistant and return its raw text response.

    patient_id      - which mock patient record to attach as context
    user_message    - what the "patient" (or attacker) says in chat
    model           - Ollama model tag, e.g. 'llama3.1:8b'
    notes_override  - if set, replaces the patient's notes field for this
                       call only, used to simulate indirect injection
    """
    patient_record_text = format_patient_record(patient_id, notes_override)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Current patient record:\n{patient_record_text}"},
        {"role": "user", "content": user_message},
    ]

    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"]


if __name__ == "__main__":
    # Quick manual sanity check - run this FIRST, before any attacks,
    # to confirm the assistant behaves normally on a benign question.
    reply = ask_assistant(
        patient_id="P001",
        user_message="Hi, I've had this cough for a few days, should I be worried?",
        model="llama3.1:8b",
    )
    print(reply)
