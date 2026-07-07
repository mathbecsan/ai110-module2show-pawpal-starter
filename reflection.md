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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
