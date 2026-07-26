#!/usr/bin/env bash
set -euo pipefail

python -m pip install --quiet --disable-pip-version-check \
  "transformers==4.54.1" "accelerate==1.9.0" "sentencepiece==0.2.0"

python scripts/run_experiment.py
