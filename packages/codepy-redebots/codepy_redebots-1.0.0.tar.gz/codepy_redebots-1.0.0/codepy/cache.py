from typing import Any, Dict, Optional
import redis
import pickle
import logging

logger = logging.getLogger("codepy.cache")

class Cache:
    def __init__(self, config: Dict):
        self._mem: Dict[str, Any] = {}
        self._redis = None
        if config.get("redis_url"):
            try:
                self._redis = redis.Redis.from_url(config["redis_url"])
            except redis.RedisError as e:
                logger.error(f"Erro ao conectar ao Redis: {str(e)}")

    def set(self, chave: str, valor: Any, ttl: Optional[int] = None):
        """Salva um valor no cache."""
        try:
            serialized = pickle.dumps(valor)
            if self._redis:
                try:
                    self._redis.set(chave, serialized, ex=ttl)
                except redis.RedisError:
                    self._mem[chave] = valor
            else:
                self._mem[chave] = valor
        except Exception as e:
            logger.error(f"Erro ao salvar no cache: {str(e)}")

    def get(self, chave: str) -> Any:
        """Recupera um valor do cache."""
        try:
            if self._redis:
                valor = self._redis.get(chave)
                return pickle.loads(valor) if valor else None
            return self._mem.get(chave)
        except Exception as e:
            logger.error(f"Erro ao recuperar do cache: {str(e)}")
            return None