from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Jordan", preferences={"start_time": "08:00", "available_minutes": 60})

mochi = Pet(name="Mochi", species="cat")
biscuit = Pet(name="Biscuit", species="dog")
owner.add_pet(mochi)
owner.add_pet(biscuit)

# Tasks are added out of time order, and two of them (walk/feeding) share a
# time slot on purpose so the conflict check below has something to catch.
biscuit.add_task(Task(id="1", title="Morning walk", duration_minutes=30, priority="high", category="walk", time="08:00"))
mochi.add_task(Task(id="3", title="Litter box cleaning", duration_minutes=15, priority="medium", category="grooming", time="07:30"))
mochi.add_task(Task(id="4", title="Playtime", duration_minutes=20, priority="low", category="enrichment"))
biscuit.add_task(Task(id="2", title="Feeding", duration_minutes=10, priority="high", category="feeding", time="08:00", frequency="daily"))

scheduler = Scheduler(
    available_minutes=owner.preferences["available_minutes"],
    start_time=owner.preferences["start_time"],
)
all_tasks = owner.get_all_tasks()

print("=" * 40)
print("Today's Schedule")
print("=" * 40)
schedule = scheduler.build_schedule_for_owner(owner)
for task in schedule:
    print(f"{task.scheduled_start}-{task.scheduled_end}  {task.title} ({task.pet_name}) [{task.priority}]")
print()
print(scheduler.explain_plan(schedule))

print()
print("=" * 40)
print("Sorted by time")
print("=" * 40)
for task in scheduler.sort_by_time(all_tasks):
    print(f"{task.time or '(flexible)'}  {task.title} ({task.pet_name})")

print()
print("=" * 40)
print("Filtered: Biscuit's tasks")
print("=" * 40)
for task in scheduler.filter_tasks(all_tasks, pet_name="Biscuit"):
    print(f"- {task.title}")

print()
print("=" * 40)
print("Conflict check")
print("=" * 40)
conflicts = scheduler.detect_conflicts(all_tasks)
if conflicts:
    for warning in conflicts:
        print(f"WARNING: {warning}")
else:
    print("No conflicts found.")

print()
print("=" * 40)
print("Recurring task demo")
print("=" * 40)
print("Completing Biscuit's daily 'Feeding' task...")
next_feeding = biscuit.complete_task("2")
if next_feeding:
    print(f"Next occurrence auto-created: due {next_feeding.due_date} (id={next_feeding.id})")

print()
print("=" * 40)
print("Filtered: Biscuit's completed tasks")
print("=" * 40)
for task in scheduler.filter_tasks(biscuit.get_tasks(), completed=True):
    print(f"- {task.title} (completed)")

print()
print("=" * 40)
print("Next available slot")
print("=" * 40)
new_task_minutes = 15
slot = scheduler.find_next_available_slot(owner.get_all_tasks(), duration_minutes=new_task_minutes)
if slot:
    print(f"A {new_task_minutes}-minute task could start at {slot} without any overlap.")
else:
    print(f"No {new_task_minutes}-minute slot is free today.")
