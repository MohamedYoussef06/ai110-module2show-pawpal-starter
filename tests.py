import pytest
from pawpal_system import Pet, Task, CreateTask


@pytest.fixture
def sample_pet():
    return Pet(name="Mochi", breed="Shiba Inu", age=3, weight=22.5)


@pytest.fixture
def sample_task():
    return Task(
        task_name="Morning Walk",
        task_description="Walk around the block",
        task_time="7:00 AM",
        priority="high",
        duration_minutes=30
    )


def test_mark_complete_changes_status(sample_task):
    """Calling mark_complete() should set completed to True."""
    assert sample_task.completed is False
    sample_task.mark_complete()
    assert sample_task.completed is True


def test_add_task_increases_pet_task_count(sample_pet):
    """Adding a task to a Pet should increase its task count by 1."""
    create_task = CreateTask()
    initial_count = len(sample_pet.tasks)

    create_task.create_task(sample_pet, "Evening Walk", "Walk after dinner", "6:00 PM", "medium", 20)

    assert len(sample_pet.tasks) == initial_count + 1
