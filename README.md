# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

- **Owner & pet profiles** — enter an owner name and a pet's name/species; the app builds an `Owner`/`Pet` pair behind the scenes (`app.py`, `pawpal_system.py`).
- **Task management** — add care tasks with a title, duration, priority, an optional fixed time, and a repeat frequency (`Pet.add_task()`).
- **Sorting by time** — `Scheduler.sort_by_time()` orders tasks chronologically by their fixed `"HH:MM"` slot, pushing flexible (untimed) tasks to the end.
- **Filtering** — `Scheduler.filter_tasks()` narrows the task list by pet name and/or completion status; the UI exposes this as "Sort by time" / "Show completed tasks" toggles.
- **Conflict warnings** — `Scheduler.detect_conflicts()` flags pending tasks that share the same fixed time slot, surfaced in the UI via `st.warning` so an owner immediately sees which tasks clash and can move one.
- **Daily/weekly recurrence** — `Task.next_occurrence()` + `Pet.complete_task()` automatically create the next instance of a `"daily"`/`"weekly"` task (due date advanced with `timedelta`) the moment it's marked complete.
- **Priority-based daily schedule** — `Scheduler.build_schedule()` fits as many tasks as possible into the day's available minutes, ordered high → medium → low priority, and `Scheduler.explain_plan()` explains the result in plain English.
- **Next available slot finder** — `Scheduler.find_next_available_slot()` finds the earliest open time slot (of a given duration) that doesn't overlap any pending fixed-time task, using real `[start, start+duration]` interval math rather than exact-time matching.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
========================================
Today's Schedule
========================================
08:00-08:30  Morning walk (Biscuit) [high]
08:30-08:40  Feeding (Biscuit) [high]
08:40-08:55  Litter box cleaning (Mochi) [medium]

3 task(s) scheduled, ordered by priority (high, then medium, then low).
- Morning walk for Biscuit: high priority, 30 min, scheduled 08:00-08:30
- Feeding for Biscuit: high priority, 10 min, scheduled 08:30-08:40
- Litter box cleaning for Mochi: medium priority, 15 min, scheduled 08:40-08:55

========================================
Sorted by time
========================================
07:30  Litter box cleaning (Mochi)
08:00  Morning walk (Biscuit)
08:00  Feeding (Biscuit)
(flexible)  Playtime (Mochi)

========================================
Filtered: Biscuit's tasks
========================================
- Morning walk
- Feeding

========================================
Conflict check
========================================
WARNING: Conflict at 08:00: Morning walk (Biscuit), Feeding (Biscuit)

========================================
Recurring task demo
========================================
Completing Biscuit's daily 'Feeding' task...
Next occurrence auto-created: due 2026-07-08 (id=2-2026-07-08)

========================================
Filtered: Biscuit's completed tasks
========================================
- Feeding (completed)

========================================
Next available slot
========================================
A 15-minute task could start at 08:30 without any overlap.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

The suite in `tests/test_pawpal.py` covers:

- **Core class behavior**: marking a task complete, adding a task to a pet, a pet with no tasks starting empty, and `Owner.get_all_tasks()` aggregating tasks across multiple pets.
- **Sorting**: `Scheduler.sort_by_time()` returns tasks in chronological order and pushes untimed tasks to the end.
- **Scheduling**: `Scheduler.build_schedule()` orders tasks by priority (high → medium → low) and skips a task that doesn't fit in the remaining time budget.
- **Recurring tasks**: completing a `"daily"` task creates a next occurrence due the following day, a `"weekly"` task advances by 7 days, and a one-time (`"once"`) task produces no next occurrence.
- **Conflict detection**: `Scheduler.detect_conflicts()` flags two pending tasks sharing the same fixed time slot, stays silent when times differ, and ignores completed tasks (a finished task no longer occupies its slot).
- **Filtering**: `Scheduler.filter_tasks()` filters correctly by pet name and by completion status.

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.12.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/mathiasbecerrasanchez/Downloads/ai110-module2show-pawpal-starter-main
plugins: anyio-4.14.1
collected 19 items

tests/test_pawpal.py ...................                                 [100%]

============================== 19 passed in 0.01s ==============================
```

**Confidence Level**: ⭐⭐⭐⭐☆ (4/5) — all core class behavior, sorting, priority scheduling, recurrence, conflict detection, filtering, and next-available-slot finding are covered and passing, and the full add → sort/filter → conflict → complete → recur → schedule flow has been verified end-to-end through both the CLI (`main.py`) and the Streamlit UI. The main known gap (see reflection.md 2b) is that `detect_conflicts()` only checks exact time matches, not overlapping durations — though `find_next_available_slot()` does do real interval-overlap math, so that gap is now narrower than it was.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their fixed `"HH:MM"` time slot; tasks with no fixed time are pushed to the end |
| Filtering | `Scheduler.filter_tasks()` | Filters a task list by `pet_name` and/or `completed` status |
| Conflict handling | `Scheduler.detect_conflicts()` | Warns when two or more tasks share the exact same fixed time slot (see reflection.md 2b for why exact-match, not overlap, was chosen) |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a `"daily"`/`"weekly"` task via `Pet.complete_task()` auto-creates the next occurrence with `due_date` advanced by a `timedelta` |
| Next available slot | `Scheduler.find_next_available_slot()` | Finds the earliest open `"HH:MM"` slot of a given duration by merging real `[start, start+duration]` intervals from pending fixed-time tasks — catches overlaps that `detect_conflicts()`'s exact-match check would miss |

## 📸 Demo Walkthrough

**UI features and actions available:**

- Set the owner's name and the pet's name/species under "Owner & Pet."
- Set the day's start time and how many minutes are available under "Today's Constraints."
- Add a task under "Add a Task" with a title, duration, priority, an optional fixed time (checkbox + time picker), and a repeat frequency (once/daily/weekly).
- Under "Tasks," toggle "Sort by time" and "Show completed tasks" to see filtering/sorting live, mark any pending task complete from the dropdown, and read conflict warnings for any tasks sharing a fixed time slot.
- Click "Generate schedule" to build and view today's priority-ordered plan, with an expandable "Why this plan?" explanation.

**Example workflow:**

1. Owner "Jordan" adds pet "Mochi" (dog).
2. Add "Litter box cleaning" (15 min, medium priority, no fixed time).
3. Add "Feeding" (10 min, high priority, fixed time 08:00, repeats daily).
4. Add "Morning walk" (30 min, high priority, fixed time 08:00, once) — since it shares 08:00 with "Feeding," a conflict warning appears immediately: *"Conflict at 08:00: Feeding (Mochi), Morning walk (Mochi)."*
5. Mark "Feeding" complete — a success message confirms its next occurrence was auto-scheduled for tomorrow, and the conflict warning updates (a completed task no longer counts as occupying its slot).
6. Click "Generate schedule" — the app fits "Morning walk" and "Litter box cleaning" into the available minutes, ordered by priority, with an explanation of why each task was included.

**Key Scheduler behaviors shown:** chronological sorting (`sort_by_time`), pet/completion filtering (`filter_tasks`), same-time conflict warnings that ignore completed tasks (`detect_conflicts`), daily/weekly recurrence on completion (`next_occurrence`/`complete_task`), priority-based schedule building with reasoning (`build_schedule`/`explain_plan`), and finding the next open interval-aware time slot for a new task (`find_next_available_slot`).

**Sample CLI output** (from `python main.py`, which exercises the same backend as the UI):

```
========================================
Today's Schedule
========================================
08:00-08:30  Morning walk (Biscuit) [high]
08:30-08:40  Feeding (Biscuit) [high]
08:40-08:55  Litter box cleaning (Mochi) [medium]

3 task(s) scheduled, ordered by priority (high, then medium, then low).
- Morning walk for Biscuit: high priority, 30 min, scheduled 08:00-08:30
- Feeding for Biscuit: high priority, 10 min, scheduled 08:30-08:40
- Litter box cleaning for Mochi: medium priority, 15 min, scheduled 08:40-08:55

========================================
Sorted by time
========================================
07:30  Litter box cleaning (Mochi)
08:00  Morning walk (Biscuit)
08:00  Feeding (Biscuit)
(flexible)  Playtime (Mochi)

========================================
Filtered: Biscuit's tasks
========================================
- Morning walk
- Feeding

========================================
Conflict check
========================================
WARNING: Conflict at 08:00: Morning walk (Biscuit), Feeding (Biscuit)

========================================
Recurring task demo
========================================
Completing Biscuit's daily 'Feeding' task...
Next occurrence auto-created: due 2026-07-08 (id=2-2026-07-08)

========================================
Filtered: Biscuit's completed tasks
========================================
- Feeding (completed)

========================================
Next available slot
========================================
A 15-minute task could start at 08:30 without any overlap.
```
