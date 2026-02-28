import uuid
from enum import Enum
from typing import Dict, Any, List

from app.memory.session_store import SessionStore
from app.agents.planner_agent import PlannerAgent
from app.agents.conductor_agent import ConductorAgent
from app.agents.evaluator_agent import EvaluatorAgent
from app.agents.report_agent import ReportAgent
from app.engines.probing_engine import ProbingEngine
from app.utils.logger import get_logger


logger = get_logger(__name__)


# ==========================================================
# Interview State Machine
# ==========================================================

class InterviewState(str, Enum):
    INITIALIZED = "initialized"
    PLANNED = "planned"
    QUESTION_ASKED = "question_asked"
    ANSWER_RECEIVED = "answer_received"
    EVALUATED = "evaluated"
    PROBING = "probing"
    COMPLETED = "completed"
    TERMINATED = "terminated"


# ==========================================================
# Orchestrator
# ==========================================================

class InterviewOrchestrator:
    """
    Production-grade orchestration engine.

    Responsibilities:
    - Enforce deterministic state transitions
    - Coordinate agents
    - Guard lifecycle correctness
    - Never call LLM directly
    - Never contain prompt logic
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

    # ======================================================
    # PUBLIC API
    # ======================================================

    def start_interview(self, resume: str, job_description: str) -> Dict[str, Any]:
        session_id = str(uuid.uuid4())

        logger.info(f"[START] Creating session {session_id}")

        self.session_store.create_session(
            session_id=session_id,
            state=InterviewState.INITIALIZED.value,
        )

        self._generate_plan(session_id, resume, job_description)
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
            allowed=[
                InterviewState.QUESTION_ASKED.value,
                InterviewState.PROBING.value,
            ],
        )

        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty")

        logger.info(f"[ANSWER] Session {session_id}")

        self.session_store.append_answer(session_id, answer)
        self.session_store.update_state(
            session_id, InterviewState.ANSWER_RECEIVED.value
        )

        evaluation = self._evaluate_answer(session_id)

        # If probing required
        if self.probing_engine.should_probe(evaluation):
            next_question = self._generate_followup(session_id, evaluation)
            next_state = InterviewState.PROBING.value
        else:
            # Check completion before asking next
            updated_session = self._require_session(session_id)

            if self._is_interview_complete(updated_session):
                return self.end_interview(session_id)

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

        self._ensure_not_completed(session)

        logger.info(f"[END] Session {session_id}")

        report = self.reporter.generate_report(session)

        self.session_store.update_state(
            session_id, InterviewState.COMPLETED.value
        )

        return {
            "state": InterviewState.COMPLETED.value,
            "report": report,
        }

    def terminate_interview(self, session_id: str) -> Dict[str, Any]:
        self._require_session(session_id)

        self.session_store.update_state(
            session_id, InterviewState.TERMINATED.value
        )

        logger.warning(f"[TERMINATED] Session {session_id}")

        return {"state": InterviewState.TERMINATED.value}

    # ======================================================
    # INTERNAL CONTROL METHODS
    # ======================================================

    def _generate_plan(
        self, session_id: str, resume: str, jd: str
    ) -> None:
        logger.info(f"[PLAN] Generating plan for {session_id}")

        plan = self.planner.create_plan(resume, jd)

        self.session_store.store_plan(session_id, plan)
        self.session_store.update_state(
            session_id, InterviewState.PLANNED.value
        )

    def _ask_next_question(self, session_id: str) -> str:
        session = self._require_session(session_id)

        question = self.conductor.generate_question(session)

        if not question or not question.strip():
            raise RuntimeError("Generated question is invalid")

        self.session_store.store_question(session_id, question)
        self.session_store.update_state(
            session_id, InterviewState.QUESTION_ASKED.value
        )

        return question

    def _generate_followup(
        self, session_id: str, evaluation: Dict[str, Any]
    ) -> str:
        session = self._require_session(session_id)

        question = self.conductor.generate_followup(session, evaluation)

        if not question or not question.strip():
            raise RuntimeError("Generated follow-up question is invalid")

        self.session_store.store_question(session_id, question)

        return question

    def _evaluate_answer(self, session_id: str) -> Dict[str, Any]:
        session = self._require_session(session_id)

        question = session.get("current_question")
        answers = session.get("answers", [])
        plan = session.get("plan")

        if not question:
            raise RuntimeError("No active question to evaluate")

        if not answers:
            raise RuntimeError("No answers available for evaluation")

        if not plan:
            raise RuntimeError("Interview plan missing")

        answer = answers[-1]

        evaluation = self.evaluator.evaluate(question, answer, plan)
        print("EVALUATION OUTPUT:", evaluation)

        self.session_store.store_evaluation(session_id, evaluation)
        self.session_store.update_state(
            session_id, InterviewState.EVALUATED.value
        )

        return evaluation

    # ======================================================
    # VALIDATION & GUARD LAYER
    # ======================================================

    def _require_session(self, session_id: str) -> Dict[str, Any]:
        session = self.session_store.get_session(session_id)

        if not session:
            logger.error(f"Invalid session_id: {session_id}")
            raise ValueError("Session does not exist")

        return session

    def _ensure_state(self, session: Dict[str, Any], allowed: List[str]) -> None:
        if session["state"] not in allowed:
            raise RuntimeError(
                f"Invalid state transition. "
                f"Current: {session['state']}, Allowed: {allowed}"
            )

    def _ensure_not_completed(self, session: Dict[str, Any]) -> None:
        if session["state"] in [
            InterviewState.COMPLETED.value,
            InterviewState.TERMINATED.value,
        ]:
            raise RuntimeError("Interview already finished")

    def _is_interview_complete(self, session: Dict[str, Any]) -> bool:
        plan = session.get("plan", {})
        core_topics = plan.get("core_topics", [])
        asked = len(session.get("questions", []))

        if not core_topics:
            return True

        return asked >= len(core_topics)