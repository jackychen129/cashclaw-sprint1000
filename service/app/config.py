from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    port: int = int(os.getenv("PORT", "8080"))

    local_model_base_url: str = os.getenv("LOCAL_MODEL_BASE_URL", "http://localhost:11434/v1")
    local_model_name: str = os.getenv("LOCAL_MODEL_NAME", "llama3.1")
    local_model_api_key: str = os.getenv("LOCAL_MODEL_API_KEY", "local-not-required")

    online_model_base_url: str = os.getenv("ONLINE_MODEL_BASE_URL", "https://api.openai.com/v1")
    online_model_name: str = os.getenv("ONLINE_MODEL_NAME", "gpt-4o-mini")
    online_model_api_key: str = os.getenv("ONLINE_MODEL_API_KEY", "")

    model_routing_policy: str = os.getenv("MODEL_ROUTING_POLICY", "quality_first")


settings = Settings()
