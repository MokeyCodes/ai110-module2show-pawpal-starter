"""
Test suite for PawPal+ system.
Tests core behaviors: task completion, task addition, sorting, filtering, conflicts, and recurrence.
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler, Frequency, Priority


class TestTaskCompletion:
    """Tests for task completion behavior."""

    def test_mark_complete_changes_status(self):
        """Verify that marking a task complete changes its completed status."""
        task = Task(
            description="Feeding",
            time="08:00",
            duration_minutes=15,
            frequency=Frequency.DAILY,
            priority=Priority.HIGH
        )
        assert task.completed is False
        task.mark_complete()
        assert task.completed is True

    def test_completed_task_in_filter(self):
        """Verify completed tasks can be filtered correctly."""
        task1 = Task(
            description="Walk",
            time="09:00",
            duration_minutes=30,
            frequency=Frequency.DAILY,
            priority=Priority.HIGH
        )
        task2 = Task(
            description="Feeding",
            time="12:00",
            duration_minutes=15,
            frequency=Frequency.DAILY,
            priority=Priority.HIGH
        )
        task1.mark_complete()

        owner = Owner(name="Test Owner")
        pet = Pet(name="TestPet", species="dog", age=2)
        owner.add_pet(pet)
        pet.add_task(task1)
        pet.add_task(task2)

        scheduler = Scheduler(owner)
        all_tasks = owner.get_all_tasks()

        completed = scheduler.filter_by_status(all_tasks, completed=True)
        incomplete = scheduler.filter_by_status(all_tasks, completed=False)

        assert len(completed) == 1
        assert len(incomplete) == 1
        assert task1 in completed
        assert task2 in incomplete


class TestTaskAddition:
    """Tests for adding tasks to pets."""

    def test_add_task_to_pet(self):
        """Verify adding a task to a pet increases task count."""
        pet = Pet(name="Mochi", species="dog", age=3)
        assert len(pet.get_tasks()) == 0

        task = Task(
            description="Walk",
            time="08:00",
            duration_minutes=30,
            frequency=Frequency.DAILY,
            priority=Priority.HIGH
        )
        pet.add_task(task)
        assert len(pet.get_tasks()) == 1

    def test_task_pet_name_assigned_on_add(self):
        """Verify that when a task is added to a pet, its pet_name is set."""
        pet = Pet(name="Whiskers", species="cat", age=5)
        task = Task(
            description="Feeding",
            time="08:00",
            duration_minutes=10,
            frequency=Frequency.DAILY,
            priority=Priority.HIGH
        )
        assert task.pet_name == ""
        pet.add_task(task)
        assert task.pet_name == "Whiskers"

    def test_add_multiple_tasks_to_pet(self):
        """Verify multiple tasks can be added to a single pet."""
        pet = Pet(name="Mochi", species="dog", age=3)

        task1 = Task(
            description="Walk",
            time="08:00",
            duration_minutes=30,
            frequency=Frequency.DAILY,
            priority=Priority.HIGH
        )
        task2 = Task(
            description="Feeding",
            time="12:00",
            duration_minutes=15,
            frequency=Frequency.DAILY,
            priority=Priority.HIGH
        )
        task3 = Task(
            description="Playtime",
            time="17:00",
            duration_minutes=30,
            frequency=Frequency.DAILY,
            priority=Priority.MEDIUM
        )

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        assert len(pet.get_tasks()) == 3


class TestSorting:
    """Tests for sorting tasks by time."""

    def test_sort_tasks_by_time(self):
        """Verify tasks are sorted chronologically by time."""
        owner = Owner(name="Jordan")
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)

        # Add tasks in non-chronological order
        task1 = Task("Walk", "14:00", 30, Frequency.DAILY, Priority.HIGH)
        task2 = Task("Feeding", "08:00", 15, Frequency.DAILY, Priority.HIGH)
        task3 = Task("Playtime", "11:00", 30, Frequency.DAILY, Priority.MEDIUM)

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_tasks_by_time(owner.get_all_tasks())

        assert sorted_tasks[0].time == "08:00"
        assert sorted_tasks[1].time == "11:00"
        assert sorted_tasks[2].time == "14:00"

    def test_get_today_schedule_is_sorted(self):
        """Verify get_today_schedule returns tasks sorted by time."""
        owner = Owner(name="Jordan")
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)

        task1 = Task("Afternoon Walk", "16:00", 30, Frequency.DAILY, Priority.MEDIUM)
        task2 = Task("Morning Feeding", "07:00", 15, Frequency.DAILY, Priority.HIGH)
        task3 = Task("Lunch", "12:00", 20, Frequency.DAILY, Priority.HIGH)

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        scheduler = Scheduler(owner)
        schedule = scheduler.get_today_schedule()

        assert schedule[0].time == "07:00"
        assert schedule[1].time == "12:00"
        assert schedule[2].time == "16:00"


class TestConflictDetection:
    """Tests for detecting task conflicts."""

    def test_detect_conflict_same_time(self):
        """Verify conflicts are detected when tasks are at the same time."""
        owner = Owner(name="Jordan")
        dog = Pet(name="Mochi", species="dog", age=3)
        cat = Pet(name="Whiskers", species="cat", age=5)
        owner.add_pet(dog)
        owner.add_pet(cat)

        dog_task = Task("Dog Feeding", "08:00", 15, Frequency.DAILY, Priority.HIGH)
        cat_task = Task("Cat Feeding", "08:00", 10, Frequency.DAILY, Priority.HIGH)

        dog.add_task(dog_task)
        cat.add_task(cat_task)

        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

        assert len(conflicts) == 1
        assert "08:00" in conflicts[0]

    def test_no_conflict_different_times(self):
        """Verify no conflicts when tasks are at different times."""
        owner = Owner(name="Jordan")
        dog = Pet(name="Mochi", species="dog", age=3)
        cat = Pet(name="Whiskers", species="cat", age=5)
        owner.add_pet(dog)
        owner.add_pet(cat)

        dog_task = Task("Dog Feeding", "08:00", 15, Frequency.DAILY, Priority.HIGH)
        cat_task = Task("Cat Feeding", "09:00", 10, Frequency.DAILY, Priority.HIGH)

        dog.add_task(dog_task)
        cat.add_task(cat_task)

        scheduler = Scheduler(owner)
        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

        assert len(conflicts) == 0


class TestFiltering:
    """Tests for filtering tasks by pet or status."""

    def test_filter_by_pet_name(self):
        """Verify filtering tasks by pet name returns correct tasks."""
        owner = Owner(name="Jordan")
        dog = Pet(name="Mochi", species="dog", age=3)
        cat = Pet(name="Whiskers", species="cat", age=5)
        owner.add_pet(dog)
        owner.add_pet(cat)

        dog_task1 = Task("Walk", "08:00", 30, Frequency.DAILY, Priority.HIGH)
        dog_task2 = Task("Feeding", "12:00", 15, Frequency.DAILY, Priority.HIGH)
        cat_task = Task("Playtime", "14:00", 20, Frequency.DAILY, Priority.MEDIUM)

        dog.add_task(dog_task1)
        dog.add_task(dog_task2)
        cat.add_task(cat_task)

        scheduler = Scheduler(owner)
        dog_tasks = scheduler.filter_by_pet(owner.get_all_tasks(), "Mochi")
        cat_tasks = scheduler.filter_by_pet(owner.get_all_tasks(), "Whiskers")

        assert len(dog_tasks) == 2
        assert len(cat_tasks) == 1
        assert all(t.pet_name == "Mochi" for t in dog_tasks)
        assert all(t.pet_name == "Whiskers" for t in cat_tasks)


class TestRecurrence:
    """Tests for recurring task behavior."""

    def test_once_task_no_recurrence(self):
        """Verify tasks with ONCE frequency don't create next occurrences."""
        task = Task(
            description="One-time Vet Visit",
            time="10:00",
            duration_minutes=60,
            frequency=Frequency.ONCE,
            priority=Priority.HIGH
        )
        next_task = task.get_next_occurrence()
        assert next_task is None

    def test_daily_task_creates_next_day(self):
        """Verify daily tasks create next occurrence for following day."""
        task = Task(
            description="Feeding",
            time="08:00",
            duration_minutes=15,
            frequency=Frequency.DAILY,
            priority=Priority.HIGH
        )
        next_task = task.get_next_occurrence()

        assert next_task is not None
        assert next_task.description == "Feeding"
        assert next_task.frequency == Frequency.DAILY
        assert next_task.completed is False
        # Time should be same (08:00)
        assert next_task.time == "08:00"

    def test_weekly_task_creates_next_week(self):
        """Verify weekly tasks create next occurrence a week later."""
        task = Task(
            description="Grooming",
            time="10:00",
            duration_minutes=60,
            frequency=Frequency.WEEKLY,
            priority=Priority.MEDIUM
        )
        next_task = task.get_next_occurrence()

        assert next_task is not None
        assert next_task.description == "Grooming"
        assert next_task.frequency == Frequency.WEEKLY
        assert next_task.completed is False


class TestOwnerAndPetManagement:
    """Tests for managing owners and pets."""

    def test_add_pet_to_owner(self):
        """Verify pets can be added to an owner."""
        owner = Owner(name="Jordan")
        assert len(owner.get_pets()) == 0

        pet1 = Pet(name="Mochi", species="dog", age=3)
        pet2 = Pet(name="Whiskers", species="cat", age=5)

        owner.add_pet(pet1)
        owner.add_pet(pet2)

        assert len(owner.get_pets()) == 2

    def test_get_all_tasks_from_multiple_pets(self):
        """Verify get_all_tasks returns tasks from all pets."""
        owner = Owner(name="Jordan")
        dog = Pet(name="Mochi", species="dog", age=3)
        cat = Pet(name="Whiskers", species="cat", age=5)
        owner.add_pet(dog)
        owner.add_pet(cat)

        dog_task = Task("Walk", "08:00", 30, Frequency.DAILY, Priority.HIGH)
        cat_task = Task("Playtime", "14:00", 20, Frequency.DAILY, Priority.MEDIUM)

        dog.add_task(dog_task)
        cat.add_task(cat_task)

        all_tasks = owner.get_all_tasks()
        assert len(all_tasks) == 2
        assert dog_task in all_tasks
        assert cat_task in all_tasks


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
