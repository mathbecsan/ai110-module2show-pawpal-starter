from dataclasses import dataclass, field
from typing import List, Optional

_PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def _time_to_minutes(time_str: str) -> int:
    """Convert an "HH:MM" string into minutes since midnight."""
    hours, minutes = map(int, time_str.split(":"))
    return hours * 60 + minutes


def _minutes_to_time(minutes: int) -> str:
    """Convert minutes since midnight back into an "HH:MM" string."""
    minutes %= 24 * 60
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


@dataclass
class Task:
    id: str
    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    category: str = "general"  # e.g. walk, feeding, meds, enrichment, grooming
    is_recurring: bool = False
    completed: bool = False
    pet_name: Optional[str] = None
    scheduled_start: Optional[str] = None
    scheduled_end: Optional[str] = None

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet, tagging it with the pet's name."""
        task.pet_name = task.pet_name or self.name
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this pet by id."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def get_tasks(self) -> List[Task]:
        """Return all tasks belonging to this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


class Scheduler:
    def __init__(self, available_minutes: int, start_time: str = "08:00"):
        self.available_minutes = available_minutes
        self.start_time = start_time

    def build_schedule(self, tasks: List[Task]) -> List[Task]:
        """Order pending tasks by priority and fit as many as possible into the available time."""
        pending = [task for task in tasks if not task.completed]
        ordered = sorted(pending, key=lambda task: _PRIORITY_RANK.get(task.priority, 99))

        schedule: List[Task] = []
        current_minutes = _time_to_minutes(self.start_time)
        remaining = self.available_minutes

        for task in ordered:
            if task.duration_minutes > remaining:
                continue
            task.scheduled_start = _minutes_to_time(current_minutes)
            task.scheduled_end = _minutes_to_time(current_minutes + task.duration_minutes)
            schedule.append(task)
            current_minutes += task.duration_minutes
            remaining -= task.duration_minutes

        return schedule

    def build_schedule_for_owner(self, owner: Owner) -> List[Task]:
        """Retrieve all tasks across an owner's pets and build a schedule from them."""
        return self.build_schedule(owner.get_all_tasks())

    def explain_plan(self, schedule: List[Task]) -> str:
        """Return a human-readable explanation of why the schedule looks the way it does."""
        if not schedule:
            return "No tasks fit in the available time."

        lines = [
            f"{len(schedule)} task(s) scheduled, ordered by priority (high, then medium, then low)."
        ]
        for task in schedule:
            pet_label = f" for {task.pet_name}" if task.pet_name else ""
            lines.append(
                f"- {task.title}{pet_label}: {task.priority} priority, "
                f"{task.duration_minutes} min, scheduled {task.scheduled_start}-{task.scheduled_end}"
            )
        return "\n".join(lines)
