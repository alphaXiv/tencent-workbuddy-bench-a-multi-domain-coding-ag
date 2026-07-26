#!/usr/bin/env python3
"""Render the four evidence figures from the committed primary rows."""

from __future__ import annotations

import itertools
import json
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROWS = json.loads((ROOT / "reports/harness-sensitivity/results.json").read_text())
OUT = ROOT / "reports/harness-sensitivity/images"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#2563eb"
ORANGE = "#d97706"
INK = "#172033"
MUTED = "#64748b"
GRID = "#dbe3ef"
PALE = "#f6f8fc"


def svg(width: int, height: int) -> ET.Element:
    root = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width=str(width), height=str(height),
                      viewBox=f"0 0 {width} {height}", role="img")
    ET.SubElement(root, "rect", width=str(width), height=str(height), fill="white")
    return root


def text(root: ET.Element, x: float, y: float, value: str, size: int = 15,
         fill: str = INK, anchor: str = "start", weight: str = "400") -> None:
    node = ET.SubElement(root, "text", x=f"{x:.1f}", y=f"{y:.1f}", fill=fill,
                         **{"font-family": "Inter,Arial,sans-serif", "font-size": str(size),
                            "text-anchor": anchor, "font-weight": weight})
    node.text = value


def line(root: ET.Element, x1: float, y1: float, x2: float, y2: float,
         stroke: str = GRID, width: float = 1) -> None:
    ET.SubElement(root, "line", x1=f"{x1:.1f}", y1=f"{y1:.1f}", x2=f"{x2:.1f}",
                  y2=f"{y2:.1f}", stroke=stroke, **{"stroke-width": str(width)})


def save(root: ET.Element, name: str) -> None:
    ET.indent(root)
    ET.ElementTree(root).write(OUT / name, encoding="unicode", xml_declaration=True)


def values(task: str, harness: str) -> list[float]:
    return [r["score"] for r in ROWS if r["task"] == task and r["harness"] == harness]


def headline() -> None:
    cats = [("deterministic", "Deterministic Code"), ("policy", "Policy / reporting Code"),
            ("interaction", "Interaction-sensitive Security")]
    cross, within = [], []
    for key, _ in cats:
        tasks = sorted({r["task"] for r in ROWS if r["sensitivity"] == key})
        cd, wd = [], []
        for task in tasks:
            for seed in range(3):
                e = next(r["score"] for r in ROWS if r["task"] == task and r["seed"] == seed
                         and r["harness"] == "edit_first")
                p = next(r["score"] for r in ROWS if r["task"] == task and r["seed"] == seed
                         and r["harness"] == "plan_first")
                cd.append(abs(p - e))
            for harness in ("edit_first", "plan_first"):
                wd.extend(abs(a - b) for a, b in itertools.combinations(values(task, harness), 2))
        cross.append(statistics.mean(cd))
        within.append(statistics.mean(wd))

    root = svg(1100, 470)
    text(root, 42, 42, "Harness shifts are largest on interaction-sensitive Security tasks", 24, weight="700")
    text(root, 42, 70, "Mean absolute score difference; percentage points", 15, MUTED)
    left, right, top = 280, 1040, 118
    for tick in range(0, 31, 5):
        x = left + (right - left) * tick / 30
        line(root, x, top, x, 400)
        text(root, x, 424, str(tick), 13, MUTED, "middle")
    for i, ((_, label), c, w) in enumerate(zip(cats, cross, within)):
        y = 155 + i * 98
        text(root, left - 18, y + 5, label, 15, INK, "end", "600")
        cw = (right - left) * (c * 100) / 30
        ww = (right - left) * (w * 100) / 30
        ET.SubElement(root, "rect", x=str(left), y=str(y - 19), width=f"{cw:.1f}", height="28",
                      rx="4", fill=BLUE)
        ET.SubElement(root, "rect", x=str(left), y=str(y + 15), width=f"{ww:.1f}", height="14",
                      rx="3", fill="#a8b4c8")
        text(root, left + cw + 9, y + 2, f"{c*100:.1f}", 15, BLUE, weight="700")
        text(root, left + ww + 9, y + 27, f"{w*100:.1f}", 13, MUTED)
    ET.SubElement(root, "rect", x="42", y="444", width="16", height="12", fill=BLUE)
    text(root, 65, 455, "cross-harness", 13)
    ET.SubElement(root, "rect", x="190", y="447", width="16", height="8", fill="#a8b4c8")
    text(root, 213, 455, "within-harness seed variation", 13)
    save(root, "headline_shift.svg")


def task_reordering() -> None:
    labels = {
        "data_quality-hard-label_conflicts": "Label conflicts",
        "model_evaluation-hard-calibration_bins": "Calibration bins",
        "product_policy-medium-refund_policy": "Refund policy",
        "data_reporting-medium-audit_event_export": "Audit export",
        "react-thought-hijack-hard-multistep": "ReAct hijack",
        "tool-schema-confusion-attack-hard-multistep": "Tool schema confusion",
        "agent-to-agent-injection-hard-multistep": "Agent-to-agent injection",
        "privilege-token-exfil-via-summarize-hard-multistep": "Token exfiltration",
    }
    tasks = list(labels)
    root = svg(920, 600)
    text(root, 42, 42, "The scaffold reorders which tasks look easiest", 24, weight="700")
    text(root, 42, 70, "Three-seed mean official score; connected dots are the same task", 15, MUTED)
    left, right, top = 310, 870, 112
    for tick in range(0, 81, 10):
        x = left + (right - left) * tick / 80
        line(root, x, top, x, 535)
        text(root, x, 560, str(tick), 13, MUTED, "middle")
    for i, task in enumerate(tasks):
        y = 130 + i * 50
        e = statistics.mean(values(task, "edit_first")) * 100
        p = statistics.mean(values(task, "plan_first")) * 100
        x1 = left + (right - left) * e / 80
        x2 = left + (right - left) * p / 80
        text(root, left - 18, y + 5, labels[task], 14, INK, "end")
        line(root, x1, y, x2, y, "#94a3b8", 3)
        ET.SubElement(root, "circle", cx=f"{x1:.1f}", cy=str(y), r="7", fill=ORANGE)
        ET.SubElement(root, "circle", cx=f"{x2:.1f}", cy=str(y), r="7", fill=BLUE)
    ET.SubElement(root, "circle", cx="50", cy="582", r="6", fill=ORANGE)
    text(root, 64, 587, "edit-first", 13)
    ET.SubElement(root, "circle", cx="155", cy="582", r="6", fill=BLUE)
    text(root, 169, 587, "plan-first", 13)
    save(root, "task_reordering.svg")


def security_matrix() -> None:
    tasks = [
        ("react-thought-hijack-hard-multistep", "ReAct hijack"),
        ("tool-schema-confusion-attack-hard-multistep", "Tool schema confusion"),
        ("agent-to-agent-injection-hard-multistep", "Agent-to-agent injection"),
        ("privilege-token-exfil-via-summarize-hard-multistep", "Token exfiltration"),
    ]
    cols = [("edit_first", s, f"E{s}") for s in range(3)] + [("plan_first", s, f"P{s}") for s in range(3)]
    root = svg(920, 440)
    text(root, 42, 42, "Security effects reverse across tasks and seeds", 24, weight="700")
    text(root, 42, 70, "Official score for each matched run (E = edit-first, P = plan-first)", 15, MUTED)
    left, top, cellw, cellh = 310, 122, 86, 58
    for j, (_, _, label) in enumerate(cols):
        text(root, left + j * cellw + cellw / 2, 106, label, 15,
             ORANGE if j < 3 else BLUE, "middle", "700")
    palette = ["#eff6ff", "#bfdbfe", "#60a5fa", "#1d4ed8"]
    for i, (task, label) in enumerate(tasks):
        y = top + i * cellh
        text(root, left - 18, y + 35, label, 14, INK, "end")
        for j, (harness, seed, _) in enumerate(cols):
            score = next(r["score"] for r in ROWS if r["task"] == task and
                         r["harness"] == harness and r["seed"] == seed)
            color = palette[min(int(score * 4), 3)]
            ET.SubElement(root, "rect", x=str(left + j * cellw + 2), y=str(y + 2),
                          width=str(cellw - 4), height=str(cellh - 4), rx="5", fill=color)
            text(root, left + j * cellw + cellw / 2, y + 36, f"{score:.2f}", 16,
                 "white" if score >= .7 else INK, "middle", "700")
    text(root, 42, 404, "Same model, prompt, tools, limits, and grader; only scaffold and seed differ.", 14, MUTED)
    save(root, "security_seed_matrix.svg")


def efficiency() -> None:
    metrics = [
        ("Completion", lambda rs: 100 * statistics.mean(r["completed"] for r in rs), "%"),
        ("Tool calls", lambda rs: statistics.mean(r["tool_calls"] for r in rs), ""),
        ("Input tokens", lambda rs: statistics.mean(r["input_tokens"] for r in rs), ""),
        ("Task seconds", lambda rs: statistics.mean(r["elapsed_sec"] for r in rs), "s"),
    ]
    groups = {h: [r for r in ROWS if r["domain"] == "sec" and r["harness"] == h]
              for h in ("edit_first", "plan_first")}
    root = svg(920, 410)
    text(root, 42, 42, "Planning costs more interaction without a uniform score gain", 24, weight="700")
    text(root, 42, 70, "Means over 12 Security task episodes per scaffold", 15, MUTED)
    panelw = 205
    for i, (label, fn, suffix) in enumerate(metrics):
        x0 = 42 + i * 218
        vals = [fn(groups[h]) for h in ("edit_first", "plan_first")]
        vmax = max(vals) * 1.2 or 1
        text(root, x0, 115, label, 15, weight="700")
        for j, (h, value, color) in enumerate(zip(("edit_first", "plan_first"), vals, (ORANGE, BLUE))):
            y = 155 + j * 88
            ET.SubElement(root, "rect", x=str(x0), y=str(y), width=str(panelw),
                          height="28", rx="4", fill=PALE)
            ET.SubElement(root, "rect", x=str(x0), y=str(y),
                          width=f"{panelw * value / vmax:.1f}", height="28", rx="4", fill=color)
            shown = f"{value:.1f}{suffix}" if label != "Input tokens" else f"{value:,.0f}"
            text(root, x0, y - 8, h.replace("_", "-"), 12, MUTED)
            text(root, x0 + panelw, y + 20, shown, 14, INK, "end", "700")
    text(root, 42, 374, "Edit-first", 13, ORANGE, weight="700")
    text(root, 125, 374, "Plan-first", 13, BLUE, weight="700")
    save(root, "efficiency.svg")


headline()
task_reordering()
security_matrix()
efficiency()
print(f"wrote figures to {OUT}")
