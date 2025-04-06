import discord
import aiohttp
import re
from config import settings, logout_command, logout_message, system_prompt, model


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        specific_channel_id = settings.CHANNEL_ID

        if (
            message.content == logout_command
            and message.author.guild_permissions.administrator
        ):
            await message.channel.send(logout_message)
            await self.close()

        if self.user in message.mentions and message.channel.id == specific_channel_id:
            message_content = message.content

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"http://{settings.API_IP}:{settings.API_PORT}/api/generate",
                        json={
                            "model": model,
                            "system": system_prompt,
                            "prompt": message_content,
                            "stream": False,
                        },
                        # {
                        #     "model": model,
                        #     "messages": [
                        #         {"role": "system", "content": system_prompt},
                        #         {"role": "user", "content": message_content},
                        #     ],
                        #     "stream": False,
                        # }
                    ) as response:

                        response.raise_for_status()  # Raise exception for HTTP errors
                        response_json = await response.json()
                        print(response_json)

                        model_reply = response_json["response"]
                        model_reply = re.sub(
                            r"<think>.*?</think>", "", model_reply, flags=re.DOTALL
                        ).strip()

                        await message.channel.send(model_reply)

            except aiohttp.ClientError as e:
                await message.channel.send(
                    print(f"error: {e}"),
                    f"Sorry {message.author.mention}, I couldn't process your request.",
                )


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(settings.BOT_KEY)
