import discord
import os

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("hello"):
            await message.channel.send(f"Hi there {message.author}!")

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(f"You reacted")

intents  = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(os.environ["DISCORD_TOKEN"])