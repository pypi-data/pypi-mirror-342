from enum import Enum
import nextcord

class EstiloBtn(Enum):
    primario = nextcord.ButtonStyle.primary
    secundario = nextcord.ButtonStyle.secondary
    sucesso = nextcord.ButtonStyle.green
    perigo = nextcord.ButtonStyle.red
    link = nextcord.ButtonStyle.link

class TipoOpt(Enum):
    texto = nextcord.SlashOptionType.string
    inteiro = nextcord.SlashOptionType.integer
    bool = nextcord.SlashOptionType.boolean
    user = nextcord.SlashOptionType.user
    canal = nextcord.SlashOptionType.channel
    cargo = nextcord.SlashOptionType.role
    anexo = nextcord.SlashOptionType.attachment