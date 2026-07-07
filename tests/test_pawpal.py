from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task(id="1", title="Walk", duration_minutes=20, priority="high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="cat")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task(id="1", title="Feeding", duration_minutes=10, priority="high"))

    assert len(pet.get_tasks()) == 1


def test_pet_with_no_tasks_returns_empty_list():
    pet = Pet(name="Mochi", species="cat")

    assert pet.get_tasks() == []


def test_sort_by_time_orders_chronologically():
    scheduler = Scheduler(available_minutes=60)
    tasks = [
        Task(id="1", title="Feeding", duration_minutes=10, priority="high", time="09:00"),
        Task(id="2", title="Walk", duration_minutes=20, priority="high", time="07:00"),
        Task(id="3", title="Playtime", duration_minutes=15, priority="low"),  # no fixed time
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.title for task in sorted_tasks] == ["Walk", "Feeding", "Playtime"]


def test_build_schedule_orders_by_priority():
    scheduler = Scheduler(available_minutes=60, start_time="08:00")
    tasks = [
        Task(id="1", title="Playtime", duration_minutes=10, priority="low"),
        Task(id="2", title="Walk", duration_minutes=10, priority="high"),
        Task(id="3", title="Grooming", duration_minutes=10, priority="medium"),
    ]

    schedule = scheduler.build_schedule(tasks)

    assert [task.title for task in schedule] == ["Walk", "Grooming", "Playtime"]


def test_build_schedule_skips_task_that_exceeds_available_time():
    scheduler = Scheduler(available_minutes=10, start_time="08:00")
    tasks = [Task(id="1", title="Long walk", duration_minutes=30, priority="high")]

    schedule = scheduler.build_schedule(tasks)

    assert schedule == []


def test_daily_task_completion_creates_next_day_occurrence():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(
        Task(
            id="1",
            title="Feeding",
            duration_minutes=10,
            priority="high",
            frequency="daily",
            due_date=date(2026, 7, 7),
        )
    )

    next_task = pet.complete_task("1")

    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 8)
    assert next_task.completed is False
    assert len(pet.get_tasks()) == 2  # original (completed) + new occurrence


def test_weekly_task_completion_advances_by_seven_days():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(
        Task(
            id="1",
            title="Grooming",
            duration_minutes=30,
            priority="medium",
            frequency="weekly",
            due_date=date(2026, 7, 7),
        )
    )

    next_task = pet.complete_task("1")

    assert next_task.due_date == date(2026, 7, 14)


def test_one_time_task_completion_has_no_next_occurrence():
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(id="1", title="Vet visit", duration_minutes=45, priority="high"))

    next_task = pet.complete_task("1")

    assert next_task is None
    assert len(pet.get_tasks()) == 1


def test_detect_conflicts_flags_duplicate_times():
    scheduler = Scheduler(available_minutes=60)
    tasks = [
        Task(id="1", title="Walk", duration_minutes=30, priority="high", pet_name="Biscuit", time="08:00"),
        Task(id="2", title="Feeding", duration_minutes=10, priority="high", pet_name="Mochi", time="08:00"),
    ]

    conflicts = scheduler.detect_conflicts(tasks)

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_detect_conflicts_no_warning_for_different_times():
    scheduler = Scheduler(available_minutes=60)
    tasks = [
        Task(id="1", title="Walk", duration_minutes=30, priority="high", time="08:00"),
        Task(id="2", title="Feeding", duration_minutes=10, priority="high", time="09:00"),
    ]

    assert scheduler.detect_conflicts(tasks) == []


def test_filter_tasks_by_pet_name_and_completion():
    scheduler = Scheduler(available_minutes=60)
    walk = Task(id="1", title="Walk", duration_minutes=30, priority="high", pet_name="Biscuit", completed=True)
    feeding = Task(id="2", title="Feeding", duration_minutes=10, priority="high", pet_name="Biscuit")
    litter = Task(id="3", title="Litter", duration_minutes=15, priority="medium", pet_name="Mochi")
    tasks = [walk, feeding, litter]

    assert scheduler.filter_tasks(tasks, pet_name="Biscuit") == [walk, feeding]
    assert scheduler.filter_tasks(tasks, completed=True) == [walk]


def test_owner_get_all_tasks_aggregates_across_pets():
    owner = Owner(name="Jordan")
    mochi = Pet(name="Mochi", species="cat")
    biscuit = Pet(name="Biscuit", species="dog")
    mochi.add_task(Task(id="1", title="Litter", duration_minutes=15, priority="medium"))
    biscuit.add_task(Task(id="2", title="Walk", duration_minutes=30, priority="high"))
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    all_tasks = owner.get_all_tasks()

    assert len(all_tasks) == 2
    assert {task.title for task in all_tasks} == {"Litter", "Walk"}
