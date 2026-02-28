from typing import Dict, Any, Optional
from datetime import datetime


class SessionStore:
    """
    In-memory session store.

    Responsibilities:
    - Maintain deterministic session state
    - Prevent KeyErrors
    - Guarantee required fields exist
    - Safe lifecycle management
    """

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    # ==========================================================
    # SESSION LIFECYCLE
    # ==========================================================

    def create_session(self, session_id: str, state: str) -> None:
        """
        Create a new interview session with fully initialized structure.
        """

        if session_id in self._sessions:
            raise ValueError("Session already exists")

        self._sessions[session_id] = {
            "session_id": session_id,
            "state": state,
            "created_at": datetime.utcnow(),
            "plan": None,
            "questions": [],
            "answers": [],
            "evaluations": [],
            "current_question": None,
        }

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._sessions.get(session_id)

    def update_state(self, session_id: str, state: str) -> None:
        self._require_session(session_id)
        self._sessions[session_id]["state"] = state

    # ==========================================================
    # PLAN MANAGEMENT
    # ==========================================================

    def store_plan(self, session_id: str, plan: Dict[str, Any]) -> None:
        self._require_session(session_id)
        self._sessions[session_id]["plan"] = plan

    # ==========================================================
    # QUESTION MANAGEMENT
    # ==========================================================

    def store_question(self, session_id: str, question: str) -> None:
        self._require_session(session_id)

        if not question:
            raise ValueError("Question cannot be empty")

        self._sessions[session_id]["questions"].append(question)
        self._sessions[session_id]["current_question"] = question

    # ==========================================================
    # ANSWER MANAGEMENT
    # ==========================================================

    def append_answer(self, session_id: str, answer: str) -> None:
        self._require_session(session_id)

        if not answer:
            raise ValueError("Answer cannot be empty")

        self._sessions[session_id]["answers"].append(answer)

    # ==========================================================
    # EVALUATION MANAGEMENT
    # ==========================================================

    def store_evaluation(self, session_id: str, evaluation: Dict[str, Any]) -> None:
        self._require_session(session_id)

        if not isinstance(evaluation, dict):
            raise ValueError("Evaluation must be a dictionary")

        self._sessions[session_id]["evaluations"].append(evaluation)

    # ==========================================================
    # INTERNAL GUARD
    # ==========================================================

    def _require_session(self, session_id: str) -> None:
        if session_id not in self._sessions:
            raise ValueError("Session does not exist")