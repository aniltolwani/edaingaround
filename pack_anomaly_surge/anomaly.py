#!/usr/bin/env python
# coding: utf-8

# # Pack: anomaly_surge
# 
# **Goal:** Practice robust JSON loading (invalid lines, BOM, control chars), normalization, and targeted plots.
# 
# ## Closed-ended tasks
# 1) Build a tolerant loader. Report `rows_parsed` and `error_counts` (with keys: truncated, jsonerror, control_char, bom).
# 2) Normalize: coerce `rating` to 1..5 ints when possible; `text` to string; keep a count of `empty_text_count`.
# 3) Compute `p95_text_length` and a `rating_hist` dict (1..5).
# 4) Plots: save `length_hist.html` (hist of text lengths) and `rating_bar.html`.
# 
# ## Output (result.json)
# ```
# {
#   "rows_parsed": int,
#   "error_counts": {"truncated": int, "jsonerror": int, "control_char": int, "bom": int},
#   "rating_hist": {"1": int, "2": int, "3": int, "4": int, "5": int},
#   "p95_text_length": int,
#   "empty_text_count": int
# }
# ```
# ```
# {
#   "rows_parsed": 0,
#   "error_counts": {
#     "truncated": 0,
#     "jsonerror": 0,
#     "control_char": 0,
#     "bom": 0
#   },
#   "rating_hist": {
#     "1": 0,
#     "2": 0,
#     "3": 0,
#     "4": 0,
#     "5": 0
#   },
#   "p95_text_length": 0,
#   "empty_text_count": 0
# }
# ```

# 

# In[30]:


from pathlib import Path

files = list(Path('./').rglob('an*json*'))
set([f.suffix for f in files])


# In[155]:


import gzip
import json
from json import JSONDecodeError

control_nums = list(range(32))
ok_chars = ["\t", "\n","\r"]
ok_nums = [ord(c) for c in ok_chars]
control_nums = list(set(control_nums) - set(ok_nums))
control_chars = [chr(a) for a in control_nums]

def parse_remove_control_characters(content):
    is_control = False
    char_hits = [char for char in control_chars if char in content]
    if char_hits:
        is_control = True
        for char in char_hits:
            content = content.replace(char, "")
    return content, is_control

records = []
rows_parsed = 0 
error_counts = {
    "truncated": 0,
    "jsonerror": 0,
    "control_char": 0,
    "bom": 0,
}

for file in files:
    if file.suffix == ".gz":
        opener = gzip.open(file, "rt")
    else:
        opener = open(file, "rt")
    with opener as f:
        content = f.read()

    # check for BOM or control character
    if content.startswith("\ufeff"):
        error_counts["bom"] += 1
        # move the cursor so that we can still read it properly
        # is this even an error?
        # 4 hex values -> how many bytes?
        content = content[1:]
    # remove control characters

    content, is_control = parse_remove_control_characters(content)
    if is_control:
        error_counts["control_char"] += 1

    # try a json parse
    try:
        obj = json.loads(content)
        # load it in 
        if isinstance(obj, list):
            records.extend(obj)
        elif isinstance(obj, dict):
            records.append(obj)
        else:
            print("unintended: obj is ", obj)
        continue
    except JSONDecodeError:
        # print("passing on file", file)
        pass

    # try jsonl if that didn't work
    for line in content.splitlines():
        if line.strip():
            try:
                obj = json.loads(line)
                records.extend(obj if isinstance(obj,list) else [obj])
            except JSONDecodeError:
                error_counts["jsonerror"] += 1
                # print(obj, line)
                # print('weird!', file)

len(records)


# In[97]:


import pandas as pd
df = pd.DataFrame(records)
df.rating.value_counts()


# 2) Normalize: coerce `rating` to 1..5 ints when possible; `text` to string; keep a count of `empty_text_count`.

# In[103]:


df.rating = pd.to_numeric(df.rating, errors = "coerce")
df.rating.value_counts()


# In[108]:


df.rating = df.rating.clip(1, 5)


# In[130]:


df.text = df.text.astype('string')
na = df.text.isna().sum()
empty = (df.text.str.strip() == "").sum()
empty_text_count = na + empty
empty_text_count


# 3) Compute `p95_text_length` and a `rating_hist` dict (1..5).

# In[135]:


df['text_length'] = df.text.str.len()


# In[138]:


p95_text_length = df['text_length'].quantile(0.95)
p95_text_length


# In[145]:


ratings_hist = dict(df.rating.value_counts())


# In[144]:


dict(ratings_hist)


# 4) Plots: save `length_hist.html` (hist of text lengths) and `rating_bar.html`.

# In[146]:


from matplotlib import pyplot as plt
plt.hist(df.text_length)


# In[148]:


val_counts = df.rating.value_counts()
plt.bar(val_counts.index, val_counts.values)


# In[156]:


# from pprint import pprint
error_counts


# In[161]:


out = {
    "rows_parsed": int(rows_parsed),
    "error_counts": {k:int(v) for k,v in error_counts.items()},
    "rating_hist": ratings_hist,
    "p95_text_length": int(p95_text_length),
    "empty_text_count": int(empty_text_count)
}
out


# In[158]:


p95_text_length


# In[ ]:




