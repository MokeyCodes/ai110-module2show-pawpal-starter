"""
PawPal+ Demo Script
A CLI demo showing the scheduling system in action with sample data.
"""

from pawpal_system import Owner, Pet, Task, Scheduler, Frequency, Priority


def main():
    # Create an owner
    print("=" * 50)
    print("🐾 PAWPAL+ DEMO - Pet Care Scheduling System")
    print("=" * 50)

    owner = Owner(name="Jordan")
    print(f"\n✓ Created owner: {owner}")

    # Create pets
    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Whiskers", species="cat", age=5)
    owner.add_pet(dog)
    owner.add_pet(cat)
    print(f"✓ Added {dog}")
    print(f"✓ Added {cat}")

    # Add tasks for Mochi (dog)
    print(f"\n--- Tasks for {dog.name} ---")
    morning_walk = Task(
        description="Morning walk",
        time="08:00",
        duration_minutes=30,
        frequency=Frequency.DAILY,
        priority=Priority.HIGH
    )
    dog.add_task(morning_walk)
    print(f"✓ {morning_walk}")

    breakfast = Task(
        description="Breakfast",
        time="08:30",
        duration_minutes=15,
        frequency=Frequency.DAILY,
        priority=Priority.HIGH
    )
    dog.add_task(breakfast)
    print(f"✓ {breakfast}")

    afternoon_walk = Task(
        description="Afternoon walk",
        time="14:00",
        duration_minutes=30,
        frequency=Frequency.DAILY,
        priority=Priority.MEDIUM
    )
    dog.add_task(afternoon_walk)
    print(f"✓ {afternoon_walk}")

    grooming = Task(
        description="Grooming",
        time="16:00",
        duration_minutes=45,
        frequency=Frequency.WEEKLY,
        priority=Priority.MEDIUM
    )
    dog.add_task(grooming)
    print(f"✓ {grooming}")

    # Add tasks for Whiskers (cat)
    print(f"\n--- Tasks for {cat.name} ---")
    cat_breakfast = Task(
        description="Breakfast",
        time="08:00",
        duration_minutes=10,
        frequency=Frequency.DAILY,
        priority=Priority.HIGH
    )
    cat.add_task(cat_breakfast)
    print(f"✓ {cat_breakfast}")

    cat_lunch = Task(
        description="Lunch",
        time="12:00",
        duration_minutes=10,
        frequency=Frequency.DAILY,
        priority=Priority.HIGH
    )
    cat.add_task(cat_lunch)
    print(f"✓ {cat_lunch}")

    playtime = Task(
        description="Playtime/Activity",
        time="14:00",
        duration_minutes=20,
        frequency=Frequency.DAILY,
        priority=Priority.MEDIUM
    )
    cat.add_task(playtime)
    print(f"✓ {playtime}")

    # Create scheduler
    print("\n" + "=" * 50)
    scheduler = Scheduler(owner)
    print(f"\n✓ Created scheduler: {scheduler}\n")

    # Display today's schedule
    print("=" * 50)
    print("📅 TODAY'S SCHEDULE (Sorted by Time)")
    print("=" * 50)
    today_schedule = scheduler.get_today_schedule()
    for task in today_schedule:
        print(task)

    # Check for conflicts
    print("\n" + "=" * 50)
    print("🔍 CONFLICT DETECTION")
    print("=" * 50)
    conflicts = scheduler.detect_conflicts(today_schedule)
    if conflicts:
        for conflict in conflicts:
            print(conflict)
    else:
        print("✓ No scheduling conflicts detected!")

    # Demonstrate filtering
    print("\n" + "=" * 50)
    print(f"🐕 TASKS FOR {dog.name.upper()}")
    print("=" * 50)
    mochi_tasks = scheduler.filter_by_pet(today_schedule, dog.name)
    for task in mochi_tasks:
        print(task)

    print(f"\n" + "=" * 50)
    print(f"🐱 TASKS FOR {cat.name.upper()}")
    print("=" * 50)
    whiskers_tasks = scheduler.filter_by_pet(today_schedule, cat.name)
    for task in whiskers_tasks:
        print(task)

    # Demonstrate task completion
    print("\n" + "=" * 50)
    print("✅ MARKING TASK AS COMPLETE")
    print("=" * 50)
    print(f"Before: {morning_walk}")
    morning_walk.mark_complete()
    print(f"After:  {morning_walk}")

    # Show completed tasks
    completed_tasks = scheduler.filter_by_status(owner.get_all_tasks(), completed=True)
    print(f"\n✓ Completed tasks: {len(completed_tasks)}")
    for task in completed_tasks:
        print(f"  {task}")

    # Demonstrate recurring task creation
    print("\n" + "=" * 50)
    print("🔄 RECURRING TASK AUTOMATION")
    print("=" * 50)
    print(f"Original daily task: {breakfast}")
    next_breakfast = breakfast.get_next_occurrence()
    if next_breakfast:
        print(f"Next occurrence:    {next_breakfast}")
    else:
        print("Not a recurring task")

    print("\n" + "=" * 50)
    print("✓ Demo Complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
