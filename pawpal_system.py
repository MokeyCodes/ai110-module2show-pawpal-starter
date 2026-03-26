"""
PawPal+ System - Core scheduling logic for pet care management.

Classes:
- Task: Represents a single pet care activity
- Pet: Represents a pet with associated tasks
- Owner: Manages multiple pets
- Scheduler: Orchestrates task scheduling and optimization
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum


class Frequency(Enum):
    """Task frequency options."""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Represents a single pet care task."""

    description: str
    time: str  # Format: "HH:MM" (e.g., "09:00")
    duration_minutes: int
    frequency: Frequency
    priority: Priority
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def get_next_occurrence(self) -> Optional['Task']:
        """Generate the next occurrence of this task if it's recurring."""
        if self.frequency == Frequency.ONCE:
            return None

        # Parse current time
        current_time = datetime.strptime(self.time, "%H:%M")

        if self.frequency == Frequency.DAILY:
            next_time = current_time + timedelta(days=1)
        elif self.frequency == Frequency.WEEKLY:
            next_time = current_time + timedelta(weeks=1)
        else:
            return None

        # Create new task with same properties but reset completed status
        return Task(
            description=self.description,
            time=next_time.strftime("%H:%M"),
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            completed=False,
            pet_name=self.pet_name
        )

    def __str__(self) -> str:
        """Return a readable string representation of the task."""
        status = "✓" if self.completed else "○"
        return f"{status} [{self.time}] {self.description} ({self.duration_minutes}min) [{self.priority.value}]"


@dataclass
class Pet:
    """Represents a pet with tasks."""

    name: str
    species: str  # e.g., "dog", "cat"
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def __str__(self) -> str:
        """Return a readable string representation of the pet."""
        return f"{self.name} ({self.species}, {self.age} years old) - {len(self.tasks)} tasks"


@dataclass
class Owner:
    """Represents a pet owner managing multiple pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's pet list."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def __str__(self) -> str:
        """Return a readable string representation of the owner."""
        return f"{self.name} owns {len(self.pets)} pet(s)"


class Scheduler:
    """Orchestrates scheduling logic for pet care tasks."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_today_schedule(self) -> List[Task]:
        """Retrieve and organize all incomplete tasks for today."""
        all_tasks = self.owner.get_all_tasks()
        incomplete_tasks = self.filter_by_status(all_tasks, completed=False)
        return self.sort_tasks_by_time(incomplete_tasks)

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks chronologically by time."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_status(self, tasks: List[Task], completed: bool = False) -> List[Task]:
        """Filter tasks by completion status."""
        return [task for task in tasks if task.completed == completed]

    def filter_by_pet(self, tasks: List[Task], pet_name: str) -> List[Task]:
        """Filter tasks by pet name."""
        return [task for task in tasks if task.pet_name == pet_name]

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect tasks scheduled at the same time and return warning messages."""
        conflicts = []
        time_groups = {}

        # Group tasks by time
        for task in tasks:
            if task.time not in time_groups:
                time_groups[task.time] = []
            time_groups[task.time].append(task)

        # Find conflicts (2+ tasks at same time)
        for time, tasks_at_time in time_groups.items():
            if len(tasks_at_time) > 1:
                pet_names = [t.pet_name for t in tasks_at_time]
                conflicts.append(
                    f"⚠️ Conflict at {time}: {', '.join(pet_names)} have overlapping tasks"
                )

        return conflicts

    def __str__(self) -> str:
        """Return a summary of the scheduler's current state."""
        all_tasks = self.owner.get_all_tasks()
        incomplete = len(self.filter_by_status(all_tasks, completed=False))
        complete = len(self.filter_by_status(all_tasks, completed=True))
        return f"Scheduler for {self.owner.name}: {incomplete} todo, {complete} completed"
