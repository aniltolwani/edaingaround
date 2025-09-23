# Pack: anomaly_surge

**Goal:** Practice robust JSON loading (invalid lines, BOM, control chars), normalization, and targeted plots.

## Closed-ended tasks
1) Build a tolerant loader. Report `rows_parsed` and `error_counts` (with keys: truncated, jsonerror, control_char, bom).
2) Normalize: coerce `rating` to 1..5 ints when possible; `text` to string; keep a count of `empty_text_count`.
3) Compute `p95_text_length` and a `rating_hist` dict (1..5).
4) Plots: save `length_hist.html` (hist of text lengths) and `rating_bar.html`.

## Output (result.json)
```
{
  "rows_parsed": int,
  "error_counts": {"truncated": int, "jsonerror": int, "control_char": int, "bom": int},
  "rating_hist": {"1": int, "2": int, "3": int, "4": int, "5": int},
  "p95_text_length": int,
  "empty_text_count": int
}
```
