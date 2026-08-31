# Experiment 4 — per-row tagging traces

One gzipped tar per analysis unit, `<substrate>/<dataset>__<unit>.tar.gz`.
14 archives in total: 2 substrates x 7 units, 15,058 trace files, 153 MB
uncompressed.

These are SADA's per-row LLM tagging traces on the 10,000-row
`amazon_fine_food_review` table. They are the evidence for the mechanism claim
of §5.5: every augmented value came from a model call over the row's own text,
recorded here chunk by chunk. The `skill_off` conditions have no counterpart,
because their emitted Python scripts assign values by keyword and regex instead
— those scripts are in `../mechanism_artifacts/`.

They are packed because they are numerous and highly compressible (11:1), and
because `1_verify/verify_all.sh` does not read them: the grounding percentages come
from `../grounding/`. Nothing in the reproduction path needs to be unpacked.

To unpack everything in place:

```bash
./extract.sh
```

To inspect a single unit without unpacking:

```bash
tar tzf substrate-claude-sonnet-4-6/amazon_fine_food_review__causal_whatif_helpfulness.tar.gz | head
tar xzOf substrate-claude-sonnet-4-6/amazon_fine_food_review__causal_whatif_helpfulness.tar.gz \
    --wildcards '*/tag_*.json' | head -c 2000
```
