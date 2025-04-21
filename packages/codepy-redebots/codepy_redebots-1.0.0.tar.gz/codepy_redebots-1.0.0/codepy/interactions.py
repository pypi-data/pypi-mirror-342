import nextcord
from typing import Callable, Dict, List
from .core import Inter
import logging

logger = logging.getLogger("codepy.interactions")

class InterManager:
    def __init__(self):
        self._auto_completes: Dict[str, Callable] = {}

    def autocomplete(self, cmd_nome: str, opt_nome: str):
        """Registra um callback de autocomplete."""
        def decorador(func: Callable):
            self._auto_completes[f"{cmd_nome}:{opt_nome}"] = func
            return func
        return decorador

    async def processar_autocomplete(self, inter: nextcord.Interaction, cmd_nome: str, opt_nome: str, valor: str) -> List[Dict]:
        """Processa autocomplete."""
        key = f"{cmd_nome}:{opt_nome}"
        if key in self._auto_completes:
            try:
                opts = await self._auto_completes[key](Inter(inter, None, None), valor)
                return [{"name": opt["nome"], "value": opt["valor"]} for opt in opts]
            except Exception as e:
                logger.error(f"Erro no autocomplete {key}: {str(e)}")
        return []