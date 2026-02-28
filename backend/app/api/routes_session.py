from fastapi import APIRouter
from typing import Dict

from app.core.orchestrator import InterviewOrchestrator


def get_session_router(orchestrator: InterviewOrchestrator) -> APIRouter:
    """
    Session-related routes.
    """

    router = APIRouter(prefix="/session", tags=["Session"])

    @router.get("/{session_id}")
    def get_session(session_id: str) -> Dict:
        session = orchestrator.session_store.get_session(session_id)

        if not session:
            return {"error": "Session not found"}

        return session

    return router