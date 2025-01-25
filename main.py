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

@client.tree.command(name="embed", description="Embed demo", guild=GUILD_ID)
async def printer(interaction: discord.Integration):
    embed = discord.Embed(title="I am a title", url="https://www.youtube.com/watch?v=xvFZjo5PgG0&ab_channel=Duran", description="I am the description", color=discord.Color.dark_purple())
    embed.set_thumbnail(url="https://images2.minutemediacdn.com/image/upload/c_fill,w_1200,ar_4:3,f_auto,q_auto,g_auto/shape/cover/sport/649273-youtube-rick-astley-6b69666394bb6020a913c6fcd18f74be.jpg")
    embed.add_field(name="Field 1", value="I am the field 1")
    embed.add_field(name="Field 2", value="I am the field 2")
    embed.add_field(name="Field 3", value="I am the field 3", inline=False)
    embed.set_author(name=interaction.user.name, url="https://www.youtube.com/watch?v=uOpdyytB3OY&ab_channel=Protocube", icon_url="https://www.rpnation.com/data/avatars/l/36/36968.jpg?1488155304")
    await interaction.response.send_message(embed=embed)

client.run(os.environ["DISCORD_TOKEN"])