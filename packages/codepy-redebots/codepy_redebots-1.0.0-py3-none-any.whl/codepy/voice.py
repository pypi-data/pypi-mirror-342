import nextcord
import asyncio
import logging
import aiohttp
from typing import Optional, List, Union
from pydub import AudioSegment
import io
import wave
import opuslib
import sounddevice as sd
try:
    import vlc
except ImportError:
    vlc = None
from .ia import IA
from .core import Bot, Canal

logger = logging.getLogger("codepy.voz")

class MediaPlayer:
    """Abstrai diferentes backends de reprodução de mídia sem dependência de binários."""
    def __init__(self, backend: str = "pydub", loop: Optional[asyncio.AbstractEventLoop] = None):
        self.backend = backend.lower()
        self.loop = loop or asyncio.get_event_loop()
        self.vlc_instance = vlc.Instance() if vlc else None
        self.opus_encoder = None
        self.queue: List[Union[str, io.BytesIO]] = []
        if self.backend == "opus":
            self.opus_encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)

    async def play(self, source: Union[str, io.BytesIO], vc: nextcord.VoiceClient):
        """Reproduz áudio usando o backend especificado."""
        try:
            # Normaliza o áudio para PCM/WAV
            audio = self._normalize_audio(source)
            pcm_data = self._audio_to_pcm(audio)

            if self.backend == "pydub":
                # Usa PCM puro com nextcord.PCMAudio
                vc.play(nextcord.PCMAudio(io.BytesIO(pcm_data)))
            elif self.backend == "vlc" and self.vlc_instance:
                player = self.vlc_instance.media_player_new()
                media = self.vlc_instance.media_new(source if isinstance(source, str) else source.getvalue())
                player.set_media(media)
                player.play()
                while player.get_state() not in (vlc.State.Ended, vlc.State.Error):
                    await asyncio.sleep(0.1)
            elif self.backend == "opus":
                opus_data = self.opus_encoder.encode(pcm_data, len(pcm_data))
                vc.play(nextcord.PCMAudio(io.BytesIO(opus_data)))
            elif self.backend == "sounddevice":
                # Reproduz via sounddevice (requer hardware de áudio)
                sd.play(pcm_data, samplerate=44100)
                sd.wait()
                vc.play(nextcord.PCMAudio(io.BytesIO(pcm_data)))
            else:
                raise ValueError(f"Backend {self.backend} não suportado")

            while vc.is_playing():
                await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Erro ao reproduzir com {self.backend}: {str(e)}")
            raise

    def enqueue(self, source: Union[str, io.BytesIO]):
        """Adiciona áudio à fila de reprodução."""
        self.queue.append(source)

    async def play_queue(self, vc: nextcord.VoiceClient):
        """Reproduz todos os áudios na fila."""
        while self.queue:
            source = self.queue.pop(0)
            await self.play(source, vc)

    def _normalize_audio(self, source: Union[str, io.BytesIO]) -> AudioSegment:
        """Normaliza o áudio para um formato compatível."""
        try:
            if isinstance(source, str):
                audio = AudioSegment.from_file(source)
            else:
                audio = AudioSegment.from_file(source)
            return audio.set_channels(2).set_frame_rate(44100).set_sample_width(2)
        except Exception as e:
            logger.error(f"Erro ao normalizar áudio: {str(e)}")
            raise

    def _audio_to_pcm(self, audio: AudioSegment) -> bytes:
        """Converte áudio para PCM bruto."""
        raw_data = audio.raw_data
        return raw_data

    def stop(self):
        """Para a reprodução (se aplicável)."""
        if self.backend == "vlc" and self.vlc_instance:
            player = self.vlc_instance.media_player_new()
            player.stop()
        elif self.backend == "sounddevice":
            sd.stop()

class Voz:
    def __init__(self, bot: 'Bot', canal: Canal, elevenlabs_key: Optional[str] = None, 
                 whisper_key: Optional[str] = None, backend: str = "pydub"):
        self.bot = bot
        self.canal = canal
        self.vc: Optional[nextcord.VoiceClient] = None
        self.ia = IA(elevenlabs_key=elevenlabs_key, whisper_key=whisper_key)
        self._audio_buffer = io.BytesIO()
        self.player = MediaPlayer(backend=backend)
        self.backend = backend

    async def conectar(self):
        """Conecta ao canal de voz."""
        try:
            self.vc = await self.canal._canal.connect()
            logger.info(f"Conectado ao canal de voz: {self.canal._canal.name}")
        except Exception as e:
            logger.error(f"Erro ao conectar ao canal de voz: {str(e)}")
            raise

    async def desconectar(self):
        """Desconecta do canal de voz."""
        if self.vc:
            self.player.stop()
            await self.vc.disconnect()
            self.vc = None
            logger.info(f"Desconectado do canal de voz: {self.canal._canal.name}")

    async def play_audio(self, source: Union[str, io.BytesIO]):
        """Toca um áudio ou adiciona à fila."""
        if not self.vc:
            raise ValueError("Não conectado a um canal de voz")
        try:
            self.player.enqueue(source)
            await self.player.play_queue(self.vc)
        except Exception as e:
            logger.error(f"Erro ao tocar áudio: {str(e)}")
            raise

    async def falar(self, txt: str, voz_id: str = "voz_em_portugues"):
        """Converte texto em fala e toca usando ElevenLabs."""
        try:
            audio_path = await self.ia.gerar_fala(txt, voz_id=voz_id)
            await self.play_audio(audio_path)
        except Exception as e:
            logger.error(f"Erro ao gerar e tocar fala: {str(e)}")
            raise

    async def ouvir(self, duracao: int = 5) -> str:
        """Captura e reconhece fala no canal de voz usando Whisper."""
        if not self.vc:
            raise ValueError("Não conectado a um canal de voz")
        try:
            audio_path = await self._capturar_audio(duracao)
            txt = await self.ia.reconhecer_fala(audio_path)
            return txt
        except Exception as e:
            logger.error(f"Erro ao capturar e reconhecer fala: {str(e)}")
            raise

    async def _capturar_audio(self, duracao: int) -> str:
        """Captura áudio real do canal de voz."""
        if not self.vc:
            raise ValueError("Não conectado a um canal de voz")
        
        try:
            sink = nextcord.sinks.WaveSink()
            self.vc.start_recording(sink, self._on_recording_finished, None)
            await asyncio.sleep(duracao)
            self.vc.stop_recording()
            await asyncio.sleep(1)

            output_path = "captura_audio.wav"
            with open(output_path, "wb") as f:
                f.write(self._audio_buffer.getvalue())
            
            audio = AudioSegment.from_wav(output_path)
            audio.export(output_path, format="wav")
            return output_path
        except Exception as e:
            logger.error(f"Erro ao capturar áudio: {str(e)}")
            raise

    async def _on_recording_finished(self, sink: nextcord.sinks.WaveSink, _):
        """Callback chamado quando a gravação termina."""
        try:
            self._audio_buffer.seek(0)
            self._audio_buffer.write(sink.get_buffer())
            logger.info("Gravação de áudio concluída.")
        except Exception as e:
            logger.error(f"Erro ao processar áudio gravado: {str(e)}")
            raise