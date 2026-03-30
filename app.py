import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "pet" not in st.session_state:
    st.session_state.pet = None

st.divider()

# --- Owner + Pet Setup ---
st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time per day (minutes)", min_value=10, max_value=480, value=90)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=3)

if st.button("Save Owner & Pet"):
    pet = Pet(name=pet_name, species=species, age=pet_age)
    owner = Owner(name=owner_name, available_time=int(available_time))
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.pet = pet
    st.success(f"Saved! {owner_name} owns {pet_name} the {species}.")

st.divider()

# --- Add Tasks ---
st.subheader("Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", [1, 2, 3], format_func=lambda x: {1: "High", 2: "Medium", 3: "Low"}[x])
with col4:
    category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment"])

if st.button("Add task"):
    if st.session_state.pet is None:
        st.warning("Please save an Owner & Pet first.")
    else:
        task = Task(name=task_title, duration=int(duration), priority=priority, category=category)
        st.session_state.pet.add_task(task)
        st.success(f"Added task: {task_title}")

if st.session_state.pet and st.session_state.pet.get_tasks():
    st.write("Current tasks:")
    st.table([
        {"Task": t.name, "Duration (mins)": t.duration, "Priority": t.priority, "Category": t.category}
        for t in st.session_state.pet.get_tasks()
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner is None or st.session_state.pet is None:
        st.warning("Please save an Owner & Pet first.")
    elif not st.session_state.pet.get_tasks():
        st.warning("Please add at least one task first.")
    else:
        scheduler = Scheduler(owner=st.session_state.owner, pets=st.session_state.owner.get_pets())
        scheduler.generate_plan()
        st.success("Schedule generated!")
        st.text(scheduler.explain_plan())
