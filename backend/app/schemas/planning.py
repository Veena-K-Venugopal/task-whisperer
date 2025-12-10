from typing import Optional, List

from pydantic import BaseModel

class GoalInput(BaseModel):
    goal: str
    timeframe_days: Optional[int] = None
    notes: Optional[str] = None


class PlanStep(BaseModel):
    id: int
    title: str
    description: str
    depends_on: Optional[List[int]] = None


class PlanResponse(BaseModel):
    goal: str
    steps: List[PlanStep]
    notes: Optional[str] = None

