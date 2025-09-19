# Mock LLM-Data EDA Packs — HOWTO

Each pack mimics the interview: **~1000 JSON/JSONL/(some .gz)** files, messy schema.

## What’s inside each pack
- `README.md` — closed‑ended tasks
- `answers.json` — ground truth (peek only after a timed attempt)
- `grader_stub.py` — pack-specific checker
- `result_template.json` — keys you should output

A **universal grader** is available at the root: `universal_grader.py`.

## Quickstart
1. Unzip a pack locally (e.g., `pack_mixed_chat.zip`).
2. Write/launch your notebook or script.
3. Load JSON/JSONL/.gz recursively, tolerate bad rows, attach `_file` & `_row`.
4. Normalize into columns: `{id, source, prompt, response, text, ts}` (choose main `text`).
5. Compute the metrics in that pack’s `README.md`.
6. Save your answers to `result.json` in the pack folder.
7. Grade with either:
   - `python grader_stub.py result.json`  (from inside the pack)
   - `python /path/to/universal_grader.py /path/to/pack_dir /path/to/result.json`

## Output keys by pack

**Mixed Chat EDA**
- rows (int)
- exact_dup_rate (float)
- dup_rate_by_source (dict: {source -> float})
- token_total_est (int)
- token_p95_est (int)
- token_top5_share (float)
- pii_email_count (int)
- pii_phone_count (int)
- aiish_count (int)
- spam_count (int)

**Instructions + Ratings**
- rows (int)
- exact_dup_rate (float)
- token_p95_est (int)
- category_counts (dict: {category -> int})
- avg_response_length_by_rating (dict: {1..5 -> float})
- empty_high_rating_count (int)

**Code Mini**
- rows (int)
- exact_dup_rate (float)
- py_parse_rate (float)
- eval_exec_open_count (int)
- longline_over_200_count (int)

## Tolerances
- Floats are compared with tolerant rounding:
  - exact_dup_rate, token_top5_share, py_parse_rate: 3 decimals
  - dup_rate_by_source: 3 decimals
  - avg_response_length_by_rating: 1 decimal

Good luck — time yourself for 45 minutes per pack, then run the grader.
