import json, sys, pathlib

pack_dir = pathlib.Path(__file__).parent
answers = json.load(open(pack_dir/'answers.json','r',encoding='utf-8'))
user = json.load(open(sys.argv[1],'r',encoding='utf-8'))

keys = [
  ("rows", 0),
  ("exact_dup_rate", 3),
  ("token_total_est", 0),
  ("token_p95_est", 0),
  ("token_top5_share", 3),
  ("pii_email_count", 0),
  ("pii_phone_count", 0),
  ("aiish_count", 0),
  ("spam_count", 0)
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

print("by-source dup rates (rounded to 3):")
for src, val in answers["dup_rate_by_source"].items():
    uv = round(user.get("dup_rate_by_source",{}).get(src, -1),3)
    av = round(val,3)
    print(f"  {src}: got {uv}, want {av}")
    if uv != av: ok=False

print("PASS" if ok else "FAIL")
