from pawpal_system import Owner, Pet, Task, Scheduler

# --- Create Owner ---
owner = Owner(name="Jordan", available_time=90)

# --- Create Pets ---
dog = Pet(name="Mochi", species="dog", age=3)
cat = Pet(name="Luna", species="cat", age=5)

# --- Add Tasks to Dog ---
dog.add_task(Task(name="Morning walk",   duration=30, priority=1, category="walk"))
dog.add_task(Task(name="Flea medication",duration=10, priority=1, category="meds"))
dog.add_task(Task(name="Fetch session",  duration=20, priority=3, category="enrichment"))

# --- Add Tasks to Cat ---
cat.add_task(Task(name="Feeding",        duration=10, priority=1, category="feeding"))
cat.add_task(Task(name="Grooming",       duration=15, priority=2, category="grooming"))
cat.add_task(Task(name="Laser toy play", duration=20, priority=3, category="enrichment"))

# --- Add Pets to Owner ---
owner.add_pet(dog)
owner.add_pet(cat)

# --- Run Scheduler ---
scheduler = Scheduler(owner=owner, pets=owner.get_pets())
scheduler.generate_plan()

# --- Print Today's Schedule ---
print("=" * 45)
print("        TODAY'S SCHEDULE — PawPal+")
print("=" * 45)
print(scheduler.explain_plan())
print("=" * 45)
