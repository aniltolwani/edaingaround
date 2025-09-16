# Pack: mixed_chat
- Mixed JSON/JSONL/(gz) with nested `messages` and flat `prompt/response`.
- Injected exact dupes, AI-ish boilerplate, PII (emails/phones), and spam repetition.
## Closed-ended tasks
1) Count rows.
2) Exact duplicate rate overall and by `source` (on main text = response or messages concat).
3) Token cost: total est tokens, p95, and share of tokens in top 5% longest.
4) Counts: AI-ish boilerplate, spam repetition, PII emails/phones.
5) Propose 3 filters with estimated retained %%.
