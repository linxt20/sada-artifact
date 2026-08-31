# Paper excerpts

Kept here so a reviewer can check the artifact against the text without leaving
the repository.

| File | What |
|---|---|
| `experiments.tex` | the paper's experiment section, the source of every claim the verification in `../../1_verify/` checks |
| `appendix.pdf` | the supplementary appendix. Sections D.1-D.4 reproduce the four LLM judge prompts of Experiments 1-4 verbatim; the rendered copies under `../../3_experiments/*/prompts/` are generated from the code and should match them |

Appendix A-B cover the trust/provenance layer and the schema-structure validity
rules; appendix C covers the cost model and sub-agent isolation. `../../2_operator/`
is the implementation those sections describe.
