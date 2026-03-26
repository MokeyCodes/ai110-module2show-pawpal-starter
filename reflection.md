# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The 3 core user actions identified:
1. **Feeding** - Schedule and track daily meals
2. **Grooming** - Schedule grooming activities (bathing, brushing, nail care)
3. **Activity/Walks** - Schedule exercise and walking time

Classes designed:
- **Task**: Represents a single pet care activity (e.g., "Morning Walk"). Stores description, time, duration, frequency, and completion status.
- **Pet**: Represents a pet (name, species, age). Maintains a list of tasks assigned to the pet.
- **Owner**: Represents the pet owner. Manages multiple pets and provides centralized access to all pet data.
- **Scheduler**: The "brain" of the system. Retrieves tasks from owner's pets, sorts/filters by time and priority, detects conflicts, and handles recurring task automation.

**b. Design changes**

Yes, the design evolved during implementation in a positive way:

1. **Frequency Enum Addition** - Initially considered frequency as a simple string ("daily", "weekly"), but converted to an Enum for type safety and validation. This prevented bugs and made the code more maintainable.

2. **Scheduler as Coordinator** - The Scheduler class became more powerful than initially planned. It evolved from just "retrieving tasks" to also handling sorting, filtering, and conflict detection. This reduced complexity in the UI layer by centralizing scheduling logic in one place.

3. **str() Methods for Readability** - Added comprehensive `__str__()` methods to all classes early. This proved invaluable during development for debugging and for the CLI demo, making the system much more user-friendly.

4. **Session State Persistence** - During Phase 3, realized Streamlit's stateless nature required storing the Owner object in `st.session_state`. This wasn't explicitly in the original design but became essential for the UI to work properly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers these constraints:
1. **Time** - Tasks are sorted chronologically (08:00, 09:30, 14:00, etc.)
2. **Pet assignment** - Each task belongs to a specific pet (can't be reassigned)
3. **Priority level** - Tasks marked as HIGH, MEDIUM, or LOW (shown in UI for human decision)
4. **Duration** - Task duration tracked to help estimate total time needed
5. **Frequency** - Recurring (DAILY/WEEKLY) vs one-time tasks

**Decision rationale**: For a busy pet owner, **time is the most critical constraint** because they need to see what's scheduled when. Priority is secondary because pet owners know their pets' needs (feeding is always high priority). Duration matters for planning but doesn't block scheduling like time does. Frequency is essential for automation to reduce manual task entry.

The scheduler intentionally **does not optimize scheduling** (e.g., reorder tasks) - instead it displays tasks in time order and flags conflicts. This respects the human's intent while making conflicts visible.

**b. Tradeoffs**

**Tradeoff: Exact time matching for conflict detection instead of duration-aware overlap detection**

Current approach:
- Detects conflicts when multiple tasks have the *same* scheduled time (e.g., both at 08:00)
- Simple, fast, easy to understand

Alternative (not implemented):
- Would calculate actual duration intervals and detect overlaps (e.g., 08:00-08:30 overlaps with 08:15-08:45)
- More accurate but much more complex

**Why this tradeoff is reasonable**:
- Pet care intervals are typically non-overlapping by design (owner does one task at a time)
- A human reviewing the schedule can visually see if a 30-min walk ending at 08:30 conflicts with a 09:00 feeding
- Exact-match detection is good enough to catch the most common issue: "I scheduled two pets for the same time"
- Added complexity of duration math would make the code harder to maintain for minimal value in this scenario

---

## 3. AI Collaboration

**a. How you used AI**

I used AI (Claude) throughout the project as a collaborative partner with my human judgment:

1. **Design Phase (Phase 1)**: Asked AI to help brainstorm classes, attributes, and relationships. AI created the initial Mermaid UML diagram based on my core actions (Feeding, Grooming, Activity). Instead of accepting it blindly, I reviewed it and refined the relationships (e.g., ensuring the Scheduler only reads from Owner, not directly manipulating tasks).

2. **Implementation Phase (Phase 2)**: Used AI to generate method implementations with actual logic. For example:
   - `Task.get_next_occurrence()` using timedelta for recurring tasks
   - `Scheduler.sort_tasks_by_time()` using lambda functions
   - `Scheduler.detect_conflicts()` grouping tasks by time
   This saved time on boilerplate while I focused on logic correctness.

3. **Testing Phase (Phase 5)**: AI generated comprehensive test cases, but I refined them to ensure they tested what actually mattered (edge cases like empty pet lists, conflicting times).

4. **UI Integration (Phase 3)**: AI suggested using `st.session_state` for Owner persistence and generated the Streamlit layout. I then modified it to add tabs and better organize features.

**Most helpful prompts**:
- "Generate a Mermaid class diagram for these classes..."
- "Write the full implementation for [specific method] that [requirement]"
- "Create a test that verifies [specific behavior]"
- "Here's my current UI code, integrate this backend class with proper session state"

**b. Judgment and verification**

**Moment where I didn't accept AI suggestion as-is**:
AI suggested storing task completion state in the Task object itself. While this works functionally, I realized this could lead to complex state management in the UI trying to persist task completion across Streamlit reruns. Instead, I kept tasks as simple data containers and would store completion state in `st.session_state` during a future enhancement (the Streamlit caching layer handles this).

**How I evaluated**:
- I always ran the demo script (`main.py`) after each major change to verify behavior
- I ran the full test suite (`pytest`) to check for regressions
- I manually tested the Streamlit app to see if the UI felt intuitive
- I read through the generated code carefully, not just accepting it

**Key principle**: AI is best for generating structure and boilerplate. I retained control over architectural decisions, algorithm tradeoffs, and testing strategy.

---

## 4. Testing and Verification

**a. What you tested**

I created 15 tests organized into 8 test classes:

1. **Task Completion** (2 tests)
   - Verify `mark_complete()` changes status
   - Verify completed tasks appear in filtered results

2. **Task Addition** (3 tests)
   - Adding a single task increases pet's task count
   - Task's pet_name is set when added to pet
   - Multiple tasks can be added to one pet

3. **Sorting** (2 tests)
   - Tasks are sorted by time in HH:MM format
   - get_today_schedule() returns pre-sorted results

4. **Conflict Detection** (2 tests)
   - Conflicts detected when 2+ tasks at same time
   - No conflicts when tasks at different times

5. **Filtering** (1 test)
   - filter_by_pet() returns only tasks for that pet

6. **Recurrence** (3 tests)
   - ONCE frequency doesn't create next occurrence
   - DAILY frequency creates task for next day
   - WEEKLY frequency creates task for next week

7. **Owner/Pet Management** (2 tests)
   - Pets can be added to owner
   - get_all_tasks() collects tasks from all pets

**Why these tests mattered**: These behaviors are the *core* of the system. If sorting fails, the schedule is useless. If conflicts aren't detected, users don't know about scheduling problems. If recurring tasks don't work, users must manually re-add daily feeding. These tests give me confidence the system won't silently fail in common scenarios.

**b. Confidence**

**Confidence Level**: ⭐⭐⭐⭐ (4/5)

**Why 4 stars and not 5**:
- All 15 tests pass with green checkmarks ✅
- Core logic is rock-solid (sorting, filtering, recurrence all work correctly)
- Edge cases handled well (empty pet lists, no tasks, conflicts)

**What would push it to 5 stars**:
- Test time parsing edge cases (e.g., "23:59" wrapping to next day)
- Test overlapping task durations (not just exact time matches)
- Test task removal and edge cases
- Performance testing with 1000+ tasks
- Integration tests with Streamlit UI persistence

**Additional testing I'd do next**:
- Create pets/tasks via the Streamlit UI and verify they persist across page reloads
- Test with malformed inputs (HH:MM with invalid hours, negative durations)
- Simulate a week-long schedule to verify recurring tasks generate correctly

---

## 5. Reflection

**a. What went well**

**Most satisfied with**: The clean separation of concerns. The `pawpal_system.py` logic layer is completely independent of Streamlit. This means:
- I can run `python main.py` to test logic without a web server
- Tests import only `pawpal_system.py`, not the UI
- If I ever port this to a mobile app or CLI, I just reuse the logic layer
- The Scheduler class is truly reusable—any UI can call its methods

This architecture decision has proven its worth throughout the project.

**Second place**: The test suite. Having 15 passing tests gave me confidence to refactor and improve code without fear of breaking things. When I added Frequency/Priority enums or changed conflict detection logic, I ran tests immediately and knew if something broke.

**Third place**: The Streamlit UI's three-tab design. It's clean, intuitive, and showcases all the features without overwhelming the user. The sidebar for pet management is a nice touch that keeps the main area focused.

**b. What you would improve**

If I had another iteration:

1. **Task editing and deletion** - Currently can only add tasks, not edit or remove them. Would add an "Manage Tasks" view where you can delete completed tasks or edit details.

2. **Time-aware conflict detection** - Currently flags exact-time matches. Would calculate actual duration overlaps (08:00-08:30 vs 08:15-08:45) for real-world accuracy.

3. **Persistence to file** - Currently pets/tasks live only in `st.session_state` (lost on browser refresh). Would add JSON file saving so users don't lose data.

4. **Priority-based scheduling** - Currently just displays priority info. Could add a "Smart Schedule" view that prioritizes HIGH tasks first, clusters related tasks, and suggests optimal ordering.

5. **Multi-user support** - Currently one Owner per session. Would add multi-user support with different schedules per user.

6. **Mobile-first responsive design** - Current UI works but isn't optimized for phones. Would redesign for mobile-first.

**c. Key takeaway**

**The biggest lesson**: Start with a **clear UML design before coding**, then implement incrementally with tests. This project felt much more manageable than if I had started coding immediately. Here's why:

- The UML gave me a map before building the house. When Phase 3 seemed complex ("how do I connect UI to backend?"), I could refer back to the architecture.
- Writing tests *as I built features* (not at the end) meant I caught bugs immediately, not after writing 1000 lines of code.
- Using an intermediate CLI demo script (`main.py`) before the Streamlit UI meant I verified the backbone worked before adding fancy UI layers.

**Secondary lesson**: AI is a powerful collaboration tool, but only if you maintain architectural control. I didn't just accept AI's suggestions; I verified them with tests, reviewed them critically, and sometimes chose the *simpler* approach over the AI's "more advanced" idea.

The phase-based structure of this project (Design → Implementation → Testing → UI → Reflection) is genuinely how professional software gets built, just compressed into 4 hours instead of 4 weeks.
