import aiohttp
import logging
from typing import Dict, List, Optional

logger = logging.getLogger("codepy.oauth")

class OAuth:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.base_url = "https://discord.com/api/v10"

    async def get_auth_url(self, scopes: List[str]) -> str:
        """Gera a URL de autenticação OAuth2."""
        scopes_str = " ".join(scopes)
        return f"{self.base_url}/oauth2/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope={scopes_str}"

    async def trocar_codigo(self, code: str) -> Dict:
        """Troca o código por um token de acesso."""
        async with aiohttp.ClientSession() as session:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri
            }
            try:
                async with session.post(f"{self.base_url}/oauth2/token", data=data) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            except Exception as e:
                logger.error(f"Erro ao trocar código OAuth2: {str(e)}")
                raise