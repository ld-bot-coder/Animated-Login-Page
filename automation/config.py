import os
import logging
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    """Single source of truth for configuration"""
    
    # APP
    APP_ENV = os.getenv("APP_ENV", "production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY")

    # LLM
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-oss:120b")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://api.ollama.com")
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

    # SEARCH
    OXYLABS_USERNAME = os.getenv("OXYLABS_USERNAME")
    OXYLABS_PASSWORD = os.getenv("OXYLABS_PASSWORD")
    OXYLABS_ENDPOINT = os.getenv("OXYLABS_ENDPOINT", "https://realtime.oxylabs.io/v1/queries")

    # DATA & QUEUE
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ai_search_engine")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # CELERY
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", 8))

    @classmethod
    def validate(cls):
        """Ensure critical config exists at startup"""
        missing = []
        if not cls.OLLAMA_API_KEY:
            missing.append("OLLAMA_API_KEY")
        if not cls.OXYLABS_USERNAME:
            missing.append("OXYLABS_USERNAME")
        if not cls.OXYLABS_PASSWORD:
            missing.append("OXYLABS_PASSWORD")
        
        if missing:
            logging.error(f"Missing critical configuration: {', '.join(missing)}")
            # In production, we might want to raise an error, but for dev setup we log error
            if cls.APP_ENV == "production":
                raise ValueError(f"Missing configuration: {missing}")

# Validate on import/startup
# Config.validate()
