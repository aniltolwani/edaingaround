#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, gzip
from pathlib import Path
import pandas as pd
import plotly.express as px

def robust_iter(root):
    errors = {"truncated":0,"jsonerror":0,"control_char":0,"bom":0}
    def gen():
        for fp in Path(root).rglob("*.json*"):
            if fp.suffix == ".gz":
                f = gzip.open(fp, "rt", encoding="utf-8", errors="ignore")
            else:
                f = open(fp, "r", encoding="utf-8", errors="ignore")
            head = f.read(2048); f.seek(0)
            if head.strip().startswith("["):
                try:
                    arr = json.load(f)
                    for o in arr:
                        yield o
                except Exception:
                    errors["jsonerror"] += 1
            else:
                for line in f:
                    if not line.strip(): continue
                    # count BOM/control char heuristically
                    if line.startswith("\ufeff"): errors["bom"] += 1
                    if "\x00" in line: errors["control_char"] += 1
                    try:
                        yield json.loads(line.lstrip("\ufeff"))
                    except json.JSONDecodeError:
                        # guess truncated vs generic
                        errors["jsonerror"] += 1
            f.close()
    return gen(), errors

def main():
    root = Path(__file__).parent
    it, err = robust_iter(root)
    rows = list(it)
    rows_parsed = len(rows)
    # normalize
    for r in rows:
        r["text"] = str(r.get("text","") or "")
        try:
            val = int(r.get("rating", None))
        except Exception:
            val = None
        r["rating_norm"] = val if (val is not None and 1 <= val <= 5) else None
    import pandas as pd
    df = pd.DataFrame(rows)
    empty_text_count = int((df["text"].str.strip()=="").sum())
    rating_hist = {str(k): int((df["rating_norm"]==k).sum()) for k in range(1,6)}
    lens = df["text"].str.len().sort_values().tolist()
    p95 = int(lens[int(0.95*len(lens))-1]) if lens else 0
    # plots
    px.histogram(df, x=df["text"].str.len(), nbins=60, title="Text length").write_html(str(root/"length_hist.html"))
    px.bar(pd.Series(rating_hist).reset_index().rename(columns={"index":"rating",0:"count"}),
           x="rating", y="count", title="Rating histogram").write_html(str(root/"rating_bar.html"))
    out = {
      "rows_parsed": int(rows_parsed),
      "error_counts": {k:int(v) for k,v in err.items()},
      "rating_hist": rating_hist,
      "p95_text_length": int(p95),
      "empty_text_count": int(empty_text_count)
    }
    (root/"result.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))

if __name__=="__main__":
    main()
