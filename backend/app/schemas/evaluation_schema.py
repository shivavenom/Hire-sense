from pydantic import BaseModel, conint
from typing import List


class EvaluationSchema(BaseModel):
    technical_depth: conint(ge=0, le=10)
    accuracy: conint(ge=0, le=10)
    clarity: conint(ge=0, le=10)
    confidence: conint(ge=0, le=10)
    strengths: List[str]
    weaknesses: List[str]
    missing_concepts: List[str]
    follow_up_required: bool