import unittest
import asyncio
from codepy import Code, Inter, Embed

class TestCore(unittest.TestCase):
    def test_criar_bot(self):
        bot = Code.criar_bot(prefix="!")
        self.assertIsNotNone(bot)

    async def test_comando(self):
        bot = Code.criar_bot(prefix="!")
        @bot.cmd(nome="teste", desc="Comando de teste")
        async def teste(inter: Inter):
            await inter.resp("Teste OK", embed=Embed(tit="Teste"))
        self.assertIn("teste", bot.cmds._slash_cmds)

if __name__ == "__main__":
    unittest.main()