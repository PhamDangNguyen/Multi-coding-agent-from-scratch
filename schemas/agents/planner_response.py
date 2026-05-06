from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class PlannerResponse(BaseModel):
    Response: List[Dict[str, str]]