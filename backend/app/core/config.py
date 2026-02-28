from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration.
    Loaded from environment variables or defaults.
    """

    # Absolute resolved path to model
    model_path: str = str(
        Path(__file__).resolve().parents[2] /
        "models_store/qwen/qwen-7b-4q_k_m.gguf"
    )

    temperature: float = 0.3
    max_tokens: int = 1024
    context_size: int = 4096

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()