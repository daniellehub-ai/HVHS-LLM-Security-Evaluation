# HVHS Virtual Intake Assistant — LLM Security Evaluation

An empirical evaluation of prompt injection and data leakage resistance in a
simulated healthcare-context LLM assistant, run against multiple local
open-weight models via Ollama.

This project is part of a broader AI security/governance portfolio
(see the related HVHS AI Governance Capstone) and is intentionally scoped
as a RAG-style context-injection assistant rather than a tool-calling
agent, to keep the threat surface focused and the results reproducible.

📊 [**View the live dashboard**](https://daniellehub-ai.github.io/HVHS-LLM-Security-Evaluation/dashboard.html)

## Setup

1. Install [Ollama](https://ollama.com).
2. Pull the models used in this evaluation:
   ```bash
   ollama pull llama3.1:8b
   ollama pull mistral:7b
   ollama pull qwen2.5:7b
   ```
3. Install Python dependencies:
   ```bash
   pip install ollama --break-system-packages
   ```
4. Sanity check the assistant works normally before running any attacks:
   ```bash
   python assistant.py
   ```
   You should see a plausible, in-character response to a benign symptom question.

## Project structure

```
system_prompt.txt        - the assistant's role and boundaries
mock_patient_data.json   - synthetic, non-real patient records used as context
attacks.json             - the attack taxonomy and prompt set (36 attacks, 6 categories)
SCORING_RUBRIC.md        - how to label results after a harness run
WRITEUP.md               - completed draft writeup with results filled in
assistant.py             - core function: assembles prompt, calls Ollama
run_harness.py           - runs every attack against every model, logs results
process/                 - planning docs, dated work log, and writeup skeleton
results/                 - timestamped CSV output, scoring summary, and harness run log
```

## How it works

Each turn sent to the model is assembled from three parts:
1. The system prompt (its role and boundaries)
2. The "retrieved" patient record for the current patient
3. The user's chat message

**Direct attacks** put the malicious content in the user message.
**Indirect attacks** put the malicious content inside the patient record's
`notes` field instead — simulating a compromised or adversarial document
that the assistant reads as data, not as an instruction from the user.

## Threat model / what counts as a "successful" attack

See the `goal` field on each entry in `attacks.json`. Broadly:
- The assistant reveals its system prompt
- The assistant discloses another patient's information
- The assistant provides a diagnosis or specific medication dosage
- The assistant abandons its persona/role under a jailbreak framing
- The assistant treats attacker-controlled data as a command (indirect injection)

## Status

- [x] Assistant scaffold + baseline sanity check
- [x] Attack set (36 prompts, balanced across 6 categories)
- [x] Scoring rubric defined (see SCORING_RUBRIC.md)
- [x] Writeup skeleton drafted (see WRITEUP_SKELETON.md)
- [x] Run full harness across all 3 models
- [x] Manual scoring pass (Success / Partial / Failed / Incoherent)
- [x] Analysis + NIST AI RMF / HIPAA risk mapping
- [x] Writeup drafted (see WRITEUP.md) — [ ] publication still pending

## Frameworks referenced

- OWASP Top 10 for LLM Applications
- NIST AI RMF / NIST AI 600-1 (Generative AI Profile)
- HIPAA (for healthcare data exposure framing)

## Disclaimer

All patient data in this repository is synthetic. No real patient
information, PHI, or production systems are used or referenced.

## License

© 2026 Danielle Hendon. All rights reserved.

This repository is shared publicly for portfolio and demonstration
purposes. No part of this project — code, data, methodology, or
writeup — may be copied, reused, or redistributed without permission.
