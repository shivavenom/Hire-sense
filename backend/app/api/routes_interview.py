from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

from app.core.orchestrator import InterviewOrchestrator


def get_interview_router(orchestrator: InterviewOrchestrator) -> APIRouter:
    router = APIRouter()

    class StartRequest(BaseModel):
        resume: str
        job_description: str

    class AnswerRequest(BaseModel):
        session_id: str
        answer: str

    class EndRequest(BaseModel):
        session_id: str

    @router.post("/start")
    def start_interview(request: StartRequest) -> Dict:
        return orchestrator.start_interview(
            resume=request.resume,
            job_description=request.job_description,
        )

    @router.post("/answer")
    def submit_answer(request: AnswerRequest) -> Dict:
        return orchestrator.submit_answer(
            session_id=request.session_id,
            answer=request.answer,
        )

    @router.post("/end")
    def end_interview(request: EndRequest) -> Dict:
        return orchestrator.end_interview(
            session_id=request.session_id,
        )

    return router