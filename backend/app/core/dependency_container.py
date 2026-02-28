from app.memory.session_store import SessionStore
from app.agents.planner_agent import PlannerAgent
from app.agents.conductor_agent import ConductorAgent
from app.agents.evaluator_agent import EvaluatorAgent
from app.agents.report_agent import ReportAgent
from app.engines.probing_engine import ProbingEngine
from app.models.model_manager import ModelManager
from app.core.orchestrator import InterviewOrchestrator


def build_orchestrator() -> InterviewOrchestrator:
    model_manager = ModelManager()
    session_store = SessionStore()
    probing_engine = ProbingEngine()

    planner = PlannerAgent(model_manager)
    conductor = ConductorAgent(model_manager)
    evaluator = EvaluatorAgent(model_manager)
    reporter = ReportAgent(model_manager)

    return InterviewOrchestrator(
        session_store=session_store,
        planner=planner,
        conductor=conductor,
        evaluator=evaluator,
        reporter=reporter,
        probing_engine=probing_engine,
    )