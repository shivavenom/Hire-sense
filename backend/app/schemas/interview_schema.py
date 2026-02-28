from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime


class SessionSchema(BaseModel):
    session_id: str
    state: str
    plan: Dict[str, Any] | None = None
    questions: List[str] = Field(default_factory=list)
    answers: List[str] = Field(default_factory=list)
    evaluations: List[Dict[str, Any]] = Field(default_factory=list)
    current_question: str | None = None
    created_at: datetime