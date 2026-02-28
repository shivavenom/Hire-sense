from typing import Dict, Any, Optional
from datetime import datetime

from app.schemas.interview_schema import SessionSchema


class SessionStore:
    """
    In-memory session storage.

    Responsibilities:
    - Create sessions
    - Store and retrieve session data
    - No business logic
    - No state machine logic
    - No validation logic (handled elsewhere)
    """

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    # --------------------------------------
    # Session Lifecycle
    # --------------------------------------

    def create_session(self, session_id: str, state: str) -> None:
        session = SessionSchema(
            session_id=session_id,
            state=state,
            created_at=datetime.utcnow(),
        )

        self._sessions[session_id] = session.model_dump()

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._sessions.get(session_id)

    def update_state(self, session_id: str, state: str) -> None:
        self._require_session(session_id)
        self._sessions[session_id]["state"] = state

    # --------------------------------------
    # Data Storage Methods
    # --------------------------------------

    def store_plan(self, session_id: str, plan: Dict[str, Any]) -> None:
        self._require_session(session_id)
        self._sessions[session_id]["plan"] = plan

    def store_question(self, session_id: str, question: str) -> None:
        self._require_session(session_id)
        self._sessions[session_id]["questions"].append(question)
        self._sessions[session_id]["current_question"] = question

    def append_answer(self, session_id: str, answer: str) -> None:
        self._require_session(session_id)
        self._sessions[session_id]["answers"].append(answer)

    def store_evaluation(self, session_id: str, evaluation: Dict[str, Any]) -> None:
        self._require_session(session_id)
        self._sessions[session_id]["evaluations"].append(evaluation)

    # --------------------------------------
    # Internal Safety
    # --------------------------------------

    def _require_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

    # --------------------------------------
    # Utility
    # --------------------------------------

    def delete_session(self, session_id: str) -> None:
        self._require_session(session_id)
        del self._sessions[session_id]

    def list_sessions(self) -> Dict[str, Dict[str, Any]]:
        return self._sessions