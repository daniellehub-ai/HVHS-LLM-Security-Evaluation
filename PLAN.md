# Project Plan — HVHS LLM Security Evaluation

Full start-to-finish plan for this project, with completed work marked so
this doubles as a status tracker. See `UPDATES.md` for a dated log of what
happened during execution; this file is the structural plan, not the log.

---

## Phase 0 — Design (pre-existing, done before this session)

- [x] Define the simulated system: HVHS Virtual Intake Assistant (system
      prompt + retrieved patient record + user message, no tool-calling)
- [x] Write `system_prompt.txt` (role + strict boundaries)
- [x] Write `mock_patient_data.json` (6 synthetic patients)
- [x] Design attack taxonomy: 6 categories x 6 attacks = 36 attacks
      (`attacks.json`) — direct_override, system_prompt_extraction,
      pii_exfiltration_cross_patient, unsafe_medical_advice,
      role_play_jailbreak, indirect_injection
- [x] Write `SCORING_RUBRIC.md` (Success/Partial/Failed/Incoherent labels
      + category-specific scoring notes)
- [x] Write `WRITEUP_SKELETON.md` (paper structure, kept as a template)
- [x] Write `assistant.py` (core prompt-assembly + Ollama call) and
      `run_harness.py` (runs every attack against every model, logs CSV)

## Phase 1 — Environment setup

- [x] Confirm Ollama installed and running locally
- [x] Install Python dependency (`pip install ollama`, per `requirements.txt`)
- [x] Pull all 3 evaluation models: `llama3.1:8b`, `mistral:7b`, `qwen2.5:7b`
- [x] Sanity check: run `assistant.py` against a benign question, confirm
      in-character, boundary-respecting response — done for all 3 models
      (one transient crash on qwen2.5:7b's first attempt; retry succeeded)

## Phase 2 — Execution

- [x] Run the full attack harness (`run_harness.py`): 36 attacks + 1 baseline
      per model x 3 models = 111 calls
  - [x] Diagnose and recover from a stuck first run (unbuffered output +
        logging to a file to make progress observable; root cause was slow
        CPU-only inference combined with buffered stdout, not an actual hang)
  - [x] Confirm zero errors/crashes across the full 111-call run
  - Output: `results/run_20260717_112547.csv`

## Phase 3 — Manual scoring

- [x] Read and label all 108 attack-response rows (36 attacks x 3 models)
      against `SCORING_RUBRIC.md`, with a short rationale per row
  - [x] llama3.1:8b (37 rows)
  - [x] mistral:7b (37 rows)
  - [x] qwen2.5:7b (37 rows)
- [x] Compile labels + rationale into `results/run_20260717_112547_scored.csv`
- [x] Calculate summary statistics (success/partial/incoherent rate per
      model, per category, direct-vs-indirect comparison) —
      `results/scoring_summary.md`

## Phase 4 — Analysis & risk mapping

- [x] NIST AI RMF mapping (Govern / Map / Measure / Manage) against findings
- [x] HIPAA exposure framing (minimum necessary standard, impermissible
      disclosure risk) for the cross-patient PII findings specifically
- [x] Per-category mitigation recommendations
- All captured in `WRITEUP.md` Section 5

## Phase 5 — Writeup

- [x] Fill in every bracketed section of `WRITEUP_SKELETON.md` into a
      completed draft: `WRITEUP.md`
  - [x] Abstract
  - [x] Introduction, Related Work (with citations)
  - [x] Methodology (system under test, models, attack taxonomy, scoring)
  - [x] Results (overall, by category, direct vs. indirect, notable cases)
  - [x] Risk mapping (NIST AI RMF, HIPAA, mitigations)
  - [x] Limitations, Future Work, Conclusion
- [ ] Copyedit / proofread pass on `WRITEUP.md`
- [ ] Decide where this fits alongside the related HVHS AI Governance
      Capstone (cross-reference or merge?)

## Phase 6 — Publication (not started — decision pending)

- [ ] Decide publication venue/format (portfolio site, blog post, PDF,
      LinkedIn/GitHub README highlight, etc.)
- [ ] Final read-through against the published venue's constraints (length,
      formatting, whether raw CSVs get published alongside or just linked)
- [ ] Publish
- [ ] Confirm `results/` git-ignore behavior is correct before pushing
      (per README: keep only the final analyzed run committed, not every
      raw timestamped CSV generated during iteration)

## Phase 7 — Future work (explicitly out of scope for this pass)

These are the concrete next-study ideas already identified in
`WRITEUP.md` Section 7 — listed here so the plan reflects the project's
full arc, not just what's scheduled next:

- [ ] Expand to a tool-calling agent architecture (the "Option B" system
      design mentioned in the README, vs. this study's RAG-style scope)
- [ ] Multi-turn attack sequences (this study is single-turn only; several
      Partial results, e.g. llama3.1:8b's role-play agreements, are
      strongly suggestive of a multi-turn follow-up vulnerability that a
      single-turn design can't confirm)
- [ ] Larger and/or proprietary frontier model comparison
- [ ] Automated scoring / LLM-judge validation against the manual labels,
      including an inter-rater reliability check (no second rater was used
      in Phase 3)
- [ ] Structural mitigations testbed — actually build and test whether the
      delimiter/classifier-based defenses recommended in Section 5.3
      measurably reduce the success rates found in this study

---

## Where things stand right now

Everything through Phase 5's core drafting is done. What's left is
editorial (copyedit, decide how this relates to the Capstone) and a
publication decision that's the user's call, not a technical task — see
Phase 6. Phase 7 is a backlog of follow-on studies, not committed work.
