import json, sys, pathlib

pack_dir = pathlib.Path(__file__).parent
answers = json.load(open(pack_dir/'answers.json','r',encoding='utf-8'))
user = json.load(open(sys.argv[1],'r',encoding='utf-8'))

keys = [
  ("rows", 0),
  ("exact_dup_rate", 3),
  ("token_p95_est", 0),
  ("empty_high_rating_count", 0)
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

print("category counts (top-3 shown):")
ac = answers["category_counts"]
uc = user.get("category_counts",{})
for cat in sorted(ac.keys())[:3]:
    print(f"  {cat}: got {uc.get(cat,-1)}, want {ac[cat]}")
    if uc.get(cat,-1) != ac[cat]: ok=False

print("avg response length by rating (rounded to 1):")
for r, val in answers["avg_response_length_by_rating"].items():
    uv = round(user.get("avg_response_length_by_rating",{}).get(str(r), user.get("avg_response_length_by_rating",{}).get(r, -1)),1)
    av = round(val,1)
    print(f"  rating {r}: got {uv}, want {av}")
    if uv != av: ok=False

print("PASS" if ok else "FAIL")
