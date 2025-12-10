from fastapi import APIRouter

from app.schemas.planning import GoalInput, PlanResponse
from app.services.planner import plan_from_goal

router = APIRouter(
    prefix="/plan",
    tags=["planning"],
)

@router.post("", response_model=PlanResponse)
async def create_plan(payload: GoalInput) -> PlanResponse:
    return plan_from_goal(payload)
