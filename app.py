import streamlit as st
from pawpal_system import Owner, AddPet, CreateTask, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

# --- Owner setup ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
if st.button("Set Owner"):
    st.session_state.owner = Owner(owner_name=owner_name)
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
    st.success(f"Owner set: {owner_name}")

if st.session_state.owner is None:
    st.info("Set an owner above to get started.")
else:
    owner: Owner = st.session_state.owner

st.divider()

if st.session_state.owner is None:
    st.stop()

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    breed = st.text_input("Breed", value="Shiba Inu")
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
with col4:
    weight = st.number_input("Weight (lbs)", min_value=0.1, max_value=300.0, value=20.0)

if st.button("Add Pet"):
    if owner.get_pet(pet_name):
        st.warning(f"A pet named '{pet_name}' already exists.")
    else:
        AddPet().add_pet(owner, name=pet_name, breed=breed, age=int(age), weight=float(weight))
        st.success(f"Added pet: {pet_name}")

if owner.pets:
    st.write("Pets:", [p.name for p in owner.pets])

st.divider()

# --- Add a Task ---
st.subheader("Schedule a Task")

pet_names = [p.name for p in owner.pets]
if not pet_names:
    st.info("Add a pet first before scheduling tasks.")
else:
    selected_pet_name = st.selectbox("Select pet", pet_names)
    selected_pet = owner.get_pet(selected_pet_name)

    col1, col2 = st.columns(2)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk")
        task_time = st.text_input("Time (e.g. 08:00)", value="08:00")
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col2:
        task_description = st.text_area("Description", value="Walk around the block")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)

    if st.button("Add Task"):
        CreateTask().create_task(
            pet=selected_pet,
            task_name=task_name,
            task_description=task_description,
            task_time=task_time,
            priority=priority,
            duration_minutes=int(duration),
        )
        st.success(f"Task '{task_name}' added to {selected_pet_name}.")

    if selected_pet and selected_pet.tasks:
        st.write(f"Tasks for {selected_pet_name}:")
        st.table([
            {
                "Task": t.task_name,
                "Time": t.task_time,
                "Priority": t.priority,
                "Duration (min)": t.duration_minutes,
                "Done": t.completed,
            }
            for t in selected_pet.tasks
        ])

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Schedule")
scheduler: Scheduler = st.session_state.scheduler

schedule_pet_names = [p.name for p in owner.pets]
if not schedule_pet_names:
    st.info("Add a pet and tasks first.")
else:
    sched_pet = st.selectbox("Pet to schedule", schedule_pet_names, key="sched_pet")

    if st.button("Generate Schedule"):
        scheduler.set_active_pet(sched_pet)
        scheduler.organize_schedule()
        st.success("Schedule generated!")

    if scheduler.schedule and scheduler.active_pet and scheduler.active_pet.name == sched_pet:
        st.text(scheduler.get_schedule_summary())
