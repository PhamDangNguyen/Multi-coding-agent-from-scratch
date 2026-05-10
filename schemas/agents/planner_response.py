from typing import List
from pydantic import BaseModel


class PlannerTask(BaseModel):
    id : str
    agent: str
    task: str
    depends_on: List[str]
    recommended_skills: List[str]


class PlannerResponse(BaseModel):
    Response: List[PlannerTask]