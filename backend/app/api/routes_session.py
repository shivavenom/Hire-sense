from fastapi import APIRouter, HTTPException
from typing import Dict

from app.core.dependency_container import build_orchestrator


router = APIRouter()
orchestrator = build_orchestrator()


@router.get("/session/{session_id}")
def get_session(session_id: str) -> Dict:
    session = orchestrator.session_store.get_session(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session