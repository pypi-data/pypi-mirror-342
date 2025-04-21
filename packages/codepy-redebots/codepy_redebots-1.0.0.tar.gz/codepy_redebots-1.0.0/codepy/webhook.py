import aiohttp
import logging
from typing import Callable, Dict, Any

logger = logging.getLogger("codepy.webhook")

class Webhook:
    def __init__(self):
        self._hooks: Dict[str, Callable] = {}

    def registrar(self, nome: str, cb: Callable):
        """Registra um webhook."""
        self._hooks[nome] = cb

    async def processar(self, nome: str, dados: Dict[str, Any]):
        """Processa um webhook."""
        if nome in self._hooks:
            try:
                await self._hooks[nome](dados)
            except Exception as e:
                logger.error(f"Erro ao processar webhook {nome}: {str(e)}")