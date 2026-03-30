from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(name="Morning walk", duration=30, priority=1, category="walk")
    pet.add_task(task)
    task.mark_complete(pet)
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(name="Feeding", duration=10, priority=1, category="feeding"))
    assert len(pet.get_tasks()) == 1

def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan", available_time=90)
    dog = Pet(name="Mochi", species="dog", age=3)
    dog.add_task(Task(name="Fetch",   duration=20, priority=3, category="enrichment", time="10:00"))
    dog.add_task(Task(name="Walk",    duration=30, priority=1, category="walk",        time="08:00"))
    dog.add_task(Task(name="Feeding", duration=10, priority=1, category="feeding",     time="07:00"))
    owner.add_pet(dog)
    scheduler = Scheduler(owner=owner, pets=owner.get_pets())
    sorted_tasks = scheduler.sort_by_time()
    times = [task.time for _, task in sorted_tasks]
    assert times == sorted(times)
 
def test_daily_task_creates_new_task_on_complete():
    from datetime import date, timedelta
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(name="Morning walk", duration=30, priority=1, category="walk", frequency="daily")
    pet.add_task(task)
    task.mark_complete(pet)
    incomplete = pet.get_tasks()
    assert len(incomplete) == 1
    assert incomplete[0].due_date == str(date.today() + timedelta(days=1))

def test_detect_conflicts_flags_same_time():
    owner = Owner(name="Jordan", available_time=90)
    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Luna",  species="cat", age=5)
    dog.add_task(Task(name="Walk",    duration=30, priority=1, category="walk",    time="08:00"))
    cat.add_task(Task(name="Feeding", duration=10, priority=1, category="feeding", time="08:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner=owner, pets=owner.get_pets())
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]
