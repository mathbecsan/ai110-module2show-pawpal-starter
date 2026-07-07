from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Jordan", preferences={"start_time": "08:00", "available_minutes": 60})

mochi = Pet(name="Mochi", species="cat")
biscuit = Pet(name="Biscuit", species="dog")
owner.add_pet(mochi)
owner.add_pet(biscuit)

biscuit.add_task(Task(id="1", title="Morning walk", duration_minutes=30, priority="high", category="walk"))
biscuit.add_task(Task(id="2", title="Feeding", duration_minutes=10, priority="high", category="feeding"))
mochi.add_task(Task(id="3", title="Litter box cleaning", duration_minutes=15, priority="medium", category="grooming"))
mochi.add_task(Task(id="4", title="Playtime", duration_minutes=20, priority="low", category="enrichment"))

scheduler = Scheduler(
    available_minutes=owner.preferences["available_minutes"],
    start_time=owner.preferences["start_time"],
)
schedule = scheduler.build_schedule_for_owner(owner)

print("=" * 40)
print("Today's Schedule")
print("=" * 40)
for task in schedule:
    print(f"{task.scheduled_start}-{task.scheduled_end}  {task.title} ({task.pet_name}) [{task.priority}]")

print()
print(scheduler.explain_plan(schedule))
