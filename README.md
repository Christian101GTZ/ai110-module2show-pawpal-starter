# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built. 

## Smarter Scheduling 

 Pawpal+ includes several algorithms that will make scheduling soo much smarter:

## Smarter Scheduling

PawPal+ includes several algorithms that make scheduling smarter:

1. Sorting: Tasks can be sorted by their scheduled time so the daily plan is easy to follow in order.
2. Filtering: Tasks can be filtered by pet name or completion status to quickly find what's relevant.
3. Recurring Tasks: When a daily or weekly task is marked complete, a new instance is automatically created for the next occurrence.
4. Conflict Detection: The scheduler warns you if two tasks are set to the same start time, helping you spot and fix scheduling mistakes before the day begins.

## Testing PawPal+ 


Run the test suite with:

Tests cover:

Sorting: Tasks are returned in chronological order by scheduled time

Recurrence: Marking a daily task complete creates a new task for the next day

Conflict Detection: Scheduler flags two tasks scheduled at the same time

Task Completion: Marking a task complete updates its status

Confidence Level: ⭐⭐⭐⭐

```bash
python -m pytest
