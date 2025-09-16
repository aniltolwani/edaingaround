import json, sys, pathlib

pack_dir = pathlib.Path(__file__).parent
answers = json.load(open(pack_dir/'answers.json','r',encoding='utf-8'))
user = json.load(open(sys.argv[1],'r',encoding='utf-8'))

keys = [
  ("rows", 0),
  ("exact_dup_rate", 3),
  ("py_parse_rate", 3),
  ("eval_exec_open_count", 0),
  ("longline_over_200_count", 0)
]
ok = True
for k,prec in keys:
    if k not in user:
        print(f"MISSING key: {k}"); ok=False; continue
    au = user[k]; aa = answers[k]
    if isinstance(aa, float):
        if round(au,prec) != round(aa,prec):
            print(f"DIFF {k}: got {au}, want {aa} (rounded to {prec})"); ok=False
    else:
        if au != aa:
            print(f"DIFF {k}: got {au}, want {aa}"); ok=False

print("PASS" if ok else "FAIL")
