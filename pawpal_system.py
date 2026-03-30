from dataclasses import dataclass, field
from datetime import date, timedelta

@dataclass
class Task:
    name: str
    duration: int        # minutes
    priority: int        # 1 = high, 2 = medium, 3 = low
    category: str        # walk, feeding, meds, grooming, enrichment
    completed: bool = False
    time: str = "08:00"  # scheduled time for this task 
    frequency: str = "once" #once, daily, weekly, etc.
    due_date: str = "" # YYYY-MM-DD format for tasks with specific deadlines
  

    def mark_complete(self, pet: "Pet") -> None:
        """Mark this task as completed."""
        self.completed = True
        if self.frequency == "daily":
            next_date = date.today() + timedelta(days=1)
            new_task = Task(
                name=self.name, duration=self.duration, priority=self.priority, 
                category=self.category, time=self.time, frequency=self.frequency, 
                due_date=str(next_date)
            )
            pet.add_task(new_task)
        elif self.frequency == "weekly":
            next_date = date.today() + timedelta(days=7)
            new_task = Task(
                name=self.name, duration=self.duration, priority=self.priority, 
                category=self.category, time=self.time, frequency=self.frequency, 
                due_date=str(next_date)
            )
            pet.add_task(new_task)

    def is_completable(self, available_time: int) -> bool:
        """Return True if this task fits within the given available time."""
        return self.duration <= available_time


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str = ""
    tasks: dict[str, Task] = field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks[task.name] = task

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.pop(task.name, None)

    def get_tasks(self) -> list[Task]:
        """Return all incomplete tasks assigned to this pet."""
        return [t for t in self.tasks.values() if not t.completed]


@dataclass
class Owner:
    name: str
    available_time: int  # minutes per day
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's pet list."""
        self.pets.remove(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets


class Scheduler:
    def __init__(self, owner: Owner, pets: list[Pet]):
        self.owner = owner
        self.pets = pets
        self.daily_plan: list[tuple[Pet, Task]] = []
        self.skipped: list[tuple[Pet, Task, str]] = []

    def generate_plan(self) -> list[tuple[Pet, Task]]:
        """Build a daily plan by selecting tasks sorted by priority that fit within the owner's available time."""
        self.daily_plan = []
        self.skipped = []
        remaining_time = self.owner.available_time

        # Collect all tasks across all pets with a reference to their pet
        all_tasks: list[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.get_tasks():
                if not task.completed:
                    all_tasks.append((pet, task))

        # Sort by priority (1 = highest), then by duration (shortest first)
        all_tasks.sort(key=lambda x: (x[1].priority, x[1].duration))

        for pet, task in all_tasks:
            if task.is_completable(remaining_time):
                self.daily_plan.append((pet, task))
                remaining_time -= task.duration
            else:
                reason = "not enough time" if remaining_time > 0 else "no time left"
                self.skipped.append((pet, task, reason))

        # Second pass: try to fill leftover time with skipped tasks
        still_skipped = []
        for pet, task, reason in self.skipped:
            if task.is_completable(remaining_time):
                self.daily_plan.append((pet, task))
                remaining_time -= task.duration
            else:
                still_skipped.append((pet, task, reason))
        self.skipped = still_skipped

        return self.daily_plan

    def explain_plan(self) -> str:
        """Return a readable summary of the scheduled and skipped tasks."""
        if not self.daily_plan and not self.skipped:
            return "No plan generated yet. Run generate_plan() first."

        lines = [f"Daily plan for {self.owner.name} ({self.owner.available_time} mins available):\n"]

        lines.append("SCHEDULED:")
        if self.daily_plan:
            for pet, task in self.daily_plan:
                lines.append(
                    f"  - [{pet.name}] {task.name} ({task.duration} mins, priority {task.priority}, {task.category})"
                )
        else:
            lines.append("  - No tasks scheduled.")

        lines.append("\nSKIPPED:")
        if self.skipped:
            for pet, task, reason in self.skipped:
                lines.append(
                    f"  - [{pet.name}] {task.name} ({task.duration} mins) — {reason}"
                )
        else:
            lines.append("  - No tasks skipped.")

        lines.append(f"\nTime remaining: {self.get_remaining_time()} mins")
        return "\n".join(lines)

    def get_remaining_time(self) -> int:
        """Return the number of minutes remaining after all scheduled tasks."""
        used = sum(task.duration for _, task in self.daily_plan)
        return self.owner.available_time - used

    def sort_by_time(self) -> list[tuple[Pet, Task]]:
        """return the daily plan sorted by scheduled time."""
        all_tasks = []
        for pest in self.pets:
            for task in pest.get_tasks():
                if not task.completed:
                    all_tasks.append((pest, task))
        return sorted(all_tasks, key=lambda x: x[1].time) 

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> list[tuple[Pet, Task]]:
        """Return tasks filtered by pet name and/or completion status."""
        results = []
        for pet in self.pets:
            if pet_name and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks.values():
                if completed is not None and task.completed != completed:
                    continue
                results.append((pet, task))
        return results 
    
    def detect_conflicts(self) -> list[str]:
        """Return a list of warning messages for tasks scheduled at the same time."""
        seen, warnings = {}, []
        for pet in self.pets:
            for task in (t for t in pet.tasks.values() if not t.completed):
                if task.time in seen:
                    p, t = seen[task.time]
                    warnings.append(f"⚠️ Conflict at {task.time}: [{pet.name}] {task.name} overlaps with [{p.name}] {t.name}")
                else:
                    seen[task.time] = (pet, task)
        return warnings
