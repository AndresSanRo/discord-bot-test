import discord
from discord.ext import commands
from discord import app_commands
import os


class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}")        
        try:
            guild = discord.Object(id=os.environ["DISCORD_SERVER_ID"])
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith("hello"):
            await message.channel.send(f"Hi there {message.author}!")

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(f"You reacted")

intents  = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=os.environ["DISCORD_SERVER_ID"])

@client.tree.command(name="hello", description="Say hello", guild=GUILD_ID)
async def hello(interaction: discord.Integration):
    await interaction.response.send_message("Hello there!")

@client.tree.command(name="print", description="I will print whatever you give me!", guild=GUILD_ID)
async def printer(interaction: discord.Integration, printer: str):
    await interaction.response.send_message(printer)

client.run(os.environ["DISCORD_TOKEN"])