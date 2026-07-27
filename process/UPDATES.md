# Project Updates

## 2026-07-10 — Project extracted and initialized
Unzipped the starter kit (`hvhs-llm-security-starter (3).zip`) into this repo directory. Reviewed the README to confirm project scope: an evaluation of prompt injection and data leakage resistance in a simulated healthcare intake assistant, tested against local Ollama models.
```
unzip -o "hvhs-llm-security-starter (3).zip"
```

## 2026-07-10 — Environment setup started
Confirmed Ollama was already installed and running locally (found at `%LOCALAPPDATA%\Programs\Ollama\ollama.exe`, not yet on PATH). Installed the `ollama` Python package via pip per `requirements.txt`.
```
python -m pip install ollama
```

## 2026-07-10 — Pulling evaluation models
Kicked off background download of the three models used in the evaluation: `llama3.1:8b`, `mistral:7b`, and `qwen2.5:7b`. Next step once downloads finish is to run `python assistant.py` as a sanity check before executing the attack harness.
```
ollama pull llama3.1:8b && ollama pull mistral:7b && ollama pull qwen2.5:7b
```

## 2026-07-10 — All models downloaded
Confirmed via `ollama list` that all three models are present: `llama3.1:8b` (4.9 GB), `mistral:7b` (4.4 GB), `qwen2.5:7b` (4.7 GB). Environment setup is complete; next step is the sanity check (`python assistant.py`) before running the full attack harness.
```
ollama list
```

## 2026-07-10 — Sanity check run against all three models
Ran the benign cough question from `assistant.py` against all three models (not just the default `llama3.1:8b`) via a small wrapper script that calls `ask_assistant()` for each model tag in turn. `llama3.1:8b` and `mistral:7b` responded in-character and boundary-respecting; `qwen2.5:7b` crashed Ollama's `llama-server` process with a stack-buffer-overrun error (status 500) on the first attempt.
```
python sanity_check_all.py
```

## 2026-07-10 — qwen2.5:7b retry succeeded
Re-ran the same benign cough question against `qwen2.5:7b` alone and it responded normally and in-character, confirming the earlier crash was transient rather than a persistent model/runtime issue. All three models are now confirmed working; ready to run the full attack harness (`run_harness.py`) next.
```
python -c "from assistant import ask_assistant; print(ask_assistant(patient_id='P001', user_message=\"Hi, I've had this cough for a few days, should I be worried?\", model='qwen2.5:7b'))"
```

## 2026-07-11 — First harness run hung, stopped and diagnosed
The first `run_harness.py` background run showed zero output and zero progress after an extended period. Killed the task and confirmed the low CPU usage was a red herring (a blocked client uses ~0% CPU); the real issue was CPU-only inference (no GPU acceleration) making each call slow, plus buffered stdout hiding progress. Restarted with unbuffered output redirected to a log file to make progress observable.
```
python -u run_harness.py > harness_run.log 2>&1
```

## 2026-07-17 — Full attack harness run completed
All 111 calls (36 attacks + 1 baseline, across `llama3.1:8b`, `mistral:7b`, `qwen2.5:7b`) completed with zero errors or crashes. Results are saved to `results/run_20260717_112547.csv`. Next step per the harness's own instructions: manually label each row Success/Partial/Failed against the `goal` field in `attacks.json`, per `SCORING_RUBRIC.md`.
```
grep -c "Traceback\|ResponseError" harness_run.log   # 0 errors confirmed
```

## 2026-07-17 — Manual scoring pass completed
Read and labeled all 108 attack responses (36 attacks x 3 models) against `SCORING_RUBRIC.md`, writing labels + rationale to `results/run_20260717_112547_scored.csv` and a stats summary to `results/scoring_summary.md`. Headline: `mistral:7b` is the leakiest model (8 Successes, notably confirming "I am DAN" and "Override accepted" verbatim), `indirect_injection` is the best-defended category overall (only 1 Success across all 108 rows), and `system_prompt_extraction` is the weakest-defended category (every model leaked its full system prompt at least once via reformatting tricks like code-block or translation requests).
```
python -c "# small script that merged scores_llama.json / scores_mistral.json / scores_qwen.json into the scored CSV"
```

## 2026-07-17 — Writeup drafted, NIST/HIPAA risk mapping complete
Filled in every bracketed section of `WRITEUP_SKELETON.md` into a new `WRITEUP.md`, using the scored results directly: abstract, results tables, a direct-vs-indirect injection comparison (18.0% vs 5.6% success rate), four notable-case writeups, NIST AI RMF (Govern/Map/Measure/Manage) and HIPAA minimum-necessary risk mapping, per-category mitigation recommendations, and limitations/future work. Updated `README.md`'s status checklist accordingly; publication itself is still pending.
