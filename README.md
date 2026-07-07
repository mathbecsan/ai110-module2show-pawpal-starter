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
- **Conflict detection**: `Scheduler.detect_conflicts()` flags two tasks sharing the same fixed time slot and stays silent when times differ.
- **Filtering**: `Scheduler.filter_tasks()` filters correctly by pet name and by completion status.

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.12.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/mathiasbecerrasanchez/Downloads/ai110-module2show-pawpal-starter-main
plugins: anyio-4.14.1
collected 13 items

tests/test_pawpal.py .............                                       [100%]

============================== 13 passed in 0.01s ==============================
```

**Confidence Level**: ⭐⭐⭐⭐☆ (4/5) — all core class behavior, sorting, priority scheduling, recurrence, conflict detection, and filtering are covered and passing. The main gap (see reflection.md 2b) is that conflict detection only checks exact time matches, not overlapping durations, so that edge case isn't verified here.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their fixed `"HH:MM"` time slot; tasks with no fixed time are pushed to the end |
| Filtering | `Scheduler.filter_tasks()` | Filters a task list by `pet_name` and/or `completed` status |
| Conflict handling | `Scheduler.detect_conflicts()` | Warns when two or more tasks share the exact same fixed time slot (see reflection.md 2b for why exact-match, not overlap, was chosen) |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Completing a `"daily"`/`"weekly"` task via `Pet.complete_task()` auto-creates the next occurrence with `due_date` advanced by a `timedelta` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
