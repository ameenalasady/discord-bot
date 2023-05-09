import discord
import responses
import logging
import os

logging.basicConfig(level=logging.ERROR)


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        async with message.author.typing():
            await message.author.send(response) if is_private else await message.channel.send(response)

    except discord.Forbidden:
        logging.error(
            "Bot doesn't have permission to send a message to the user")
    except discord.HTTPException:
        logging.error("Failed to send message due to an HTTP error")


def run_discord_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logging.info(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        logging.info(f'{username} said: "{user_message}" ({channel})')

        if user_message.startswith('?'):
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(str(os.getenv('DISCORD_TOKEN')))


run_discord_bot()
