# WorkBuddy Bench harness-sensitivity reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/blob/main/notebooks/workbuddy_harness_sensitivity.py)

We tested the central harness-sensitivity claim from [Tencent WorkBuddy Bench (2607.20911)](https://alphaxiv.org/abs/2607.20911) on eight checksum-pinned public tasks. With the same local Qwen backend, grader, prompt, tools, and limits, changing only an edit-first versus plan-first scaffold produced a **27.1 percentage-point mean absolute score shift on four Security tasks**, versus **9.0 points on deterministic Code** and **0.0 on policy/reporting Code**. The paper reports an 8.6-point average Security harness difference in its broader proprietary-account comparison; these numbers are directional rather than directly comparable.

**Assessment: partially reproduced.** The Security subset was more harness-sensitive and task ordering changed, but policy-sensitive Code did not shift, the signed Security mean changed by only +2.1 points, and this small open-model substitution cannot test the paper's multi-model ranking or contamination-resistance claims.

The paired matrix used 48 task episodes: eight official tasks × two matched scaffolds × three seeds. It ran on Kubernetes with NVIDIA RTX PRO 6000 Blackwell GPUs, reached 16 concurrently allocated GPUs, and took 0.483 elapsed hours. The published `CodeBuddy Code` and `Claude Code` account configurations were unavailable, so we substituted transparent edit-first and plan-first loops around `Qwen/Qwen2.5-Coder-7B-Instruct`.

- [Detailed illustrated report](reports/harness-sensitivity/report.md)
- [Self-contained tutorial notebook](notebooks/workbuddy_harness_sensitivity.py)
- [Machine-readable primary rows](reports/harness-sensitivity/results.json)
- [Exact figure builder](scripts/build_report_figures.py)

## Experiment log

Every experiment used the exact command shown by `orx exp status`: `bash scripts/run_experiment.sh`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface | Not run as an experiment (publication surface) | Report, notebook, figures, and measurements | — |
| [Protocol smoke](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/create-findings-through-replace-tool) | Verify official task unpacking, model loading, tool loop, and terminal grader output | `bash scripts/run_experiment.sh` | Successful Kubernetes terminal log | 1 GPU |
| [12 paired Code shards](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/paired-edit-first-seed0-code-a) | Two Code strata × two scaffolds × three seeds | `bash scripts/run_experiment.sh` | 24 primary task episodes | Up to 12 GPUs concurrently |
| [Security edit-first seeds 0](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-edit-first-seed0-security), [1](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-edit-first-seed1-security), [2](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-edit-first-seed2-security) | Four official Security tasks, three seeds | `bash scripts/run_experiment.sh` | 12 primary task episodes | 3 GPUs concurrently |
| [Security plan-first seeds 0](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-plan-first-seed0-security), [1](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-plan-first-seed1-security), [2](https://github.com/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/tree/orx/confirmatory-plan-first-seed2-security) | Matched scaffold comparison on the same four tasks | `bash scripts/run_experiment.sh` | 12 primary task episodes; duplicate corrected runs matched exactly | 3 GPUs concurrently |

## Reproduce the analysis

The official task archives are downloaded from [`tencent/workbuddy-bench`](https://huggingface.co/datasets/tencent/workbuddy-bench), verified against the SHA-256 values in `scripts/run_benchmark.py`, and graded with their bundled graders. The committed primary rows already contain the evidence needed for the figures:

```bash
python3 scripts/build_report_figures.py
marimo check notebooks/workbuddy_harness_sensitivity.py
marimo edit notebooks/workbuddy_harness_sensitivity.py
```

Formal inference runs require the configured OpenResearch Kubernetes backend and were launched with:

```bash
orx exp run <experiment-id> --backend k8s
```

Raw terminal logs remain attached to the run IDs recorded in `results.json`; no credentials, model weights, task archives, or unlicensed benchmark contents are redistributed here.
