#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, json, pathlib

USAGE = """\
Usage:
  python universal_grader.py /path/to/pack_dir /path/to/result.json

Notes:
- The script compares your result.json against the pack's answers.json.
- Floats are compared with tolerant rounding:
    * exact_dup_rate, token_top5_share, py_parse_rate: 3 decimals
    * nested dup_rate_by_source: 3 decimals
    * avg_response_length_by_rating: 1 decimal
- All other numeric keys are compared exactly.

# example for Mixed Chat
python universal_grader.py /path/to/pack_mixed_chat /path/to/pack_mixed_chat/result.json
"""

ROUND_FLOATS = {
    "exact_dup_rate": 3,
    "token_top5_share": 3,
    "py_parse_rate": 3,
}

DICT_FLOAT_ROUND = {
    "dup_rate_by_source": 3,
    "avg_response_length_by_rating": 1,
}

OPTIONAL_KEYS = set([
    "files", "source_file_counts", "token_total_est_by_source"
])

def _compare_simple(key, got, want, diffs):
    if isinstance(want, float):
        prec = ROUND_FLOATS.get(key, 3)
        try:
            g = float(got)
        except Exception:
            diffs.append(f"TYPE {key}: expected float-like, got {type(got)}")
            return False
        if round(g, prec) != round(float(want), prec):
            diffs.append(f"DIFF {key}: got {got}, want {want} (rounded to {prec})")
            return False
        return True
    else:
        if got != want:
            diffs.append(f"DIFF {key}: got {got}, want {want}")
            return False
        return True

def _compare_dict(key, got, want, diffs):
    ok = True
    if key == "dup_rate_by_source":
        for src, target in want.items():
            g = got.get(src, None)
            if g is None:
                diffs.append(f"MISSING dup_rate_by_source[{src}]")
                ok = False
                continue
            try:
                gval = float(g)
            except Exception:
                diffs.append(f"TYPE dup_rate_by_source[{src}]: expected float-like, got {type(g)}")
                ok = False
                continue
            if round(gval, DICT_FLOAT_ROUND[key]) != round(float(target), DICT_FLOAT_ROUND[key]):
                diffs.append(f"DIFF dup_rate_by_source[{src}]: got {g}, want {target} (rounded to {DICT_FLOAT_ROUND[key]})")
                ok = False
    elif key == "category_counts":
        for cat, target in want.items():
            g = got.get(cat, None)
            if g != target:
                diffs.append(f"DIFF category_counts[{cat}]: got {g}, want {target}")
                ok = False
    elif key == "avg_response_length_by_rating":
        for rk, target in want.items():
            g = got.get(str(rk), got.get(int(rk), None))
            if g is None:
                diffs.append(f"MISSING avg_response_length_by_rating[{rk}]")
                ok = False
                continue
            try:
                gval = float(g)
            except Exception:
                diffs.append(f"TYPE avg_response_length_by_rating[{rk}]: expected float-like, got {type(g)}")
                ok = False
                continue
            if round(gval, DICT_FLOAT_ROUND[key]) != round(float(target), DICT_FLOAT_ROUND[key]):
                diffs.append(f"DIFF avg_response_length_by_rating[{rk}]: got {g}, want {target} (rounded to {DICT_FLOAT_ROUND[key]})")
                ok = False
    else:
        if got != want:
            diffs.append(f"DIFF {key} dict: got {got}, want {want}")
            ok = False
    return ok

def main():
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(2)
    pack_dir = pathlib.Path(sys.argv[1])
    result_path = pathlib.Path(sys.argv[2])
    ans_path = pack_dir / "answers.json"
    if not ans_path.exists():
        print(f"ERROR: answers.json not found in {pack_dir}")
        sys.exit(2)
    if not result_path.exists():
        print(f"ERROR: result.json not found at {result_path}")
        sys.exit(2)

    answers = json.load(open(ans_path, "r", encoding="utf-8"))
    result  = json.load(open(result_path, "r", encoding="utf-8"))

    required_keys = [k for k in answers.keys() if k not in OPTIONAL_KEYS and k not in ("pack",)]
    diffs = []
    ok = True

    for k in required_keys:
        if k not in result:
            diffs.append(f"MISSING key: {k}")
            ok = False

    for k in required_keys:
        if k not in result:
            continue
        got, want = result[k], answers[k]
        if isinstance(want, dict):
            if not isinstance(got, dict):
                diffs.append(f"TYPE {k}: expected dict, got {type(got)}")
                ok = False
                continue
            if not _compare_dict(k, got, want, diffs):
                ok = False
        elif isinstance(want, (int, float)):
            if not _compare_simple(k, got, want, diffs):
                ok = False
        else:
            if got != want:
                diffs.append(f"DIFF {k}: got {got}, want {want}")
                ok = False

    if ok:
        print("PASS")
        sys.exit(0)
    else:
        print("\n".join(diffs))
        print("FAIL")
        sys.exit(1)

if __name__ == "__main__":
    main()
