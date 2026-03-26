# PawPal+ (Module 2 Project)

**PawPal+** is a pet care planning assistant built with Python and Streamlit. It helps busy pet owners manage and schedule daily care tasks for multiple pets, with intelligent sorting, conflict detection, and recurring task automation.

## Features ✨

### Core Features
- **Multi-pet management** - Track multiple pets (dogs, cats, etc.) with detailed info
- **Task scheduling** - Create tasks with time, duration, priority, and recurrence
- **Daily schedule generation** - Automatically organizes tasks chronologically
- **Priority-based planning** - Supports LOW, MEDIUM, HIGH priority levels
- **Recurring tasks** - Daily and weekly automation (e.g., feeding twice daily)
- **Conflict detection** - Alerts when multiple pets have overlapping tasks

### Algorithmic Intelligence
- **Smart sorting** - Tasks sorted by time using Python's lambda functions
- **Flexible filtering** - View tasks by pet, completion status, or priority
- **Automation** - Mark tasks complete, auto-create next occurrence for daily/weekly tasks
- **Time validation** - Ensures HH:MM format for all task times

## Architecture

The system uses a layered design with four main classes:

- **Task** - Represents a single pet care activity (feeding, walk, grooming, etc.)
- **Pet** - Represents a pet and its list of tasks
- **Owner** - Manages multiple pets and provides centralized data access
- **Scheduler** - Orchestrates sorting, filtering, conflict detection, and scheduling logic

See `UML_DIAGRAM.md` for the complete class diagram.

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### Demo

To see the system in action with sample data:

```bash
python main.py
```

This creates 2 pets (Mochi the dog, Whiskers the cat) with 7 tasks and displays:
- Today's full schedule sorted by time
- Scheduling conflicts
- Per-pet task lists
- Recurring task generation

## Testing

The project includes a comprehensive test suite:

```bash
python -m pytest tests/test_pawpal.py -v
```

**Test Coverage** (15 tests):
- Task completion and status tracking
- Task addition to pets
- Chronological sorting by time
- Conflict detection for overlapping times
- Filtering by pet name and completion status
- Recurring task automation (daily/weekly)
- Owner and pet management

**Confidence Level**: ⭐⭐⭐⭐ (4/5)

The system reliably handles core behaviors. Edge cases for time parsing edge values and overlapping durations could use additional testing.

## Project Structure

```
pawpal_system.py      # Core logic classes (Task, Pet, Owner, Scheduler)
app.py                # Streamlit UI with tabs for schedule/tasks/summary
main.py               # CLI demo script with sample data
tests/test_pawpal.py  # 15 automated tests
UML_DIAGRAM.md        # Mermaid class diagram
reflection.md         # Design decisions and AI collaboration notes
```

## Design Highlights

- **Dataclasses** - Clean, Pythonic object definitions
- **Enums** - Type-safe Priority and Frequency values
- **Session state** - Streamlit persistence for data across page refreshes
- **Separation of concerns** - Logic layer separate from UI
- **Reusable methods** - Scheduler methods can be called independently

## Phase Completion Summary

✅ **Phase 1** - System Design with UML
- Identified 3 core user actions (Feeding, Grooming, Activity/Walks)
- Designed 4-class system with clear responsibilities
- Created Mermaid class diagram

✅ **Phase 2** - Core Implementation
- Implemented all class methods with full logic
- Created CLI demo script (`main.py`)
- Built comprehensive test suite (15 tests, all passing)

✅ **Phase 3** - UI & Backend Integration
- Integrated `pawpal_system` classes into Streamlit app
- Implemented session state persistence
- Wired all UI actions to backend methods

✅ **Phase 4** - Algorithmic Layer
- Sorting by time via lambda functions
- Filtering by pet and completion status
- Recurring task automation
- Conflict detection with warnings

✅ **Phase 5** - Testing & Verification
- 15 comprehensive tests covering all features
- All tests passing with 100% success rate
- Edge cases covered (empty pets, no tasks, conflicts)

✅ **Phase 6** - Documentation & Polish
- Updated README with features and architecture
- Completed reflection with design decisions
- Final UML diagram matches implementation
