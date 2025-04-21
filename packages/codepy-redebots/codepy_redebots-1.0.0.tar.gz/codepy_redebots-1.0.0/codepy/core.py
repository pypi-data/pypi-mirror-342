import nextcord
from nextcord.ext import commands
import asyncio
import uuid
import logging
from typing import Callable, Optional, Dict, List, Any
from .cache import Cache
from .metrics import Metrics
from .events import Eventos
from .commands import CmdManager
from .tipos import EstiloBtn
from .voice import Voz
from .utils import abrev

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("codepy")

class Embed:
    def __init__(self, tit: str = "", desc: str = "", cor: int = 0x00FF00):
        self._embed = nextcord.Embed(title=tit, description=desc, color=cor)

    def add_campo(self, nome: str, valor: str, inline: bool = False):
        self._embed.add_field(name=nome, value=valor, inline=inline)
        return self

    @property
    def interno(self) -> nextcord.Embed:
        return self._embed

class Msg:
    def __init__(self, msg: nextcord.Message):
        self._msg = msg

    @property
    def txt(self) -> str:
        return self._msg.content

    @property
    def user(self) -> 'User':
        return User(self._msg.author)

class User:
    def __init__(self, user: nextcord.User):
        self._user = user

    @property
    def nome(self) -> str:
        return self._user.name

    @property
    def id(self) -> int:
        return self._user.id

class Canal:
    def __init__(self, canal: nextcord.abc.Messageable):
        self._canal = canal

    async def enviar(self, txt: str, embed: Optional[Embed] = None):
        await self._canal.send(content=txt, embed=embed.interno if embed else None)

class Cargo:
    def __init__(self, cargo: nextcord.Role):
        self._cargo = cargo

    @property
    def nome(self) -> str:
        return self._cargo.name

class Inter:
    def __init__(self, inter: nextcord.Interaction, cache: Cache, metrics: Metrics):
        self._inter = inter
        self.cache = cache
        self.metrics = metrics
        self.resp_enviada = False
        self.id = str(uuid.uuid4())

    @property
    def user(self) -> User:
        return User(self._inter.user)

    async def resp(self, txt: str = "", embed: Optional[Embed] = None,
                  btns: Optional[List[Dict]] = None, menu: Optional[Dict] = None,
                  efemera: bool = False):
        """Envia uma resposta à interação."""
        self.metrics.inc("resps")
        comps = []

        if btns:
            row = nextcord.ui.ActionRow()
            for btn in btns:
                row.append_item(
                    nextcord.ui.Button(
                        label=btn["txt"],
                        style=EstiloBtn[btn.get("estilo", "primario")].value,
                        custom_id=btn["id"]
                    )
                )
            comps.append(row)

        if menu:
            select = nextcord.ui.Select(
                placeholder=menu["placeholder"],
                options=[
                    nextcord.SelectOption(label=op["txt"], value=op["valor"])
                    for op in menu["opts"]
                ],
                custom_id=menu["id"]
            )
            comps.append(nextcord.ui.ActionRow(select))

        if not self.resp_enviada:
            await self._inter.response.send_message(
                content=txt, embed=embed.interno if embed else None,
                components=comps, ephemeral=efemera
            )
            self.resp_enviada = True
        else:
            await self._inter.followup.send(
                content=txt, embed=embed.interno if embed else None,
                components=comps, ephemeral=efemera
            )

    async def modal(self, tit: str, campos: List[Dict], cb: Optional[Callable] = None):
        """Cria e envia um modal."""
        self.metrics.inc("modais")
        modal = nextcord.ui.Modal(title=tit, custom_id=f"modal_{self.id}")
        for campo in campos:
            modal.add_item(
                nextcord.ui.TextInput(
                    label=campo["nome"],
                    placeholder=campo.get("placeholder", ""),
                    required=campo.get("obrig", False),
                    default_value=campo.get("padrao", "")
                )
            )
        if cb:
            self.cache.set(f"modal_cb_{modal.custom_id}", cb)
        await self._inter.response.send_modal(modal)

    async def edit(self, txt: str = "", embed: Optional[Embed] = None):
        """Edita a mensagem original."""
        self.metrics.inc("edits")
        await self._inter.edit_original_message(
            content=txt, embed=embed.interno if embed else None
        )

    def salvar(self, chave: str, valor: Any):
        """Salva estado no cache."""
        self.cache.set(f"inter_{self.id}_{chave}", valor)

    def obter(self, chave: str) -> Any:
        """Recupera estado do cache."""
        return self.cache.get(f"inter_{self.id}_{chave}")

class Bot(commands.Bot):
    def __init__(self, prefix: str = "!", intents: Dict[str, bool] = None,
                 shards: Optional[int] = None, cache_conf: Optional[Dict] = None):
        intents = intents or {
            "default": True, "guilds": True, "messages": True, "reactions": True,
            "members": True, "presences": True, "voice_states": True
        }
        nc_intents = nextcord.Intents(**intents)
        super().__init__(command_prefix=prefix, intents=nc_intents, shard_count=shards)
        self.cmds = CmdManager(self)
        self.eventos = Eventos()
        self.inters: Dict[str, Callable] = {}
        self.cache = Cache(config=cache_conf or {})
        self.metrics = Metrics()
        self.voz_clients: Dict[int, Voz] = {}

    async def iniciar(self, token: str):
        """Inicia o bot."""
        logger.info("Iniciando bot...")
        await self.start(token)

    def cmd(self, nome: str, desc: str = "Sem desc", opts: Optional[List[Dict]] = None,
            tipo: str = "slash"):
        """Decorador para comandos."""
        return self.cmds.registrar(nome, desc, opts, tipo)

    def btn(self, id: str):
        """Decorador para botões."""
        def decorador(func: Callable):
            self.inters[id] = func
            return func
        return decorador

    def menu(self, id: str):
        """Decorador para menus."""
        def decorador(func: Callable):
            self.inters[id] = func
            return func
        return decorador

    def modal_cb(self, id: str):
        """Decorador para callbacks de modais."""
        def decorador(func: Callable):
            self.inters[id] = func
            return func
        return decorador

    def evt(self, nome: str):
        """Decorador para eventos."""
        def decorador(func: Callable):
            self.eventos.registrar(nome, func)
            return func
        return decorador

    async def on_ready(self):
        """Evento de bot pronto."""
        logger.info(f"Bot conectado como {self.user.name} (ID: {self.user.id})")
        await self.cmds.sync()

    async def on_interaction(self, inter: nextcord.Interaction):
        """Lida com interações."""
        custom_id = inter.data.get("custom_id")
        if custom_id and custom_id in self.inters:
            self.metrics.inc("inters")
            try:
                await self.inters[custom_id](Inter(inter, self.cache, self.metrics))
            except Exception as e:
                self.metrics.inc("erros")
                logger.error(f"Erro na interação {custom_id}: {str(e)}")

        if custom_id and custom_id.startswith("modal_"):
            cb = self.cache.get(f"modal_cb_{custom_id}")
            if cb:
                await cb(Inter(inter, self.cache, self.metrics), inter.data["components"])

    async def on_message(self, msg: nextcord.Message):
        """Lida com mensagens."""
        await self.eventos.disparar("msg", Msg(msg))
        await super().on_message(msg)

    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        """Lida com reações."""
        await self.eventos.disparar("reacao_add", payload)

class Code:
    @staticmethod
    @abrev
    def criar_bot(prefix: str = "!", intents: Optional[Dict[str, bool]] = None,
                  shards: Optional[int] = None, cache_conf: Optional[Dict] = None):
        """Cria um bot."""
        return Bot(prefix=prefix, intents=intents, shards=shards, cache_conf=cache_conf)

    @staticmethod
    @abrev
    def rodar(bot: Bot, token: str):
        """Roda o bot."""
        try:
            bot.run(token)
        except Exception as e:
            logger.error(f"Erro ao rodar o bot: {str(e)}")
            raise