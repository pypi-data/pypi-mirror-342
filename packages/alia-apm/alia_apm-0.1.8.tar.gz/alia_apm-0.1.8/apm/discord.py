from discord import Client, Intents
from discord.app_commands import CommandTree


class DiscordBot(Client):
    def __init__(self, token: str, intents: Intents | None):
        self.token = token

        if intents is None:
            intents = Intents.default()

        super().__init__(intents=intents)

        self.tree = CommandTree(self)

        @self.event
        async def on_ready(self):
            await self.tree.sync()

    def run(self):
        super().run(self.token)


__all__ = ["DiscordBot"]