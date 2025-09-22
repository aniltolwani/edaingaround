# Pack: schema_zoo

**Goal:** Practice robust schema inference, nested flattening, indexing/selection, and plotting.

## Closed-ended tasks
1) **Schema profile**: total `rows`, `unique_ids`, and `id_collision_count` (same id with conflicting payloads).
2) **Missingness plot**: create a bar chart of top-15 keys by presence rate and save as `schema_missingness.html`.
3) **Tags**: flatten any tag fields (either `meta.tags` list or `meta=[{k:'tag',v:...}]`) and produce a bar chart of top tags saved as `top_tags.html`.
4) **Counts**: output `top_tag_counts` (top 5 as a dict) and `keys_multi_type_count` (keys that appear with more than one JSON type).

## What to output
Create `result.json` with:
```
{
  "rows": int,
  "unique_ids": int,
  "id_collision_count": int,
  "top_tag_counts": {"tag": count, ...},   # top 5
  "keys_present_top10": {"key": count, ...}, # optional, not graded
  "keys_multi_type_count": int
}
```
Also save plots:
- `schema_missingness.html`
- `top_tags.html`
