from app.schemas.planning import GoalInput, PlanStep, PlanResponse

def plan_from_goal(payload: GoalInput) -> PlanResponse:
    """
    Turn a high-level goal into a simple, structured plan.

    For now this is a stub (no AI yet).
    Later we''ll replace with real planning logic. 
    """
    ...

    steps = []
    steps.append(PlanStep(
        id=1,
        title="Clarify your goal",
        description="Rewrite your goal in one sentence focusing on what 'done' looks like.",
    ))

    return PlanResponse(
        goal=payload.goal,
        steps=steps,
    )