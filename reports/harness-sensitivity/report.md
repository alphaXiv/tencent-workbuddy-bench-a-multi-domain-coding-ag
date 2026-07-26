# Does an agent harness change the benchmark result?

Coding agents combine a language model with a “harness”: the loop that shows context, requests actions, and applies tool calls. [Tencent WorkBuddy Bench](https://alphaxiv.org/abs/2607.20911) argues that this surrounding machinery can materially change scores and rankings, especially on Security work. We tested that idea on a small public subset by holding the model and task machinery fixed and changing only whether the agent edited immediately or planned first.

**Verdict — partially reproduced.** The matched scaffold change caused a 27.1 percentage-point mean absolute score shift on four interaction-sensitive Security tasks, larger than the 9.0-point shift on two deterministic Code tasks. However, two policy/reporting Code tasks did not shift, the signed Security average moved only +2.1 points, and the open substitutions do not test the paper’s multi-model ranking or contamination-resistance claims.

**Scope.** This is 48 fresh episodes: eight official tasks, two scaffolds, and three seeds. The proprietary account configurations were replaced by transparent edit-first and plan-first loops around the same local `Qwen/Qwen2.5-Coder-7B-Instruct`.

![Cross-harness score shifts and seed variation](images/headline_shift.svg)

Blue bars show the average absolute paired difference between scaffolds; gray bars show average score variation among seeds within one scaffold. Security moved 27.1 points across scaffolds versus 14.6 among seeds, so its harness effect was not merely ordinary sampling noise in this subset. Deterministic Code was less clear: 9.0 versus 7.7 points. Policy/reporting Code was unchanged.

## What was held fixed

We used checksum-verified archives from the [official dataset release](https://huggingface.co/datasets/tencent/workbuddy-bench): two deterministic Code tasks, two policy/reporting Code tasks, and four multistep Security injection tasks. Each run received the same task prompt and workspace snapshot, file and shell tools, ten-action limit, 1,024-token action limit, temperature 0.25, model weights, and official grader. Edit-first entered the tool loop immediately; plan-first added one explicit planning pass before the identical loop.

All inference and grading ran through OpenResearch on Kubernetes. Jobs used NVIDIA RTX PRO 6000 Blackwell GPUs, peaked at 16 concurrently allocated GPUs, and the evidence window lasted 0.483 wall-clock hours (10:28:29–10:57:28 UTC on 2026-07-26). Terminal logs emitted every task score, completion/refusal flag, tool count, token count, and elapsed time; the 48 primary rows and run identifiers are in [`results.json`](results.json).

## Scores move, but not in one direction

![Mean task scores under both scaffolds](images/task_reordering.svg)

Planning helped calibration bins (+15.4 points), ReAct hijacking (+25.0), and tool-schema confusion (+25.0), but hurt agent-to-agent injection (−25.0) and token exfiltration (−16.7). Refund policy and audit export were identical. Thus a single aggregate signed change hides the main effect: plan-first did not uniformly improve the model; it changed which tasks the model could solve.

The paper reports an 8.6-point average Security difference between harness/account configurations. Our 27.1-point absolute difference is not a numerical replication of that table: it covers four selected tasks, one smaller open model, and simplified scaffolds. It is directional evidence for the narrower mechanism.

![Per-seed Security score matrix](images/security_seed_matrix.svg)

Repeated seeds also qualify the result. The Security domain means were 50.0%, 31.3%, and 37.5% for edit-first, versus 37.5%, 43.8%, and 43.8% for plan-first. Task-level effects reverse across seeds and tasks, while a duplicate plan-first confirmatory matrix reproduced every score exactly. Apparent overall “winner” changes therefore remain too small for a ranking claim, even though paired task behavior changes substantially.

## Interaction costs and failure modes

![Security interaction efficiency](images/efficiency.svg)

Plan-first used 5.4 tool calls and 6,747 input tokens per Security episode, compared with 3.4 calls and 3,999 tokens for edit-first. Its completion rate was lower (66.7% versus 83.3%) and mean task time higher (5.9 versus 3.4 seconds); neither scaffold emitted a scored refusal. More interaction therefore did not buy a uniform score gain. The measurable failure-mode shift was completion and tool-use behavior, not refusal.

## Claim-by-claim assessment

| Target claim | Paper evidence | Observed evidence | Assessment |
|---|---|---|---|
| A fixed executable subset changes under matched harnesses | Scores/rankings vary by agent account; Security differs by 8.6 points on average | Absolute paired shift: Security 27.1, deterministic Code 9.0, policy Code 0.0 points; completion and tool traces also changed | **Aligned for score and completion/tool behavior** |
| Sensitive tasks move more than deterministic algorithms | Security is especially harness-sensitive | Security 27.1 versus deterministic Code 9.0; policy Code was 0.0 | **Partially aligned** |
| Repeats distinguish ranking changes from seed variance | Ranking changes are a central concern | Security cross-harness shift 27.1 versus 14.6 within-harness seed variation, but signed mean +2.1 | **Inconclusive for ranking** |

The paired matrix is the shared compute cost for all three assessments: 0.483 elapsed Kubernetes hours at a 16-GPU peak. No long-term contamination claim was attempted; public prompts can test executability and harness sensitivity, not whether future models have seen them. A fuller reproduction needs the named account configurations, more tasks, multiple model backends, and enough repeated trials to estimate ranking uncertainty.

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/alphaXiv/tencent-workbuddy-bench-a-multi-domain-coding-ag/blob/main/notebooks/workbuddy_harness_sensitivity.py)

The [self-contained notebook](../../notebooks/workbuddy_harness_sensitivity.py) exposes the aggregate evidence without rerunning inference. Figures are generated by [`scripts/build_report_figures.py`](../../scripts/build_report_figures.py); formal branches and exact commands are linked from the [README](../../README.md).
