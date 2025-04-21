from twitchio.ext.commands import Bot


class TwitchBot(Bot):
    def __init__(self, token: str, prefix: str, initial_channels: list[str]) -> None:
        super().__init__(token=token, prefix=prefix, initial_channels=initial_channels)


__all__ = ["TwitchBot"]

if __name__ == '__main__':
    from os import environ
    
    from twitchio.ext.commands.core import Context
    from twitchio.message import Message

    token = "oauth:" + environ["TWITCH_ACCESS_TOKEN"]

    bot = TwitchBot(token=token, prefix="!", initial_channels=[
        "thebestabnormalnormality"])


    @bot.event()
    async def event_ready() -> None:
        print(f"[READY] Logged in as {bot.nick}")


    @bot.event()
    async def event_message(message: Message) -> None:
        if message.echo:
            return

        print(f"{message.author.name}: {message.content}")
        await bot.handle_commands(message)


    @bot.command(name="test")
    async def hello_command(ctx: Context) -> None:
        type_name = type(ctx).__name__
        module_name = type(ctx).__module__
        await ctx.send(f"ctx is a {type_name} from module {module_name}")

    bot.run()
