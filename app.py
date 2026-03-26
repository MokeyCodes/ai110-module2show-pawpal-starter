import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, Frequency, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, your pet care planning assistant!
Manage tasks for your pets and generate optimized daily schedules.
"""
)

# Initialize session state for owner persistence
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Pet Owner")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

# Sidebar for owner and pet management
with st.sidebar:
    st.header("👤 Owner & Pets")

    # Owner name input
    owner_name = st.text_input("Owner name", value=owner.name, key="owner_name_input")
    if owner_name != owner.name:
        owner.name = owner_name

    st.divider()

    # Add new pet
    st.subheader("Add New Pet")
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"], key="species_select")
    with col3:
        age = st.number_input("Age (years)", min_value=0, max_value=50, value=1)

    if st.button("Add Pet", key="add_pet_button"):
        new_pet = Pet(name=pet_name, species=species, age=age)
        owner.add_pet(new_pet)
        st.success(f"✓ Added {pet_name}!")
        st.rerun()

    st.divider()

    # Display current pets
    if owner.get_pets():
        st.subheader("Your Pets")
        for pet in owner.get_pets():
            st.write(f"🐾 {pet.name} ({species}, {pet.age} yrs) - {len(pet.get_tasks())} tasks")
    else:
        st.info("No pets yet. Add one above!")

# Main content area
st.divider()

if not owner.get_pets():
    st.warning("⚠️ Please add at least one pet to get started!")
else:
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📅 Schedule", "✏️ Manage Tasks", "📊 Task Summary"])

    with tab1:
        st.subheader("Today's Schedule")

        today_schedule = scheduler.get_today_schedule()

        if not today_schedule:
            st.info("No tasks scheduled for today!")
        else:
            # Display schedule
            schedule_data = []
            for task in today_schedule:
                schedule_data.append({
                    "Time": task.time,
                    "Pet": task.pet_name,
                    "Task": task.description,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority.value.upper(),
                    "Status": "✓ Done" if task.completed else "○ Todo"
                })

            st.table(schedule_data)

            # Conflict detection
            st.subheader("Scheduling Analysis")
            conflicts = scheduler.detect_conflicts(today_schedule)
            if conflicts:
                for conflict in conflicts:
                    st.warning(conflict)
            else:
                st.success("✓ No scheduling conflicts!")

    with tab2:
        st.subheader("Add Task to Pet")

        col1, col2 = st.columns(2)

        with col1:
            selected_pet = st.selectbox(
                "Select pet",
                [pet.name for pet in owner.get_pets()],
                key="task_pet_select"
            )

        with col2:
            task_description = st.text_input("Task description", value="")

        col3, col4, col5 = st.columns([1.2, 1.2, 1])

        with col3:
            task_time = st.text_input("Time (HH:MM)", value="09:00")

        with col4:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30)

        with col5:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], key="freq_select")

        priority = st.selectbox("Priority", ["low", "medium", "high"], key="priority_select")

        if st.button("Add Task", key="add_task_button"):
            if not task_description or not task_time:
                st.error("⚠️ Please fill in task description and time!")
            else:
                try:
                    # Find the pet and add task
                    pet = next(p for p in owner.get_pets() if p.name == selected_pet)

                    # Convert string values to enums
                    freq_enum = Frequency.ONCE if frequency == "once" else (
                        Frequency.DAILY if frequency == "daily" else Frequency.WEEKLY
                    )
                    priority_enum = Priority.LOW if priority == "low" else (
                        Priority.MEDIUM if priority == "medium" else Priority.HIGH
                    )

                    new_task = Task(
                        description=task_description,
                        time=task_time,
                        duration_minutes=int(duration),
                        frequency=freq_enum,
                        priority=priority_enum
                    )

                    pet.add_task(new_task)
                    st.success(f"✓ Added task '{task_description}' to {pet.name}!")
                    st.rerun()
                except ValueError:
                    st.error("⚠️ Invalid time format. Use HH:MM (e.g., 09:00)")

    with tab3:
        st.subheader("Task Summary")

        all_tasks = owner.get_all_tasks()

        if not all_tasks:
            st.info("No tasks yet!")
        else:
            # Stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks", len(all_tasks))
            with col2:
                incomplete = len(scheduler.filter_by_status(all_tasks, completed=False))
                st.metric("Todo", incomplete)
            with col3:
                complete = len(scheduler.filter_by_status(all_tasks, completed=True))
                st.metric("Completed", complete)

            st.divider()

            # Filter by pet
            st.subheader("Filter Tasks by Pet")
            pet_names = [pet.name for pet in owner.get_pets()]
            selected_filter_pet = st.selectbox("Choose pet", pet_names, key="filter_pet_select")

            filtered_tasks = scheduler.filter_by_pet(all_tasks, selected_filter_pet)

            if filtered_tasks:
                for task in filtered_tasks:
                    status = "✓" if task.completed else "○"
                    st.write(
                        f"{status} [{task.time}] {task.description} "
                        f"({task.duration_minutes}min) - **{task.priority.value}**"
                    )
            else:
                st.info(f"No tasks for {selected_filter_pet}")

