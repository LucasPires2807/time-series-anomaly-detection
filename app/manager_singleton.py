from functools import lru_cache
from app.model_manager import ModelManager

@lru_cache(maxsize=1)
def get_model_manager() -> ModelManager:
    return ModelManager()