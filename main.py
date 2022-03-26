import discord
from discord.ext import commands

description = 'bot made by F1L1P.\n'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), description=description, intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name=".help", status=discord.Status.dnd))

token = open("token.txt", "r")
token = token.read()

@bot.event
async def on_ready():

    await bot.add_cog(Ping(bot))

    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    member_count = 0
    guild_string = ""
    for g in bot.guilds:
        guild_string += f"{g.name} - {g.id} - Members: {g.member_count}\n"
        member_count += g.member_count
    print(
        f"Bot '{bot.user.name}' has connected, active on {len(bot.guilds)} guilds:\n{guild_string}")


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.reply("pong")


intents = discord.Intents.default()
intents.message_content = True

bot.run(token)