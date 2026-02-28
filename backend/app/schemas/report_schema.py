from pydantic import BaseModel
from typing import List


class ReportSchema(BaseModel):
    overall_score: float
    technical_summary: str
    communication_summary: str
    strengths: List[str]
    areas_for_improvement: List[str]
    recommendations: List[str]