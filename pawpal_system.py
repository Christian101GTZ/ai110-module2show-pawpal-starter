from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int        # minutes
    priority: int        # 1 = high, 2 = medium, 3 = low
    category: str        # walk, feeding, meds, grooming, enrichment
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def is_completable(self, available_time: int) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str = ""
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list:
        pass


@dataclass
class Owner:
    name: str
    available_time: int  # minutes per day
    preferences: list = field(default_factory=list)
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.daily_plan: list[Task] = []

    def generate_plan(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass

    def get_remaining_time(self) -> int:
        pass
