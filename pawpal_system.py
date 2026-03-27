from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int        # minutes
    priority: int        # 1 = high, 2 = medium, 3 = low
    category: str        # walk, feeding, meds, grooming, enrichment
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_completable(self, available_time: int) -> bool:
        """Return True if this task fits within the given available time."""
        return self.duration <= available_time


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


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
