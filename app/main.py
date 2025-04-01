import discord
import requests
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
            # Store the message content
            message_content = message.content

            # Send the message content to Ollama
            try:
                response = requests.post(
                    f"http://{settings.API_IP}:{settings.API_PORT}/api/chat",
                    json={
                        "model": model,  # Replace with the model name you're using in Ollama
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt,
                            },
                            {"role": "user", "content": message_content},
                        ],
                        "stream": False,
                    },
                )

                print(response.json())
                response.raise_for_status()  # Raise an error for HTTP issues
                model_reply = response.json()["message"]["content"]
                # use if model has a <think> tag in the response
                model_reply = re.sub(
                    r"<think>.*?</think>", "", model_reply, flags=re.DOTALL
                ).strip()

                # Send the model's reply back to the Discord channel
                await message.channel.send(f"{model_reply}")
            except requests.exceptions.RequestException as e:
                # Handle errors (e.g., Ollama not running or API issues)
                await message.channel.send(
                    f"Sorry {message.author.mention}, I couldn't process your request. Error: {e}"
                )


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(settings.BOT_KEY)
