# Pack: code_ast_pro

**Goal:** Practice AST-driven analysis, series transforms, indexing, and meaningful plots for code data.**

## Closed-ended tasks
1) **Python**: parse rate (`py_parse_rate`), total function defs (`py_total_funcs`), and count of branch nodes (`py_branch_nodes` ~ If/For/While/Try).
2) **Danger patterns**: counts for `["eval","exec","open(","subprocess","pickle.loads","yaml.load("]` across all code.
3) **JS**: `js_eval_count` (rows with `eval(`) and `long_lines_over_200` across all langs.
4) **Top calls**: top 5 call names (lower-cased) as dict counts under `top_calls`.
5) **Plots**: 
   - `cyclomatic_hist_py.html` (hist of cyclomatic~`branches+1` for parsed Python rows)
   - `lang_breakdown.html` (bar of rows by `lang`)

## Output (result.json)
```
{
  "rows": int,
  "py_parse_rate": float,
  "py_total_funcs": int,
  "py_branch_nodes": int,
  "danger_counts": {"eval": int, "exec": int, "open(": int, "subprocess": int, "pickle.loads": int, "yaml.load(": int},
  "js_eval_count": int,
  "long_lines_over_200": int,
  "top_calls": {"name": count, ...}
}
```
