import discord, json, random
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
    await bot.add_cog(TankTactics(bot))

    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    member_count = 0
    guild_string = ""
    for g in bot.guilds:
        guild_string += f"{g.name} - {g.id} - Members: {g.member_count}\n"
        member_count += g.member_count
    print(
        f"Bot '{bot.user.name}' has connected, active on {len(bot.guilds)} guilds:\n{guild_string}")


def fillscreen():
    with open("playerlist.txt", "r") as f:
        plist = f.read().split("\n")
    #print(plist)
    replymessage=""
    for y in range(10):
        for x in range(10):
            replymessage +="⬛"
            for player in plist:
                if(player==''):
                    break
                with open("players.json", "r") as f:
                    json_data = json.loads(f.read())
                if(json_data[player][0]==x and json_data[player][1]==y):
                    replymessage = replymessage[:-1]
                    replymessage +="📦"
            
        replymessage+="\n"
    return replymessage

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        print(fillscreen())

class TankTactics(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    
    async def nS(self,ctx):
        """Creates a new screen"""
        await ctx.message.delete()
        screen = await ctx.send(fillscreen())
        f = open("viewmessage.txt", "w+")
        f.write(str(screen.id))
        f.close()
        

    @commands.command()
    async def rS(self,ctx):
        """refreshes screen"""
        await ctx.message.delete()
        channel = bot.get_channel(956642445330907138)
        f = open("viewmessage.txt", "r+")
        msg = await channel.fetch_message(f.read())
        f.close()
        await msg.edit(content=fillscreen())

    @commands.command()
    async def join(self,ctx):
        """join to game"""
        await ctx.message.delete()
        with open("players.json", "r+") as f:
            json_data = json.loads(f.read())
            json_data[ctx.author.id] = [random.randrange(7),random.randrange(7)]
        
        with open("players.json", "w") as f:
            new_json = json.dumps(json_data, indent=4)
            f.write(new_json)
            
        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(956642445330907138)
            msg = await channel.fetch_message(f.read())

        with open("playerlist.txt","w") as f:
            content = f.read()
            content+= f"{ctx.author.id}\n"
            f.write(content)
        
        await msg.edit(content=fillscreen())
        




intents = discord.Intents.default()
intents.message_content = True

bot.run(token)