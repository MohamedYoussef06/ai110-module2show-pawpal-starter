from dataclasses import dataclass, field
from typing import List, Optional


# --- Data Classes ---

@dataclass
class Task:
    task_name: str
    task_description: str
    task_time: str
    priority: str           # "low", "medium", "high"
    duration_minutes: int
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True


@dataclass
class Pet:
    name: str
    breed: str
    age: int
    weight: float
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Owner:
    owner_name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


# --- Logic Classes ---

class AddPet:
    def add_pet(self, owner: Owner, name: str, breed: str, age: int, weight: float) -> Pet:
        pet = Pet(name=name, breed=breed, age=age, weight=weight)
        owner.add_pet(pet)
        return pet


class CreateTask:
    VALID_PRIORITIES = {"low", "medium", "high"}

    def create_task(self, pet: Pet, task_name: str, task_description: str, task_time: str, priority: str, duration_minutes: int) -> Task:
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {self.VALID_PRIORITIES}")
        task = Task(
            task_name=task_name,
            task_description=task_description,
            task_time=task_time,
            priority=priority,
            duration_minutes=duration_minutes
        )
        pet.tasks.append(task)
        return task


class CreateSchedule:
    PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

    def __init__(self):
        self.generated_schedule: List[Task] = []

    def create_schedule(self, pet: Pet) -> List[Task]:
        sorted_tasks = sorted(pet.tasks, key=lambda t: self.PRIORITY_ORDER.get(t.priority, 2))
        self.generated_schedule = sorted_tasks
        return self.generated_schedule


class CheckTasks:
    def __init__(self, scheduler: "Scheduler"):
        self.scheduler: "Scheduler" = scheduler

    def update_schedule(self) -> None:
        self.scheduler.organize_schedule()

    def get_today_schedule(self) -> List[Task]:
        return self.scheduler.schedule


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner: Owner = owner
        self.active_pet: Optional[Pet] = None
        self.schedule: List[Task] = []
        self._create_schedule = CreateSchedule()

    def set_active_pet(self, pet_name: str) -> None:
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            raise ValueError(f"No pet named '{pet_name}' found for owner '{self.owner.owner_name}'")
        self.active_pet = pet

    def collect_tasks(self) -> List[Task]:
        if self.active_pet is None:
            raise RuntimeError("No active pet set. Call set_active_pet() first.")
        return self.active_pet.tasks

    def organize_schedule(self) -> List[Task]:
        if self.active_pet is None:
            raise RuntimeError("No active pet set. Call set_active_pet() first.")
        self.schedule = self._create_schedule.create_schedule(self.active_pet)
        return self.schedule

    def get_schedule_summary(self) -> str:
        if not self.schedule:
            return "No schedule generated yet."
        lines = [f"Schedule for {self.active_pet.name}:"]
        for task in self.schedule:
            lines.append(f"  [{task.priority.upper()}] {task.task_name} at {task.task_time} ({task.duration_minutes} min)")
        return "\n".join(lines)
