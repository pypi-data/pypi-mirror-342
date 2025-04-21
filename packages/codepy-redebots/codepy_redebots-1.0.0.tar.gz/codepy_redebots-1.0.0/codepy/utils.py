from functools import wraps
import logging

logger = logging.getLogger("codepy.utils")

def abrev(func):
    """Decorador para abreviações."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Chamando {func.__name__} com args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper