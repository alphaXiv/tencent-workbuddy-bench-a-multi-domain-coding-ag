# WorkBuddy Bench: a bounded harness-sensitivity reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/blob/main/notebooks/workbuddy_harness_reproduction.py)

This repository reproduces the harness-sensitivity claim in [Tencent WorkBuddy Bench (arXiv:2607.20911)](https://arxiv.org/abs/2607.20911) on eight exact tasks from the checksum-verified public release. We ran the same open model, prompts, tools, limits, graders, and three seeds under two transparent scaffolds: edit-first and plan-first.

**Assessment: partially reproduced.** The paper reports an 8.6-point mean absolute Security shift across model/harness configurations. Our smaller substitution measured a **22.9-point mean absolute task-level Security shift** (individual tasks moved 16.7–25.0 points), although opposing changes cancelled to a **+2.1-point aggregate** for plan-first. Deterministic Code tasks moved 9.0 points on average and policy Code tasks did not move. Security task ordering reversed, but the aggregate harness gap was smaller than seed variation, so there is no robust overall winner.

Scope and substitutions: four Security and four Code tasks, Qwen2.5-Coder-7B-Instruct instead of the paper’s proprietary backends, and two open scaffolds instead of CodeBuddy Code and Claude Code. All runs used Kubernetes on NVIDIA RTX PRO 6000 Blackwell GPUs, one GPU per job, with a peak of 16 concurrent GPUs and 0.504 hours campaign wall time.

- [Tutorial-style report](reports/harness-sensitivity/report.md)
- [Self-contained marimo notebook](notebooks/workbuddy_harness_reproduction.py)
- [Primary measurements](reports/harness-sensitivity/data/results.csv)
- [Official WorkBuddy Bench release](https://huggingface.co/datasets/tencent/workbuddy-bench)

## Experiment log

The exact run command was inherited unchanged by every experiment: `bash scripts/run_experiment.sh`. `main` is presentation-only.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Public report, figures, notebook, and code | Not run as an experiment (publication surface) | Publication surface | — |
| [Fresh GPU smoke baseline](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/fresh-gpu-smoke-baseline) | Frozen root | `bash scripts/run_experiment.sh` | Failed before clone; no evidence | Kubernetes, 1 GPU |
| [Bounded replace protocol](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/bounded-replace-edit-protocol) | Final bounded edit protocol smoke | `bash scripts/run_experiment.sh` | Valid official Code grading | Kubernetes, 1 GPU |
| [Edit-first Code seed 0: A](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-edit-first-seed0-code-a) / [B](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-edit-first-seed0-code-b) | Two Code shards | `bash scripts/run_experiment.sh` | 4 official tasks | Kubernetes, 2×1 GPU |
| [Edit-first Code seed 1: A](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-edit-first-seed1-code-a) / [B](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-edit-first-seed1-code-b) | Two Code shards | `bash scripts/run_experiment.sh` | 4 official tasks | Kubernetes, 2×1 GPU |
| [Edit-first Code seed 2: A](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-edit-first-seed2-code-a) / [B](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-edit-first-seed2-code-b) | Two Code shards | `bash scripts/run_experiment.sh` | 4 official tasks | Kubernetes, 2×1 GPU |
| [Plan-first Code seed 0: A](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-plan-first-seed0-code-a) / [B](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-plan-first-seed0-code-b) | Two Code shards | `bash scripts/run_experiment.sh` | 4 official tasks | Kubernetes, 2×1 GPU |
| [Plan-first Code seed 1: A](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-plan-first-seed1-code-a) / [B](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-plan-first-seed1-code-b) | Two Code shards | `bash scripts/run_experiment.sh` | 4 official tasks | Kubernetes, 2×1 GPU |
| [Plan-first Code seed 2: A](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-plan-first-seed2-code-a) / [B](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-plan-first-seed2-code-b) | Two Code shards | `bash scripts/run_experiment.sh` | 4 official tasks | Kubernetes, 2×1 GPU |
| [Security workdir fix](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/create-findings-through-replace-tool) | Canonical `/workdir` mapping and findings creation | `bash scripts/run_experiment.sh` | Valid official Security grading | Kubernetes, 1 GPU |
| [Edit-first Security seed 0](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-edit-first-seed0-security) / [1](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-edit-first-seed1-security) / [2](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-edit-first-seed2-security) | Corrected four-task Security matrix | `bash scripts/run_experiment.sh` | 39.6% mean | Kubernetes, 3×1 GPU |
| [Plan-first Security seed 0](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-plan-first-seed0-security-corrected) / [1](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-plan-first-seed1-security-corrected) / [2](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-plan-first-seed2-security-corrected) | Corrected four-task Security matrix | `bash scripts/run_experiment.sh` | 41.7% mean | Kubernetes, 3×1 GPU |

## Re-run

Every task archive is downloaded from the official public release and verified against its published SHA-256 checksum. Choose a committed condition in `configs/experiment.json`, then run:

```bash
bash scripts/run_experiment.sh
```

Formal evidence was produced only through `orx exp run --backend k8s`; the command above is the fixed experiment entrypoint.
