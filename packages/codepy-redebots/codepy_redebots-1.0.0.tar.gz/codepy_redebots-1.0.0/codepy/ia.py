import aiohttp
import logging
from typing import Optional

logger = logging.getLogger("codepy.ia")

class IA:
    def __init__(self, api_key: Optional[str] = None, elevenlabs_key: Optional[str] = None, whisper_key: Optional[str] = None):
        self.api_key = api_key or "SUA_CHAVE_API_XAI"
        self.elevenlabs_key = elevenlabs_key or "SUA_CHAVE_ELEVENLABS"
        self.whisper_key = whisper_key or "SUA_CHAVE_WHISPER"
        self.base_url_xai = "https://api.x.ai/v1"
        self.base_url_elevenlabs = "https://api.elevenlabs.io/v1"
        self.base_url_whisper = "https://api.openai.com/v1"

    async def gerar_texto(self, prompt: str, modelo: str = "grok-3") -> str:
        """Gera texto com IA."""
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {"prompt": prompt, "model": modelo}
            try:
                async with session.post(f"{self.base_url_xai}/completions", json=data, headers=headers) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
                    return result["choices"][0]["text"]
            except Exception as e:
                logger.error(f"Erro ao gerar texto: {str(e)}")
                raise

    async def gerar_fala(self, txt: str, voz_id: str = "voz_em_portugues") -> str:
        """Gera áudio a partir de texto usando ElevenLabs."""
        async with aiohttp.ClientSession() as session:
            headers = {"xi-api-key": self.elevenlabs_key}
            data = {
                "text": txt,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            try:
                async with session.post(
                    f"{self.base_url_elevenlabs}/text-to-speech/{voz_id}",
                    json=data,
                    headers=headers
                ) as resp:
                    resp.raise_for_status()
                    audio_data = await resp.read()
                    output_path = "fala_gerada.wav"
                    with open(output_path, "wb") as f:
                        f.write(audio_data)
                    logger.info(f"Fala gerada salva em: {output_path}")
                    return output_path
            except Exception as e:
                logger.error(f"Erro ao gerar fala com ElevenLabs: {str(e)}")
                raise

    async def reconhecer_fala(self, arquivo: str) -> str:
        """Reconhece fala de áudio usando Whisper."""
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.whisper_key}"}
            with open(arquivo, "rb") as f:
                data = aiohttp.FormData()
                data.add_field("file", f, filename="audio.wav")
                data.add_field("model", "whisper-1")
                data.add_field("language", "pt")
                try:
                    async with session.post(
                        f"{self.base_url_whisper}/audio/transcriptions",
                        headers=headers,
                        data=data
                    ) as resp:
                        resp.raise_for_status()
                        result = await resp.json()
                        logger.info(f"Fala reconhecida: {result['text']}")
                        return result["text"]
                except Exception as e:
                    logger.error(f"Erro ao reconhecer fala com Whisper: {str(e)}")
                    raise