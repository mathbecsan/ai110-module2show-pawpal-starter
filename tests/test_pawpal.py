from pawpal_system import Pet, Task


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
