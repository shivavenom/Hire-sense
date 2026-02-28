import uuid
import logging
from enum import Enum
from typing import Dict, Any, Optional

from app.memory.session_store import SessionStore
from app.agents.planner_agent import PlannerAgent
from app.agents.conductor_agent import ConductorAgent
from app.agents.evaluator_agent import EvaluatorAgent
from app.agents.report_agent import ReportAgent
from app.engines.probing_engine import ProbingEngine


logger = logging.getLogger(__name__)


# -----------------------------
# Interview State Machine
# -----------------------------

class InterviewState(str, Enum):
    INITIALIZED = "initialized"
    PLANNED = "planned"
    QUESTION_ASKED = "question_asked"
    ANSWER_RECEIVED = "answer_received"
    EVALUATED = "evaluated"
    PROBING = "probing"
    COMPLETED = "completed"
    TERMINATED = "terminated"


# -----------------------------
# Orchestrator
# -----------------------------

class InterviewOrchestrator:
    """
    Production-grade orchestration engine.

    Responsibilities:
    - Control interview state transitions
    - Coordinate agents
    - Enforce deterministic flow
    - Validate lifecycle correctness
    - Handle failures safely
    """

    def __init__(
        self,
        session_store: SessionStore,
        planner: PlannerAgent,
        conductor: ConductorAgent,
        evaluator: EvaluatorAgent,
        reporter: ReportAgent,
        probing_engine: ProbingEngine,
    ):
        self.session_store = session_store
        self.planner = planner
        self.conductor = conductor
        self.evaluator = evaluator
        self.reporter = reporter
        self.probing_engine = probing_engine

    # ======================================
    # PUBLIC API
    # ======================================

    def start_interview(self, resume: str, job_description: str) -> Dict[str, Any]:
        session_id = str(uuid.uuid4())

        logger.info(f"[START] Creating interview session {session_id}")

        self.session_store.create_session(
            session_id=session_id,
            state=InterviewState.INITIALIZED.value,
        )

        plan = self._generate_plan(session_id, resume, job_description)

        first_question = self._ask_next_question(session_id)

        return {
            "session_id": session_id,
            "state": InterviewState.QUESTION_ASKED.value,
            "question": first_question,
        }

    def submit_answer(self, session_id: str, answer: str) -> Dict[str, Any]:
        session = self._require_session(session_id)

        self._ensure_state(
            session,
            allowed=[InterviewState.QUESTION_ASKED.value, InterviewState.PROBING.value],
        )

        logger.info(f"[ANSWER] Session {session_id}")

        self.session_store.append_answer(session_id, answer)
        self.session_store.update_state(session_id, InterviewState.ANSWER_RECEIVED.value)

        evaluation = self._evaluate_answer(session_id)

        probe = self.probing_engine.should_probe(evaluation)

        if probe:
            next_question = self._generate_followup(session_id, evaluation)
            next_state = InterviewState.PROBING.value
        else:
            next_question = self._ask_next_question(session_id)
            next_state = InterviewState.QUESTION_ASKED.value

        self.session_store.update_state(session_id, next_state)

        return {
            "evaluation": evaluation,
            "next_question": next_question,
            "state": next_state,
        }

    def end_interview(self, session_id: str) -> Dict[str, Any]:
        session = self._require_session(session_id)

        logger.info(f"[END] Session {session_id}")

        report = self.reporter.generate_report(session)

        self.session_store.update_state(session_id, InterviewState.COMPLETED.value)

        return {
            "state": InterviewState.COMPLETED.value,
            "report": report,
        }

    # ======================================
    # INTERNAL CONTROL METHODS
    # ======================================

    def _generate_plan(self, session_id: str, resume: str, jd: str) -> Dict[str, Any]:
        logger.info(f"[PLAN] Generating interview plan for {session_id}")

        plan = self.planner.create_plan(resume, jd)

        self.session_store.store_plan(session_id, plan)
        self.session_store.update_state(session_id, InterviewState.PLANNED.value)

        return plan

    def _ask_next_question(self, session_id: str) -> str:
        session = self._require_session(session_id)

        question = self.conductor.generate_question(session)

        self.session_store.store_question(session_id, question)
        self.session_store.update_state(session_id, InterviewState.QUESTION_ASKED.value)

        return question

    def _generate_followup(self, session_id: str, evaluation: Dict[str, Any]) -> str:
        session = self._require_session(session_id)

        question = self.conductor.generate_followup(session, evaluation)

        self.session_store.store_question(session_id, question)

        return question

    def _evaluate_answer(self, session_id: str) -> Dict[str, Any]:
        session = self._require_session(session_id)

        question = session["current_question"]
        answer = session["answers"][-1]

        evaluation = self.evaluator.evaluate(question, answer, session["plan"])

        self.session_store.store_evaluation(session_id, evaluation)
        self.session_store.update_state(session_id, InterviewState.EVALUATED.value)

        return evaluation

    # ======================================
    # GUARD & VALIDATION LAYER
    # ======================================

    def _require_session(self, session_id: str) -> Dict[str, Any]:
        session = self.session_store.get_session(session_id)

        if not session:
            logger.error(f"Invalid session_id: {session_id}")
            raise ValueError("Session does not exist")

        return session

    def _ensure_state(self, session: Dict[str, Any], allowed: list):
        if session["state"] not in allowed:
            raise RuntimeError(
                f"Invalid state transition. Current: {session['state']}, Allowed: {allowed}"
            )