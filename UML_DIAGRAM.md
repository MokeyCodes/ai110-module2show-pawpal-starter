```mermaid
classDiagram
    class Owner {
        -name: str
        -pets: List[Pet]
        +add_pet(pet): void
        +remove_pet(pet): void
        +get_pets(): List[Pet]
        +get_all_tasks(): List[Task]
    }

    class Pet {
        -name: str
        -species: str
        -age: int
        -tasks: List[Task]
        +add_task(task): void
        +remove_task(task): void
        +get_tasks(): List[Task]
    }

    class Task {
        -description: str
        -time: str
        -duration_minutes: int
        -frequency: Frequency
        -priority: Priority
        -completed: bool
        -pet_name: str
        +mark_complete(): void
        +get_next_occurrence(): Task
    }

    class Scheduler {
        -owner: Owner
        +get_today_schedule(): List[Task]
        +sort_tasks_by_time(tasks): List[Task]
        +filter_by_status(tasks, completed): List[Task]
        +filter_by_pet(tasks, pet_name): List[Task]
        +detect_conflicts(tasks): List[str]
    }

    class Frequency {
        <<enumeration>>
        ONCE
        DAILY
        WEEKLY
    }

    class Priority {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
    }

    Owner "1" --> "*" Pet : manages
    Pet "1" --> "*" Task : has
    Scheduler --> Owner : uses
    Task --> Frequency : uses
    Task --> Priority : uses
```

**Key Relationships:**
- **Owner → Pet** (1 to many): An owner can have multiple pets
- **Pet → Task** (1 to many): Each pet can have multiple tasks
- **Scheduler → Owner**: The scheduler accesses pets and tasks through the owner
- **Task uses Frequency & Priority**: Enums that define task attributes

