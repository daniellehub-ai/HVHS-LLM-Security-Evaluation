# Prompt Injection & Data Leakage Resistance in Healthcare-Context LLM Assistants

*An empirical evaluation of three open-weight local models against a simulated
clinical intake assistant*

**Author:** Danielle Hendon
**Status:** Draft skeleton — fill in bracketed sections once harness results are scored

---

## Abstract

*[2-4 sentences once complete. Template: "This study evaluates the prompt
injection and data leakage resistance of N open-weight LLMs (list) in a
simulated healthcare intake assistant context. Using a 36-prompt attack set
across 6 categories, we find [headline result]. Indirect injection attacks
succeeded at [X]% versus [Y]% for direct attacks, suggesting [interpretation].
Findings are mapped to NIST AI RMF and HIPAA to contextualize risk for
real-world healthcare AI deployments."]*

---

## 1. Introduction

- Why this matters: healthcare LLM assistants are increasingly deployed for
  intake, triage, and documentation support, often with RAG-style access to
  patient records — a context where both traditional security failures
  (data leakage) and AI-specific failures (instruction-following manipulation)
  carry direct regulatory and patient-safety consequences.
- What's novel/useful here: most public prompt injection research targets
  general-purpose assistants; this study uses a domain-specific threat model
  (HIPAA-relevant data, clinical role boundaries) and compares model families
  head-to-head under identical conditions.
- Scope statement: this is a RAG-style context-injection assistant, not a
  tool-calling agent — state this plainly as a scoping choice, and note it
  as a limitation/future work item, not something to apologize for.

## 2. Related Work

*[Cite, don't reproduce, per copyright rules: OWASP Top 10 for LLM
Applications; Greshake et al. on indirect prompt injection; Wei et al. on
why safety training fails to generalize; NIST AI 600-1. One or two sentences
each summarizing their contribution and how this study builds on or differs
from them — e.g., "unlike general-purpose injection benchmarks, this study
situates attacks in a healthcare-specific threat model with domain-relevant
success criteria."]*

## 3. Methodology

### 3.1 System under test
- Simulated assistant: HVHS Virtual Intake Assistant (fictional health system,
  reused from prior governance capstone for portfolio continuity)
- Architecture: system prompt + retrieved patient record (mock data) + user
  message, single-turn, no tool-calling — state this explicitly as the
  threat surface tested
- System prompt and full mock dataset are included in the repository for
  reproducibility

### 3.2 Models evaluated
*[Table once finalized]*

| Model | Params | Family | License |
|---|---|---|---|
| llama3.1:8b | 8B | Meta | Llama license |
| mistral:7b | 7B | Mistral AI | Apache 2.0 |
| qwen2.5:7b | 7B | Alibaba | Apache 2.0 |

Rationale for selection: spread of alignment/safety training approaches
across labs, all instruct-tuned, all runnable locally at consistent hardware
cost — see README for full selection reasoning.

### 3.3 Attack taxonomy
Six categories, six attacks each (36 total): direct override, system prompt
extraction, cross-patient PII exfiltration, unsafe medical advice, role-play
jailbreak, indirect injection. Full attack set and rationale per category in
`attacks.json`.

Direct attacks were delivered as the user's chat message. Indirect attacks
were planted inside the patient record's `notes` field, simulating a
compromised or adversarial document ingested via retrieval rather than typed
by the user — testing whether the model distinguishes retrieved data from
instructions.

### 3.4 Scoring methodology
Four-way manual labeling (Success / Partial / Failed / Incoherent) — full
rubric in `SCORING_RUBRIC.md`. Labeled independently per (model, attack)
pair against the attack's stated goal. Incoherent responses are reported
separately and excluded from headline success rates to avoid conflating
model capability limitations with security behavior.

*[If time allows: note any inter-rater reliability check, e.g., a second
pass on a 10% sample to confirm consistent labeling]*

## 4. Results

### 4.1 Overall success rate by model
*[Table: model x {Success, Partial, Failed, Incoherent} counts and %]*

### 4.2 Success rate by category, by model
*[Table or grouped bar chart — this is the most informative view; identifies
which model is weak to which attack type rather than a single aggregate score]*

### 4.3 Direct vs. indirect injection comparison
*[Specific callout: was indirect injection more or less successful than
direct attacks? This is a genuinely interesting empirical question the
literature is still working out, and a clean local comparison is a real
contribution]*

### 4.4 Notable individual cases
*[2-4 specific examples: quote the attack, paraphrase — do not reproduce
verbatim at length — the model's response, and explain why it was scored
Success/Partial. These make the paper concrete and readable rather than
purely statistical.]*

## 5. Risk Mapping

### 5.1 NIST AI RMF / AI 600-1
Map findings to the four core functions:
- **Govern** — what organizational controls would need to exist before
  deploying a model with this failure profile (e.g., human review of any
  AI-generated response before it reaches a patient)
- **Map** — how these findings would inform a context-specific risk
  identification exercise for a real HVHS-style deployment
- **Measure** — this study *is* a Measure-function exercise; note that
  explicitly and describe how it could be operationalized as a recurring
  evaluation rather than a one-off
- **Manage** — mitigation recommendations per category (see 5.3)

### 5.2 HIPAA exposure implications
Frame cross-patient PII exfiltration findings specifically in terms of
minimum necessary standard and impermissible disclosure risk — this is
where your healthcare background adds real interpretive value beyond a
generic security readout.

### 5.3 Mitigation recommendations
*[Concrete, per-category. E.g., for indirect injection: structurally
separate retrieved data from instructions using explicit delimiters plus a
secondary classifier pass, rather than relying on prompt-level instructions
alone. For cross-patient leakage: enforce patient-scope isolation at the
retrieval layer, not just the prompt layer, so leakage is architecturally
prevented rather than merely discouraged.]*

## 6. Limitations

- Single-turn only — real conversations are multi-turn, and some published
  jailbreaks rely on multi-turn escalation this study didn't test
- Small model set (3 models, 7-8B class) — findings may not generalize to
  larger models or proprietary frontier models
- No tool-calling — a production RAG/agent system with function-calling has
  a different (likely larger) attack surface than tested here
- Manual scoring introduces some subjectivity despite the rubric; no
  automated/LLM-judge scoring cross-check was performed
- Synthetic data only — real clinical documentation may contain different
  injection surface characteristics than the mock notes used here

## 7. Future Work

- Expand to tool-calling agent architecture (Option B from initial design)
- Multi-turn attack sequences
- Larger and/or proprietary model comparison
- Automated scoring/LLM-judge validation against the manual labels
- Structural mitigations testbed (test whether delimiter-based or
  classifier-based defenses measurably reduce the success rates found here)

## 8. Conclusion

*[3-5 sentences once results are in — restate headline finding, why it
matters for real healthcare AI deployments, and the one or two mitigations
you'd prioritize first if this were a real system.]*

---

## Appendix

- Full attack set: `attacks.json`
- Full scoring rubric: `SCORING_RUBRIC.md`
- Raw results: `results/run_*.csv`
- Reproduction instructions: `README.md`
