from datetime import time as dt_time
from uuid import uuid4

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

SPECIES_OPTIONS = ["dog", "cat", "other"]
PRIORITY_OPTIONS = ["low", "medium", "high"]
FREQUENCY_OPTIONS = ["once", "daily", "weekly"]

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
    st.session_state.owner.add_pet(Pet(name="Mochi", species="dog"))

owner: Owner = st.session_state.owner
pet: Pet = owner.get_pets()[0]

st.divider()
st.subheader("Owner & Pet")
owner.name = st.text_input("Owner name", value=owner.name)
col1, col2 = st.columns(2)
with col1:
    pet.name = st.text_input("Pet name", value=pet.name)
with col2:
    pet.species = st.selectbox("Species", SPECIES_OPTIONS, index=SPECIES_OPTIONS.index(pet.species))

st.divider()
st.subheader("Today's Constraints")
col1, col2 = st.columns(2)
with col1:
    start_time_str = st.text_input("Day start time (HH:MM)", value="08:00")
with col2:
    available_minutes = st.number_input("Available minutes today", min_value=5, max_value=600, value=90)

scheduler = Scheduler(available_minutes=int(available_minutes), start_time=start_time_str)

st.divider()
st.subheader("Add a Task")
has_fixed_time = st.checkbox("Give this task a fixed time?", value=False)

with st.form("add_task_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", PRIORITY_OPTIONS, index=2)

    col1, col2 = st.columns(2)
    with col1:
        task_time = st.time_input("Time", value=dt_time(8, 0)) if has_fixed_time else None
    with col2:
        frequency = st.selectbox("Repeats", FREQUENCY_OPTIONS, index=0)

    submitted = st.form_submit_button("Add task")

if submitted:
    pet.add_task(
        Task(
            id=str(uuid4()),
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            time=task_time.strftime("%H:%M") if task_time else None,
            frequency=frequency,
        )
    )

st.divider()
st.subheader("Tasks")

all_tasks = pet.get_tasks()
col1, col2 = st.columns(2)
with col1:
    sort_by_time = st.checkbox("Sort by time", value=True)
with col2:
    show_completed = st.checkbox("Show completed tasks", value=True)

visible_tasks = scheduler.filter_tasks(all_tasks, completed=None if show_completed else False)
if sort_by_time:
    visible_tasks = scheduler.sort_by_time(visible_tasks)

if visible_tasks:
    st.table(
        [
            {
                "Title": task.title,
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority,
                "Time": task.time or "flexible",
                "Repeats": task.frequency,
                "Completed": "✅" if task.completed else "—",
            }
            for task in visible_tasks
        ]
    )
else:
    st.info("No tasks match the current filters. Add one above.")

pending_tasks = [task for task in all_tasks if not task.completed]
if pending_tasks:
    task_to_complete = st.selectbox(
        "Mark a task complete",
        options=[task.id for task in pending_tasks],
        format_func=lambda tid: next(task.title for task in pending_tasks if task.id == tid),
    )
    if st.button("Mark complete"):
        next_task = pet.complete_task(task_to_complete)
        if next_task:
            st.success(f"Marked complete! Next occurrence auto-scheduled for {next_task.due_date}.")
        else:
            st.success("Marked complete!")

conflicts = scheduler.detect_conflicts(all_tasks)
if conflicts:
    for warning in conflicts:
        st.warning(f"⚠️ {warning}")
else:
    st.success("No time conflicts detected.")

st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    schedule = scheduler.build_schedule_for_owner(owner)
    if schedule:
        st.success(f"{len(schedule)} task(s) scheduled for today.")
        st.table(
            [
                {
                    "Time": f"{task.scheduled_start}–{task.scheduled_end}",
                    "Task": task.title,
                    "Pet": task.pet_name,
                    "Priority": task.priority,
                }
                for task in schedule
            ]
        )
        with st.expander("Why this plan?"):
            st.text(scheduler.explain_plan(schedule))
    else:
        st.warning("No tasks fit in the available time. Try increasing available minutes or lowering task durations.")
