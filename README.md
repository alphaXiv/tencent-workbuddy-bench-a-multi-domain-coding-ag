# WorkBuddy Bench harness-sensitivity reproduction

This public repository contains a bounded reproduction of the harness-sensitivity
claim in arXiv:2607.20911. Fresh Kubernetes measurements and the reader-facing
report will be published here after the paired runs complete.

The experiment uses checksum-verified tasks from the official
[`tencent/workbuddy-bench`](https://huggingface.co/datasets/tencent/workbuddy-bench)
release. It substitutes two transparent open scaffolds for the unavailable
CodeBuddy Code and Claude Code accounts, while holding the local Qwen model,
tools, prompts, action budgets, and grader fixed.
