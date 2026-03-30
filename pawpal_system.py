from dataclasses import dataclass, field
from typing import List


# --- Data Classes ---

@dataclass
class Pet:
    name: str
    breed: str
    age: int
    weight: float


@dataclass
class Task:
    task_name: str
    task_description: str
    task_time: str


# --- Logic Classes ---

class AddPet:
    def add_pet(self, name: str, breed: str, age: int, weight: float) -> Pet:
        pass


class CreateTask:
    def create_task(self, task_name: str, task_description: str, task_time: str) -> Task:
        pass


class SwitchProfile:
    pet_profiles: List[Pet] = field(default_factory=list)
    current_profile: Pet = None

    def add_profile(self, pet: Pet) -> None:
        pass

    def switch_profile(self, pet_name: str) -> Pet:
        pass


class CreateSchedule:
    tasks: List[Task] = field(default_factory=list)
    generated_schedule: List[Task] = field(default_factory=list)

    def create_schedule(self, tasks: List[Task]) -> List[Task]:
        pass


class CheckTasks:
    today_schedule: List[Task] = field(default_factory=list)
    last_updated: str = ""

    def update_schedule(self, schedule: List[Task]) -> None:
        pass

    def get_today_schedule(self) -> List[Task]:
        pass
