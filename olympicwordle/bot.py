import os

from telethon import TelegramClient
from telethon.events import NewMessage, StopPropagation
from telethon.sessions import StringSession

from olympicwordle import wordle, wordle_medals

api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
client = TelegramClient(StringSession(os.environ["SESSION"]), api_id, api_hash)


async def get_messages(chat, regex):
    messages = []
    async with client:
        messages = [
            ((await m.get_sender()).first_name, m.text)
            async for m in client.iter_messages(chat, reverse=True)
            if m.text and regex.search(m.text)
        ]

    return messages


@bot.on(NewMessage(pattern="/medaljer"))
async def medaljer(event):
    messages = await get_messages(await event.get_chat(), wordle.regex)

    if messages:
        await event.respond(f"\n{wordle_medals.award_ceremony(messages)}\n")

    raise StopPropagation


bot.run_until_disconnected()
