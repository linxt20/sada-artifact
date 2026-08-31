# Data

This is a compact artifact whose purpose is to reproduce the paper's tables from
the archived per-item outputs. It does not copy the full source datasets.

`../../3_experiments/*/raw/` contains everything the paper's numbers are computed
from: the analysis reports, judge outputs, grounding verdicts and XGBoost
results. The following inputs must still be obtained from the complete upstream
repository or from each dataset's official source:

- the full source tables and augmented CSVs used by Experiments 1–3;
- the full GT annotations used by Experiment 3;
- the 10,000-row Amazon Fine Food Review input table of Experiment 4;
- the TextTabBench processed pickles, `data.csv`, augmented CSVs and embeddings
  of Experiment 5.

`preprocess.py` checks whether a complete repository supplied through
`--upstream-root` has these key inputs, and emits a machine-readable manifest.
It does not download data that is subject to third-party licensing.

Experiment 5's dataset sources, download procedure and preprocessing conventions
come from [TextTabBench](https://github.com/mrazmartin/TextTabBench). Follow the
upstream instructions to obtain the data, and observe each dataset's own licence
and access conditions; this artifact does not redistribute the source data.
