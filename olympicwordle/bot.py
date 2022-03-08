import os

from telethon import TelegramClient
from telethon.events import NewMessage, StopPropagation
from telethon.sessions import StringSession

from olympicwordle import wordle

api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)
client = TelegramClient(StringSession(os.environ["SESSION"]), api_id, api_hash)


@bot.on(NewMessage(pattern="/medaljer"))
async def start(event):
    messages = []
    async with client:
        chat = await event.get_chat()
        messages = [
            ((await m.get_sender()).first_name, m.text)
            async for m in client.iter_messages(chat, reverse=True)
        ]

    if messages:
        response = []
        wordle_messages = [m for m in messages if m[1] and wordle.regex.search(m[1])]

        if wordle_messages:
            wordle_scores = wordle.parse_scores(wordle_messages)
            wordle_response = wordle.award_ceremony(wordle_scores)
            response.append(wordle_response)

        if response:
            await event.respond("\n".join(response))

    raise StopPropagation


bot.run_until_disconnected()
