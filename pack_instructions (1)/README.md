# Pack: instructions
- Instruction/response JSON with `source`, `category`, `rating`.
- Injected duplicates, label noise (empty high-rating), and long responses.
## Closed-ended tasks
1) Exact duplicate rate.
2) p95 token length; share of tokens in top 5% (optional).
3) Category distribution; avg response length by rating (spot length bias).
4) Count of empty responses with rating >=4; propose filters + retention.
