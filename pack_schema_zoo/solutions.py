#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, gzip, glob, os
from pathlib import Path
import pandas as pd
import plotly.express as px
import hashlib

def md5(s): return hashlib.md5(s.encode("utf-8","ignore")).hexdigest()

def iter_json_records(root):
    exts = ("*.json","*.jsonl","*.json.gz","*.jsonl.gz")
    for pat in exts:
        for fp in Path(root).rglob(pat):
            try:
                if fp.suffix == ".gz":
                    import gzip
                    f = gzip.open(fp, "rt", encoding="utf-8", errors="ignore")
                    close = True
                else:
                    f = open(fp, "r", encoding="utf-8", errors="ignore")
                    close = True
                head = f.read(2048); f.seek(0)
                if head.strip().startswith("["):
                    arr = json.load(f)
                    for obj in arr:
                        if isinstance(obj, dict):
                            obj["_file"]=fp.name; yield obj
                else:
                    for line in f:
                        line=line.strip()
                        if not line: continue
                        try:
                            obj=json.loads(line)
                            if isinstance(obj, dict):
                                obj["_file"]=fp.name; yield obj
                        except json.JSONDecodeError:
                            continue
                if close: f.close()
            except Exception:
                continue

def flatten_tags(obj):
    tags = []
    m = obj.get("meta")
    if isinstance(m, dict) and isinstance(m.get("tags"), list):
        for t in m["tags"]:
            if isinstance(t, str): tags.append(t)
    if isinstance(m, list):
        for kv in m:
            if kv.get("k")=="tag" and isinstance(kv.get("v"), str):
                tags.append(kv["v"])
    return tags

def main():
    root = Path(__file__).parent
    rows = []
    for rec in iter_json_records(root):
        rows.append(rec)
    import pandas as pd
    df = pd.DataFrame(rows)
    rows_n = len(df)
    unique_ids = df["id"].nunique()
    # id collisions
    df["_hash"]=df.apply(lambda r: md5(json.dumps({k:r[k] for k in r.index if not str(k).startswith("_")}, sort_keys=True, ensure_ascii=False)), axis=1)
    colls = df.groupby("id")["_hash"].nunique()
    id_collision_count = int((colls>1).sum())
    # missingness / presence
    pres = df.notna().sum().sort_values(ascending=False).head(15).reset_index()
    pres.columns=["key","present"]
    fig1 = px.bar(pres, x="key", y="present", title="Top-15 key presence")
    fig1.write_html(str(root/"schema_missingness.html"))
    # tags
    df["__tags__"]=df.apply(flatten_tags, axis=1)
    import itertools
    all_tags = list(itertools.chain.from_iterable(df["__tags__"].tolist()))
    tag_counts = pd.Series(all_tags).value_counts().head(10)
    top5 = tag_counts.head(5).to_dict()
    fig2 = px.bar(tag_counts.reset_index().rename(columns={"index":"tag",0:"count"}), x="tag", y="count", title="Top tags")
    fig2.write_html(str(root/"top_tags.html"))
    # multi-type keys (approx: check types on row sample)
    key_types = {}
    for _, row in df.head(min(5000, len(df))).iterrows():
        for k,v in row.items():
            if str(k).startswith("_"): continue
            key_types.setdefault(k,set()).add(type(v).__name__)
    multi = sum(1 for k,s in key_types.items() if len(s)>1)
    out = {
        "rows": int(rows_n),
        "unique_ids": int(unique_ids),
        "id_collision_count": int(id_collision_count),
        "top_tag_counts": {k:int(v) for k,v in top5.items()},
        "keys_present_top10": {k:int(v) for k,v in pres.set_index("key")["present"].to_dict().items()},
        "keys_multi_type_count": int(multi)
    }
    (root/"result.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))

if __name__=="__main__":
    main()
