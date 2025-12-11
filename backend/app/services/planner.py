from app.schemas.planning import GoalInput, PlanStep, PlanResponse

from typing import Literal, List, Tuple

GoalCategory = Literal["learning", "project", "job", "health", "generic"]

STEP_TEMPLATES = {
    "learning": [
        ("Define your learning scope", "Clarify what exactly you want to learn and why."),
        ("Gather high-quality learning resources", "Pick 1–2 courses or books instead of many."),
        ("Create a study schedule", "Plan a daily or weekly routine based on your timeframe."),
        ("Do hands-on practice", "Work on small exercises or mini-projects."),
        ("Review and reinforce", "Summarize what you learned and identify remaining gaps.")
    ],
    "project": [
        ("Define the project requirements", "Describe the outcome, constraints, and success criteria."),
        ("Set up your environment", "Create repo, install dependencies, prepare folders."),
        ("Build core features", "Implement the essential components first."),
        ("Polish and test", "Refactor, fix bugs, improve UX."),
        ("Deploy and validate", "Ship the project and verify that it works end-to-end.")
    ],
    "job": [
        ("Clarify your target role", "Define the type of job, skills, and companies you aim for."),
        ("Polish your resume and portfolio", "Highlight skills and remove weak items."),
        ("Upgrade your profiles", "Fix LinkedIn, GitHub, website."),
        ("Apply systematically", "Use a tracker, send quality applications."),
        ("Prepare for interviews", "Study common questions, practice mock interviews.")
    ],
    "health": [
        ("Define your health target", "Clarify weight, strength, or wellness goals."),
        ("Set a simple routine", "Pick exercises or habits that you can maintain."),
        ("Track consistency", "Log your daily progress."),
        ("Adjust based on results", "If something isn’t working, reduce friction."),
        ("Review your progress", "Evaluate outcomes after your timeframe.")
    ],
    "generic": [
        ("Clarify your goal", "Write a clear and specific version of the goal."),
        ("Break it down", "Identify 3–5 sub-tasks."),
        ("Plan the timeline", "Spread the sub-tasks across available days."),
        ("Execute systematically", "Work on one part at a time."),
        ("Review outcomes", "Measure how well the plan worked.")
    ]
}


def classify_goal_text(goal: str) -> GoalCategory:
    """
    Very simple keyword-based classifier for the user's goal text.
    Returns a coarse category that we will use to pick step templates. 
    """

    text = goal.lower()

    if any(word in text for word in ["learn", "study", "course", "exam", "test", "skill"]):
        return "learning"
    
    if any(word in text for word in ["build", "create", "ship", "launch", "app", "website", "project"]):
        return "project"
    
    if any(word in text for word in ["job", "resume", "cv", "portfolio", "interview", "linkedin", "cover letter"]):
        return "job"
    
    if any(word in text for word in ["health", "exercise", "workout", "diet", "weight", "sleep", "steps per day"]):
        return "health"
    
    return "generic"


def compute_step_day_ranges(num_steps: int, timeframe_days: int) -> List[Tuple[int, int]]:
    """
    Split the available timeframe into roughly even day ranges for each step.

    Example:
      num_steps = 5, timeframe_days = 14
      -> [(1, 3), (4, 6), (7, 9), (10, 12), (13, 14)]
    """

    if num_steps <= 0:
        return []
    
    days = max(timeframe_days, 1)

    base_chunk = days // num_steps
    remainder = days % num_steps

    ranges: List[Tuple[int, int]] = []
    current_start = 1

    for i in range(num_steps):
        length = base_chunk + (1 if i < remainder else 0)

        if length <= 0:
            if ranges:
                start = ranges[-1][1]
            else:
                start = 1
            end = start
        else:
            start = current_start
            end = start + length - 1
            current_start = end + 1

        ranges.append((start, end))
    
    return ranges


def plan_from_goal(payload: GoalInput) -> PlanResponse:
    """
    Turn a high-level goal into a simple, structured, rule-based plan.

    - Classifies the goal into a coarse category.
    - Chooses a step template for that category.
    - Distributes steps across the given timeframe in days.
    """

    category = classify_goal_text(payload.goal)
    template = STEP_TEMPLATES.get(category, STEP_TEMPLATES["generic"])

    num_steps = len(template)
    timeframe = payload.timeframe_days if payload.timeframe_days and payload.timeframe_days > 0 else num_steps

    day_ranges = compute_step_day_ranges(num_steps=num_steps, timeframe_days=timeframe)

    steps: List[PlanStep] = []

    for idx, ((title, base_description), (start_day, end_day)) in enumerate(zip(template, day_ranges),start=1,):

        if start_day == end_day:
            day_prefix = f"Day {start_day}: "
        else:
            day_prefix = f"Days {start_day}-{end_day}: "
        
        description = day_prefix + base_description

        depends_on_ids: List[int] = [idx - 1] if idx > 1 else []

        steps.append(
            PlanStep(
                id=idx,
                title=title,
                description=description,
                depends_on=depends_on_ids,
            )
        )
    
    planner_notes_parts: List[str] = [
        f"Rule-based plan categorized as '{category}' over {timeframe} day(s)."
    ]

    if payload.notes:
        planner_notes_parts.append(f"User notes/constraints: {payload.notes}")

    planner_notes = " ".join(planner_notes_parts)

    return PlanResponse(
        goal=payload.goal,
        steps=steps,
        notes=planner_notes,
    )
