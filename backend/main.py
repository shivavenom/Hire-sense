from fastapi import FastAPI
from app.core.dependency_container import build_orchestrator
from app.api.routes_interview import get_interview_router
from app.api.routes_session import get_session_router

app = FastAPI()

orchestrator = build_orchestrator()

app.include_router(get_interview_router(orchestrator))
app.include_router(get_session_router(orchestrator))