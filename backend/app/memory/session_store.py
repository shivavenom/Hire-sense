from typing import Dict, Any
from datetime import datetime
from app.schemas.interview_schema import SessionSchema


class SessionStore:

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, session_id: str, state: str):
        session = SessionSchema(
            session_id=session_id,
            state=state,
            created_at=datetime.utcnow(),
        )
        self._sessions[session_id] = session.model_dump()

    def get_session(self, session_id: str):
        return self._sessions.get(session_id)

    def update_state(self, session_id: str, state: str):
        self._sessions[session_id]["state"] = state

    def store_plan(self, session_id: str, plan: Dict[str, Any]):
        self._sessions[session_id]["plan"] = plan

    def store_question(self, session_id: str, question: str):
        self._sessions[session_id]["questions"].append(question)
        self._sessions[session_id]["current_question"] = question

    def append_answer(self, session_id: str, answer: str):
        self._sessions[session_id]["answers"].append(answer)

    def store_evaluation(self, session_id: str, evaluation: Dict[str, Any]):
        self._sessions[session_id]["evaluations"].append(evaluation)