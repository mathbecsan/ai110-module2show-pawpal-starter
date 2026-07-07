# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

A pet owner using PawPal+ should be able to:

1. **Add a pet (and their own owner info)** — enter their name and basic preferences (e.g. earliest start time, how many minutes a day they can realistically spend on care), then add one or more pets with a name and species.
2. **Add/edit care tasks for a pet** — record what needs to happen (walk, feeding, meds, enrichment, grooming), how long it takes, and how important it is (priority), and be able to update or remove a task later.
3. **Generate and view today's plan** — press a button to have the app pick and order the day's tasks based on the owner's available time and each task's priority, and see a short explanation of why the plan looks the way it does.

**a. Initial design**

My initial UML has four classes:

- **Owner** — holds the owner's `name`, a `preferences` dict (e.g. start time, daily time budget), and the list of `Pet`s they own. Responsible for managing that list (`add_pet`, `get_pets`).
- **Pet** — holds `name`, `species`, and the list of `Task`s that belong to that pet. Responsible for managing its own tasks (`add_task`, `remove_task`, `get_tasks`).
- **Task** — a plain data holder for one care item: `title`, `duration_minutes`, `priority`, `category`, `is_recurring`, `completed`, plus (after refinement, see below) `pet_name`. Responsible for its own completion state (`mark_complete`).
- **Scheduler** — takes a flat list of `Task`s plus an `available_minutes` budget and `start_time`, and is responsible for producing an ordered, time-stamped schedule (`build_schedule`) and a human-readable explanation of the choices (`explain_plan`).

The relationships are: `Owner` owns many `Pet`s, `Pet` has many `Task`s, and `Scheduler` depends on `Task` (it does not depend on `Owner`/`Pet` directly — see below).

**b. Design changes**

Yes — I asked my AI assistant to review the skeleton in `pawpal_system.py` and it flagged that `Scheduler.build_schedule` takes a flat `List[Task]` with no way to tell which pet each task came from once tasks from multiple pets are merged together, which would break the "explain the plan" requirement for an owner with more than one pet. Rather than giving `Scheduler` a hard dependency on `Pet`/`Owner` (which would couple scheduling logic to the ownership hierarchy), I added an optional `pet_name` field directly on `Task`. This keeps `Scheduler` simple and pet-agnostic while still letting `build_schedule`/`explain_plan` reference which pet a task belongs to in the output.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers: the owner's available minutes and day start time, each task's `duration_minutes` and `priority` (high/medium/low), an optional fixed `time` slot used only for conflict warnings, and `frequency` (once/daily/weekly) for recurrence.

Time and priority mattered most because they're what actually decide whether a task makes it into today's plan (`build_schedule` sorts by priority, then greedily fits tasks into the remaining minutes). Fixed time and frequency are secondary — they don't change what gets scheduled today, they just add a warning layer (conflicts) and automation layer (recurrence) on top of the core priority/time-budget decision.

**b. Tradeoffs**

`Scheduler.detect_conflicts()` only flags tasks that share the *exact same* `time` string (e.g. two tasks both set to "08:00"). It does not check whether task durations actually overlap — a task at 08:00 for 30 minutes and another at 08:15 would not be flagged, even though they overlap in practice.

This is reasonable for PawPal+ because most owners think in terms of "I want to do the walk around 8am" rather than precise start/end windows, so exact-match slots already catch the realistic case (accidentally double-booking a time) with a simple, easy-to-read `dict`-based grouping. Real interval-overlap detection (comparing `[start, start+duration]` ranges pairwise) would be more correct but adds real complexity for a feature that's meant to be a lightweight warning, not a hard scheduling constraint — the actual time slots owners get are still computed separately by `build_schedule()`, which never double-books tasks in the first place.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI across the full arc: brainstorming the class list and UML from the scenario, scaffolding `pawpal_system.py` and `main.py`, writing the pytest suite, and — in this final phase — wiring `app.py` to the Scheduler and driving the running app (CLI, a headless browser, and Streamlit's `AppTest` harness) to actually verify it worked rather than just reading the code. The most effective single feature was multi-file agent editing: being able to change `pawpal_system.py`, `main.py`, and `tests/test_pawpal.py` together in one pass kept the backend, the demo, and the tests from drifting out of sync with each other.

I also kept each phase in its own focused context — design (Phases 1–3), algorithms (Phase 4), testing (Phase 5), UI/polish (Phase 6) — rather than one long running chat. The most useful prompts were narrow and file-scoped ("based on my skeleton, how should X talk to Y") rather than open-ended ("make this better"), because they got answers I could immediately check against the actual classes instead of generic advice.

**b. Judgment and verification**

The clearest moment was in this phase: after wiring the "Mark complete" button in `app.py`, I didn't just trust that the code looked right — I actually launched the Streamlit app and drove it end-to-end with a browser automation script. The success message ("Next occurrence auto-scheduled...") never appeared on screen, even though the underlying `Pet.complete_task()` logic was already unit-tested and correct. The cause was a line I'd written myself: `st.rerun()` called immediately after `st.success(...)`, which restarts the script before the message can render. It read as perfectly reasonable code — Streamlit apps call `st.rerun()` all the time — and would have passed a code review by inspection alone. Only running the app and watching the actual page state caught it. I removed the redundant `st.rerun()` (button clicks already trigger a rerun) and re-verified with both a browser script and Streamlit's `AppTest` harness before trusting it.

That same testing pass also surfaced a real design gap, not just a bug: `Scheduler.detect_conflicts()` was flagging a *completed* task as still conflicting with a pending one at the same time slot. I decided that was wrong — a finished task no longer occupies its slot — and fixed `detect_conflicts` to ignore completed tasks, adding a test (`test_detect_conflicts_ignores_completed_tasks`) to lock in that decision.

---

## 4. Testing and Verification

**a. What you tested**

Fourteen automated tests cover: core class behavior (mark complete, add task, empty-pet edge case, cross-pet task aggregation), sorting by time (including untimed tasks), priority-based schedule building (including a task that doesn't fit the time budget), recurring tasks (daily advances 1 day, weekly advances 7 days, one-time tasks produce no recurrence), conflict detection (duplicate times flagged, different times silent, completed tasks ignored), and filtering by pet/completion status.

These mattered because they're exactly what a pet owner depends on for correctness in ways that fail silently otherwise: wrong priority ordering means an urgent task quietly gets bumped for a low-priority one; wrong recurrence means an owner stops getting reminded about a daily medication without any error; wrong conflict detection means two tasks silently double-book a time slot.

**b. Confidence**

4/5. Every unit-level behavior is tested and passing, and in this phase I also verified the full add → sort/filter → conflict → complete → recur → schedule flow end-to-end against the actually-running app (CLI and Streamlit UI), which is what caught the `st.rerun()` bug and the completed-task conflict gap described above — issues unit tests alone wouldn't have caught since they don't touch `app.py`.

What I'd test next: overlapping-duration conflicts (two tasks at different start times whose durations overlap — currently undetected, see 2b), a multi-pet flow driven through the actual UI (the backend already supports multiple pets via `Owner.get_all_tasks()`, but `app.py` only manages one pet at a time), and date/time edge cases like a recurring task completed right at a day boundary.

---

## 5. Reflection

**a. What went well**

The recurring-task and conflict-detection interaction: completing a `"daily"` task correctly spawns its next occurrence *and* correctly stops counting the just-completed task as a live conflict, while still catching a genuine clash with the newly-created next occurrence if one exists. Getting that interaction right took an actual bug fix (see 3b), so I'm most satisfied that the final behavior is verified correct rather than just plausible-looking.

**b. What you would improve**

Two things: extend `app.py` to manage multiple pets in the UI (the backend already supports it via `Owner`/`Owner.get_all_tasks()`, but the current UI only wires up one `Pet`), and upgrade `detect_conflicts()` from exact-time matching to real interval-overlap detection so a 08:00–08:30 task and an 08:15 task would also get flagged.

**c. Key takeaway**

AI can generate a lot of plausible-looking code very quickly — including code that's subtly wrong in ways that survive a casual read. The `st.rerun()` bug in this phase is the clearest example: it looked like normal, idiomatic Streamlit code, and only actually running the app (not reading it) revealed that it silently discarded user feedback. Being the "lead architect" here meant not treating "the code compiles and looks reasonable" as good enough — it meant insisting on driving the real app end-to-end, and owning the judgment calls (exact-time vs. overlap conflicts, where to draw the Scheduler/Owner/Pet boundary) that AI can propose but shouldn't be trusted to settle alone.
