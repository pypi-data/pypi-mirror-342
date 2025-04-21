from typing import Callable, Dict, Any
import logging

logger = logging.getLogger("codepy.evts")

class Eventos:
    def __init__(self):
        self._evts: Dict[str, Callable] = {}

    def registrar(self, nome: str, cb: Callable):
        """Registra um evento."""
        self._evts[nome] = cb

    async def disparar(self, nome: str, *args, **kwargs):
        """Dispara um evento."""
        if nome in self._evts:
            try:
                await self._evts[nome](*args, **kwargs)
            except Exception as e:
                logger.error(f"Erro ao disparar evento {nome}: {str(e)}")