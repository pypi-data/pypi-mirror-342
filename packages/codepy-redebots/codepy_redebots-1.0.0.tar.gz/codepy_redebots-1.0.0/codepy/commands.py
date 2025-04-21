import nextcord
from typing import Callable, Optional, Dict, List
from .core import Inter, Bot
from .tipos import TipoOpt
import logging

logger = logging.getLogger("codepy.cmds")

class Cmd:
    def __init__(self, nome: str, desc: str, opts: List[Dict], tipo: str, func: Callable):
        self.nome = nome
        self.desc = desc
        self.opts = opts
        self.tipo = tipo
        self.func = func

class CmdManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self._slash_cmds: Dict[str, Cmd] = {}
        self._ctx_cmds: Dict[str, Cmd] = {}
        self._synced: Dict[str, bool] = {}

    def registrar(self, nome: str, desc: str = "Sem desc", opts: Optional[List[Dict]] = None,
                  tipo: str = "slash"):
        """Registra um comando."""
        def decorador(func: Callable):
            cmd = Cmd(nome, desc, opts or [], tipo, func)
            if tipo == "slash":
                self._slash_cmds[nome] = cmd
            elif tipo in ("user", "msg"):
                self._ctx_cmds[nome] = cmd
            return func
        return decorador

    async def sync(self):
        """Sincronização incremental de comandos."""
        for nome, cmd in self._slash_cmds.items():
            if not self._synced.get(nome):
                options = [
                    nextcord.SlashOption(
                        name=opt["nome"],
                        description=opt.get("desc", "Sem desc"),
                        type=TipoOpt[opt["tipo"]].value,
                        required=opt.get("obrig", False)
                    )
                    for opt in cmd.opts
                ]
                self.bot.tree.add_command(
                    nextcord.SlashCommand(
                        name=nome,
                        description=cmd.desc,
                        options=options,
                        callback=lambda inter, *args, **kwargs: cmd.func(Inter(inter, self.bot.cache, self.bot.metrics), *args, **kwargs)
                    )
                )
                self._synced[nome] = True
                logger.info(f"Comando {nome} registrado.")

        for nome, cmd in self._ctx_cmds.items():
            if not self._synced.get(nome):
                self.bot.tree.add_command(
                    nextcord.ApplicationCommand(
                        name=nome,
                        description=cmd.desc,
                        type=nextcord.ApplicationCommandType.user if cmd.tipo == "user" else nextcord.ApplicationCommandType.message,
                        callback=lambda inter, target: cmd.func(Inter(inter, self.bot.cache, self.bot.metrics), target)
                    )
                )
                self._synced[nome] = True
                logger.info(f"Comando contextual {nome} registrado.")

        await self.bot.tree.sync()
        logger.info("Comandos sincronizados com o Discord.")