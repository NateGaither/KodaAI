import os
from pathlib import Path

import discord

from src.core.koda_core import KodaCore


def _load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


class KodaDiscordBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

        _load_env_file()
        owner_raw = os.getenv("OWNER_ID", "")
        self.owner_id = int(owner_raw) if owner_raw.isdigit() else None
        self.core = KodaCore()

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} ({self.user.id})")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        content = message.content.strip()
        if not content:
            return

        if content == "!ping":
            await message.channel.send("pong")
            return

        if content == "!reset":
            await message.channel.send("memory reset not implemented")
            return

        try:
            response = self.core.handle_message(content, str(message.author.id))
            await message.channel.send(response)
        except Exception as exc:
            print(f"Error handling Discord message: {exc}")
            await message.channel.send("Sorry, I hit an internal error while processing that message.")


def run_bot() -> None:
    _load_env_file()
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN is not set in environment or .env")

    bot = KodaDiscordBot()
    bot.run(token)


if __name__ == "__main__":
    run_bot()
