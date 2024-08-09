
from rubpy import Client, handlers
import asyncio

async def main():
    async with Client(session='SiSi-AUTH') as client:
        @client.on(handlers.MessageUpdates())
        async def updates(update):
            await update.reply('`hello` __from__ **rubpy**')
        await client.run_until_disconnected()

asyncio.run(main())






























help_text = f"""
SiSi-BOT |
├ • ℍ𝕖𝕝𝕡 ↬ (دستورات) -> نشان دادن دستورات
├ • 𝕄𝕠𝕕𝕖 ↬ (.mode) -> مود ها
├ • 𝕋𝕠𝕠𝕝𝕤 ↬ (.tools) -> ابزار ها
├ • 𝔼𝕟𝕖𝕞𝕪 ↬ (.enemy) -> حالت دشمن

ᴹᵞ ᴵᴰ @MSFsploit""".encode("utf-8")