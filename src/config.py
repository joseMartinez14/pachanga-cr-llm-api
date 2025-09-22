from pydantic import BaseModel
import os

class Settings(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    upstash_redis_url: str = os.getenv("UPSTASH_REDIS_URL", "")
    upstash_redis_token: str = os.getenv("UPSTASH_REDIS_TOKEN", "")
    api_bearer: str | None = os.getenv("API_BEARER_TOKEN")
    default_locale: str = os.getenv("DEFAULT_LOCALE", "es-CR")

settings = Settings()