from typing import Dict, Any


class SessionStore:
    """
    In-memory session store.
    Production version should use Redis or DB.
    """

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    # ==========================
    # CREATE
    # ==========================

    def create_session(self, session_id: str, state: str):
        self._sessions[session_id] = {
            "state": state,
            "plan": None,
            "questions": [],
            "current_question": None,
            "answers": [],
            "evaluations": [],
        }

    # ==========================
    # GET
    # ==========================

    def get_session(self, session_id: str) -> Dict[str, Any]:
        return self._sessions.get(session_id)

    # ==========================
    # UPDATE STATE
    # ==========================

    def update_state(self, session_id: str, state: str):
        if session_id in self._sessions:
            self._sessions[session_id]["state"] = state

    # ==========================
    # GENERIC UPDATE
    # ==========================

    def update_session(self, session_id: str, data: Dict[str, Any]):
        if session_id in self._sessions:
            self._sessions[session_id].update(data)

    # ==========================
    # PLAN
    # ==========================

    def store_plan(self, session_id: str, plan: Dict[str, Any]):
        if session_id in self._sessions:
            self._sessions[session_id]["plan"] = plan

    # ==========================
    # QUESTIONS
    # ==========================

    def store_question(self, session_id: str, question: str):
        if session_id in self._sessions:
            self._sessions[session_id]["current_question"] = question
            self._sessions[session_id]["questions"].append(question)

    # ==========================
    # ANSWERS
    # ==========================

    def append_answer(self, session_id: str, answer: str):
        if session_id in self._sessions:
            self._sessions[session_id]["answers"].append(answer)

    # ==========================
    # EVALUATION
    # ==========================

    def store_evaluation(self, session_id: str, evaluation: Dict[str, Any]):
        if session_id in self._sessions:
            self._sessions[session_id]["evaluations"].append(evaluation)