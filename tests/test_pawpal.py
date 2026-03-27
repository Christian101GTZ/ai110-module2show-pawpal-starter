from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(name="Morning walk", duration=30, priority=1, category="walk")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(name="Feeding", duration=10, priority=1, category="feeding"))
    assert len(pet.get_tasks()) == 1
