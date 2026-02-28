@echo off
echo Creating AI Interview Backend Structure...

:: Root Backend
mkdir backend
cd backend

mkdir app
cd app

:: Core
mkdir core
mkdir agents
mkdir engines
mkdir memory
mkdir models
mkdir prompts
mkdir schemas
mkdir api
mkdir utils

:: Create Python files inside app

cd core
type nul > config.py
type nul > orchestrator.py
type nul > session_manager.py
type nul > dependency_container.py
cd ..

cd agents
type nul > planner_agent.py
type nul > conductor_agent.py
type nul > evaluator_agent.py
type nul > report_agent.py
cd ..

cd engines
type nul > question_engine.py
type nul > comparison_engine.py
type nul > scoring_engine.py
type nul > probing_engine.py
cd ..

cd memory
type nul > session_store.py
type nul > resume_parser.py
type nul > ideal_answer_store.py
cd ..

cd models
type nul > model_manager.py
type nul > qwen_loader.py
type nul > prompt_router.py
cd ..

cd prompts
type nul > planner.txt
type nul > evaluator.txt
type nul > followup.txt
type nul > report.txt
cd ..

cd schemas
type nul > interview_schema.py
type nul > evaluation_schema.py
type nul > report_schema.py
cd ..

cd api
type nul > routes_interview.py
type nul > routes_session.py
cd ..

cd utils
type nul > logger.py
type nul > helpers.py
cd ..

:: Create main.py
cd ..
type nul > main.py

:: Go back to backend root
cd ..

:: Data folders
mkdir data
cd data
mkdir sessions
mkdir resumes
mkdir reports
cd ..

:: Tests and requirements
mkdir tests
type nul > requirements.txt

cd ..

:: Model storage outside backend
mkdir models_store
cd models_store
mkdir qwen
cd ..

echo Backend structure created successfully!
pause