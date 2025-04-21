import unittest
import asyncio
from codepy import Code, Inter, Cmd

class TestCommands(unittest.TestCase):
    def test_registrar_cmd(self):
        bot = Code.criar_bot(prefix="!")
        @bot.cmd(nome="info", desc="Info do user", opts=[{"nome": "user", "desc": "Usuário", "tipo": "user"}])
        async def info(inter: Inter, user: User):
            await inter.resp(f"Info de {user.nome}")
        self.assertIn("info", bot.cmds._slash_cmds)

if __name__ == "__main__":
    unittest.main()