# AI INTERVIEW PLATFORM – SYSTEM CONTRACT v2.0

This document defines the COMPLETE architecture, structure, interfaces,
schemas, state machine, backend logic rules, frontend integration rules,
and code-generation constraints.

ALL CODE MUST FOLLOW THIS DOCUMENT STRICTLY.

No redesign allowed.
No structure modification allowed.
No renaming allowed.

------------------------------------------------------------
1. SYSTEM OVERVIEW
------------------------------------------------------------

We are building an Agentic AI Mock Interview Platform that:

- Parses resume and job description
- Generates interview plan
- Conducts adaptive multi-round interview
- Dynamically probes weak answers
- Produces structured evaluation report
- Uses deterministic orchestration
- Uses Local LLM (Qwen 14B 4q_k_m via llama-cpp)

LLM = reasoning engine only
Orchestrator = deterministic control layer

------------------------------------------------------------
2. TECH STACK (MANDATORY)
------------------------------------------------------------

Backend:
- Python 3.11+
- FastAPI
- Pydantic
- llama-cpp-python
- Structured logging

Frontend:
- HTML
- CSS
- Vanilla JavaScript (ES Modules)
- Fetch API

Model Storage:
models_store/qwen/qwen-14b-4q_k_m.gguf

------------------------------------------------------------
3. FINAL FOLDER STRUCTURE (FROZEN)
------------------------------------------------------------

ai-interview-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
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
├── frontend/
│   ├── index.html
│   ├── interview.html
│   ├── report.html
│   │
│   ├── css/
│   │   ├── styles.css
│   │   ├── interview.css
│   │   └── report.css
│   │
│   ├── js/
│   │   ├── api.js
│   │   ├── interview.js
│   │   ├── report.js
│   │   └── utils.js
│   │
│   └── config.js
│
└── models_store/
    └── qwen/
        └── qwen-14b-4q_k_m.gguf

NO FILES MAY BE ADDED OR REMOVED WITHOUT VERSION UPDATE.

------------------------------------------------------------
4. STATE MACHINE (MANDATORY)
------------------------------------------------------------

InterviewState enum:

- initialized
- planned
- question_asked
- answer_received
- evaluated
- probing
- completed
- terminated

Only orchestrator may change state.
Agents must not change state.

------------------------------------------------------------
5. ORCHESTRATOR CONTRACT
------------------------------------------------------------

Class: InterviewOrchestrator

Public methods:

- start_interview(resume: str, job_description: str) -> Dict
- submit_answer(session_id: str, answer: str) -> Dict
- end_interview(session_id: str) -> Dict

Responsibilities:

- Enforce valid state transitions
- Call planner, conductor, evaluator, reporter
- Store structured session data
- Handle probing logic
- Never call LLM directly
- Never contain prompt text

------------------------------------------------------------
6. AGENT INTERFACES (STRICT)
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
- Must not access database
- Must not change session state
- Must not call API layer

------------------------------------------------------------
7. EVALUATION SCHEMA (STRICT)
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

Backend must validate schema before using output.

------------------------------------------------------------
8. REPORT SCHEMA (STRICT)
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
9. SESSION STRUCTURE
------------------------------------------------------------

Session object:

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
10. LLM RULES
------------------------------------------------------------

- Prompts stored only in /prompts
- No hardcoded prompts
- Temperature <= 0.4
- Structured JSON output required
- Outputs validated before use
- No free-form text allowed

------------------------------------------------------------
11. API CONTRACT (FIXED)
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

------------------------------------------------------------
12. FRONTEND RULES
------------------------------------------------------------

- Must use Fetch API
- Must call backend only via api.js
- No business logic in HTML
- No evaluation logic in frontend
- Charts rendered using structured JSON from backend
- Session ID stored in JS memory

------------------------------------------------------------
13. CODING RULES
------------------------------------------------------------

- Strict typing in backend
- Pydantic for all schemas
- Dependency injection pattern
- No circular imports
- Logging enabled
- Deterministic control flow
- No global mutable state
- No direct LLM calls outside model layer

------------------------------------------------------------
14. CODE GENERATION INSTRUCTIONS
------------------------------------------------------------

When generating any file:

- Follow this contract strictly
- Do not redesign architecture
- Do not rename classes
- Do not change method signatures
- Do not change folder structure
- Validate schemas strictly
- Respect separation of concerns

------------------------------------------------------------
END OF SYSTEM CONTRACT v2.0
------------------------------------------------------------