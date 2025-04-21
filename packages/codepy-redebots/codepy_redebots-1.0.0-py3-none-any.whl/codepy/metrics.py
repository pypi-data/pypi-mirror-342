from typing import Dict
import time

class Metrics:
    def __init__(self):
        self._mets: Dict[str, int] = {
            "resps": 0, "modais": 0, "edits": 0, "inters": 0, "erros": 0, "lat_ms": 0
        }
        self._ultima: float = time.time()

    def inc(self, met: str):
        """Incrementa uma métrica."""
        self._mets[met] = self._mets.get(met, 0) + 1
        self._atualizar_lat()

    def _atualizar_lat(self):
        """Atualiza latência."""
        agora = time.time()
        self._mets["lat_ms"] = int((agora - self._ultima) * 1000)
        self._ultima = agora

    def obter(self) -> Dict[str, int]:
        """Retorna métricas."""
        return self._mets.copy()