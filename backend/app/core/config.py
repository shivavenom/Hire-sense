from pydantic import BaseSettings


class Settings(BaseSettings):
    model_path: str = "models_store/qwen/qwen-14b-4q_k_m.gguf"
    temperature: float = 0.3
    max_tokens: int = 1024

    class Config:
        env_file = ".env"


settings = Settings()