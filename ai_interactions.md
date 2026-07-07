# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add a third algorithmic capability beyond the basic requirements (Extensions Challenge 1) — I asked for something like a "next available slot" finder or weighted prioritization, and let the agent choose which one fit the existing design best.

**What did the agent do?**

The agent picked a "next available slot" finder because it complements (and improves on) the existing `detect_conflicts()`, which only catches tasks that share the *exact same* time string. It:

- Added `Scheduler.find_next_available_slot(tasks, duration_minutes)` to `pawpal_system.py`, which builds real `[start, start+duration]` busy intervals from pending fixed-time tasks and scans forward from the day's start time for the first gap big enough to fit a new task, returning `None` if nothing fits before the day ends.
- Added 5 new tests to `tests/test_pawpal.py` (free day, slot right after a busy task, slot in a gap between two busy tasks, correct behavior when two busy tasks overlap each other, and the "day is full" case) — full suite is now 19 tests, all passing.
- Added a "Next available slot" demo section to `main.py`, and updated `README.md`'s Features list, Smarter Scheduling table, and CLI sample output, plus added the new method to both `diagrams/uml.mmd` and `diagrams/uml_final.mmd`.

**What did you have to verify or fix manually?**

While designing the algorithm, the agent's first instinct was a two-pass approach: sort busy intervals, explicitly merge overlapping ones into a clean list, *then* scan for gaps. On inspection, that merge pass was redundant — because the scan already tracks `candidate = max(candidate, busy_end)` as it walks the sorted intervals, overlapping/nested busy times are absorbed automatically without a separate merge step. The extra pass was cut in favor of the single-pass version, which was verified against a hand-traced overlap case (two tasks at 08:00–08:40 and 08:20–08:50) to confirm it still correctly reports the busy window extending to 08:50, not just 08:40.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
