# AI INTERVIEW PLATFORM – SYSTEM CONTRACT (v1.0)

This document defines the authoritative architecture, structure, interfaces,
state machine, and coding standards for the Agentic AI Mock Interview Platform.

This contract must NOT be modified unless the team agrees to a version upgrade.

All generated code must strictly follow this document.

------------------------------------------------------------
1. SYSTEM GOAL
------------------------------------------------------------

Build an agentic AI-powered mock interview system that:

- Parses resume and job description
- Creates a structured interview plan
- Conducts adaptive interview rounds
- Probes weak answers dynamically
- Produces structured evaluation reports
- Maintains session memory
- Operates with deterministic orchestration control

LLM = reasoning engine only
Backend = deterministic control layer

------------------------------------------------------------
2. TECH STACK
------------------------------------------------------------

Backend:
- Python 3.11+
- FastAPI
- Pydantic
- Local LLM (Qwen 14B 4q_k_m GGUF via llama-cpp)

Frontend:
- React
- API-based communication only

Model storage:
- models_store/qwen/qwen-14b-4q_k_m.gguf

------------------------------------------------------------
3. FOLDER STRUCTURE (FINAL AND FROZEN)
------------------------------------------------------------

ai-interview-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── orchestrator.py
│   │   │   ├── config.py
│   │   │   └── dependency_container.py
│   │   │
│   │   ├── agents/
│   │   │   ├── planner_agent.py
│   │   │   ├── conductor_agent.py
│   │   │   ├── evaluator_agent.py
│   │   │   └── report_agent.py
│   │   │
│   │   ├── engines/
│   │   │   ├── probing_engine.py
│   │   │   └── scoring_engine.py
│   │   │
│   │   ├── memory/
│   │   │   ├── session_store.py
│   │   │   └── resume_parser.py
│   │   │
│   │   ├── models/
│   │   │   ├── model_manager.py
│   │   │   └── qwen_loader.py
│   │   │
│   │   ├── prompts/
│   │   │   ├── planner.txt
│   │   │   ├── evaluator.txt
│   │   │   ├── followup.txt
│   │   │   └── report.txt
│   │   │
│   │   ├── schemas/
│   │   │   ├── interview_schema.py
│   │   │   ├── evaluation_schema.py
│   │   │   └── report_schema.py
│   │   │
│   │   └── api/
│   │       ├── routes_interview.py
│   │       └── routes_session.py
│   │
│   └── requirements.txt
│
└── models_store/
    └── qwen/
        └── qwen-14b-4q_k_m.gguf

This structure must NOT be changed.

------------------------------------------------------------
4. STATE MACHINE (MANDATORY)
------------------------------------------------------------

InterviewState:

- initialized
- planned
- question_asked
- answer_received
- evaluated
- probing
- completed
- terminated

State transitions must be deterministic.
No agent may change state directly.
Only orchestrator controls state.

------------------------------------------------------------
5. ORCHESTRATOR RULES
------------------------------------------------------------

The orchestrator:

- Controls full lifecycle
- Validates state transitions
- Calls agents
- Stores structured data
- Never contains prompts
- Never directly calls LLM
- Never contains business randomness

It must expose:

- start_interview()
- submit_answer()
- end_interview()

------------------------------------------------------------
6. AGENT CONTRACTS
------------------------------------------------------------

PlannerAgent:
    create_plan(resume: str, job_description: str) -> Dict

ConductorAgent:
    generate_question(session: Dict) -> str
    generate_followup(session: Dict, evaluation: Dict) -> str

EvaluatorAgent:
    evaluate(question: str, answer: str, plan: Dict) -> Dict

ReportAgent:
    generate_report(session: Dict) -> Dict

Agents:
- Must return structured JSON
- Must not write to database
- Must not change session state
- Must not access API layer

------------------------------------------------------------
7. EVALUATION SCHEMA (MANDATORY OUTPUT FORMAT)
------------------------------------------------------------

{
  "technical_depth": int (0-10),
  "accuracy": int (0-10),
  "clarity": int (0-10),
  "confidence": int (0-10),
  "strengths": list[str],
  "weaknesses": list[str],
  "missing_concepts": list[str],
  "follow_up_required": bool
}

If structure deviates → reject output.

------------------------------------------------------------
8. REPORT SCHEMA
------------------------------------------------------------

{
  "overall_score": float,
  "technical_summary": str,
  "communication_summary": str,
  "strengths": list[str],
  "areas_for_improvement": list[str],
  "recommendations": list[str]
}

------------------------------------------------------------
9. SESSION STORE STRUCTURE
------------------------------------------------------------

Session object must contain:

{
  "session_id": str,
  "state": str,
  "plan": Dict,
  "questions": list[str],
  "answers": list[str],
  "evaluations": list[Dict],
  "current_question": str,
  "created_at": timestamp
}

------------------------------------------------------------
10. LLM INTERACTION RULES
------------------------------------------------------------

- All prompts stored in /prompts
- Prompts never hardcoded
- LLM must return JSON only
- Temperature <= 0.4
- Max tokens controlled
- Outputs validated before use

------------------------------------------------------------
11. API CONTRACT
------------------------------------------------------------

POST /start
Input:
{
  "resume": str,
  "job_description": str
}

POST /answer
{
  "session_id": str,
  "answer": str
}

POST /end
{
  "session_id": str
}

Backend returns JSON only.
Frontend handles UI and charts.

------------------------------------------------------------
12. CODING RULES
------------------------------------------------------------

- Use dependency injection
- No circular imports
- No global state
- No LLM calls in API routes
- All schemas use Pydantic
- Logging enabled
- Error handling explicit
- Strict typing required

------------------------------------------------------------
13. EXTENSIBILITY RULE
------------------------------------------------------------

New features must:
- Not break orchestrator
- Not modify evaluation schema
- Be additive only

------------------------------------------------------------
END OF CONTRACT
------------------------------------------------------------

When generating code, strictly follow this contract.
Do not redesign architecture.
Do not change folder structure.
Do not modify schemas.