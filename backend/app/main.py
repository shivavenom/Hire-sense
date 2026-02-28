from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.dependency_container import build_orchestrator
from app.utils.logger import configure_logging, get_logger


# ==========================================================
# Configure Logging
# ==========================================================

configure_logging()
logger = get_logger(__name__)


# ==========================================================
# Application Initialization
# ==========================================================

app = FastAPI(
    title="AI Interview Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ==========================================================
# CORS Configuration
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# Dependency Injection
# ==========================================================

try:
    logger.info("Building orchestrator instance...")
    orchestrator = build_orchestrator()
    logger.info("Orchestrator initialized successfully.")
except Exception as e:
    logger.error(f"Failed to build orchestrator: {str(e)}")
    raise


# ==========================================================
# Router Registration (Fail Fast)
# ==========================================================

try:
    from app.api.routes_interview import get_interview_router
    from app.api.routes_session import get_session_router

    app.include_router(get_interview_router(orchestrator))
    logger.info("Interview router registered.")

    app.include_router(get_session_router(orchestrator))
    logger.info("Session router registered.")

except ImportError as e:
    logger.critical(f"Router import failed: {str(e)}")
    raise

except Exception as e:
    logger.critical(f"Router registration failed: {str(e)}")
    raise


# ==========================================================
# Global Exception Handler
# ==========================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
        },
    )


# ==========================================================
# Health Check
# ==========================================================

@app.get("/")
def root():
    return {
        "status": "AI Interview Platform Running",
        "version": "1.0.0",
    }