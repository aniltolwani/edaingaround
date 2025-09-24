#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, gzip, ast
from pathlib import Path
import pandas as pd
import plotly.express as px

def iter_records(root):
    for pat in ("*.json","*.jsonl","*.json.gz","*.jsonl.gz"):
        for fp in Path(root).rglob(pat):
            if fp.suffix==".gz":
                f=gzip.open(fp,"rt",encoding="utf-8",errors="ignore")
                head=f.read(1024); f.seek(0)
                if head.strip().startswith("["):
                    try:
                        arr=json.load(f)
                        for o in arr: 
                            if isinstance(o,dict): yield o
                    except Exception: pass
                else:
                    for line in f:
                        line=line.strip()
                        if not line: continue
                        try:
                            o=json.loads(line); 
                            if isinstance(o,dict): yield o
                        except Exception: pass
                f.close()
            else:
                with open(fp,"r",encoding="utf-8",errors="ignore") as f:
                    head=f.read(1024); f.seek(0)
                    if head.strip().startswith("["):
                        try:
                            arr=json.load(f)
                            for o in arr: 
                                if isinstance(o,dict): yield o
                        except Exception: pass
                    else:
                        for line in f:
                            line=line.strip()
                            if not line: continue
                            try:
                                o=json.loads(line); 
                                if isinstance(o,dict): yield o
                            except Exception: pass

def py_metrics(code:str):
    try:
        tree=ast.parse(code)
    except Exception:
        return None
    class C(ast.NodeVisitor):
        def __init__(self):
            self.fn=0; self.br=0; self.calls=[]
        def visit_FunctionDef(self,n):
            self.fn+=1; self.generic_visit(n)
        def visit_AsyncFunctionDef(self,n):
            self.fn+=1; self.generic_visit(n)
        def visit_If(self,n): self.br+=1; self.generic_visit(n)
        def visit_For(self,n): self.br+=1; self.generic_visit(n)
        def visit_While(self,n): self.br+=1; self.generic_visit(n)
        def visit_Try(self,n): self.br+=1; self.generic_visit(n)
        def visit_Call(self,n):
            name=None
            if isinstance(n.func, ast.Name): name=n.func.id
            elif isinstance(n.func, ast.Attribute): name=n.func.attr
            self.calls.append((name or "").lower())
            self.generic_visit(n)
    c=C(); c.visit(tree)
    return {"funcs":c.fn, "branches":c.br, "calls":c.calls}

def main():
    root=Path(__file__).parent
    rows=list(iter_records(root))
    import pandas as pd
    df=pd.DataFrame(rows)
    # danger counts
    danger=["eval","exec","open(","subprocess","pickle.loads","yaml.load("]
    danger_counts={k:int(df["code"].fillna("").str.contains(k, regex=False).sum()) for k in danger}
    # py parse metrics
    is_py=df["lang"]=="py"
    py_codes=df.loc[is_py,"code"].fillna("")
    parsed = [py_metrics(c) for c in py_codes]
    total_py = len(parsed)
    parsed_ok = sum(1 for p in parsed if p is not None)
    py_parse_rate = round(parsed_ok/max(1,total_py), 6)
    py_funcs = sum(p["funcs"] for p in parsed if p)
    py_branches = sum(p["branches"] for p in parsed if p)
    # top calls
    from collections import Counter
    cc = Counter()
    for p in parsed:
        if not p: continue
        cc.update(p["calls"])
    top_calls = dict(cc.most_common(5))
    # js eval count
    js_eval = int((df["lang"]=="js") & df["code"].fillna("").str.contains("eval(", regex=False)).sum()
    # long lines > 200
    def has_long_line(s):
        return any(len(line)>200 for line in s.splitlines())
    long_lines = int(df["code"].fillna("").map(has_long_line).sum())
    # plots
    import numpy as np
    cyclo = [p["branches"]+1 for p in parsed if p]
    px.histogram(x=cyclo, nbins=30, title="Cyclomatic approx (py)").write_html(str(root/"cyclomatic_hist_py.html"))
    px.bar(df["lang"].value_counts().reset_index().rename(columns={"index":"lang","lang":"count"}),
           x="lang", y="count", title="Rows by lang").write_html(str(root/"lang_breakdown.html"))
    out={
        "rows": int(len(df)),
        "py_parse_rate": float(py_parse_rate),
        "py_total_funcs": int(py_funcs),
        "py_branch_nodes": int(py_branches),
        "danger_counts": {k:int(v) for k,v in danger_counts.items()},
        "js_eval_count": int(js_eval),
        "long_lines_over_200": int(long_lines),
        "top_calls": {k:int(v) for k,v in top_calls.items()}
    }
    (root/"result.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))

if __name__=="__main__":
    main()
