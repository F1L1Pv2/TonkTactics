from calendar import c
from re import L
from turtle import up
import discord, json, random
from discord.ext import commands
from discord.ui import Button, View

description = 'bot made by F1L1P.\n'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), description=description, intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name=".help", status=discord.Status.dnd))

token = open("token.txt", "r")
token = token.read()

@bot.event
async def on_ready():

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
                with open("players.json", "r") as f:
                    json_data = json.loads(f.read())
                with open("emoji.json", "r") as f:
                    emoji_data = json.loads(f.read())
                if(json_data[player][0]==x and json_data[player][1]==y):
                    replymessage = replymessage[:-1]
                    replymessage +=emoji_data[player][0]
            
        replymessage+="\n"
    return replymessage

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
    async def left(self,ctx):
        await ctx.message.delete()
        with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0]-1,json_data[str(ctx.author.id)][1]]
        with open("players.json", "w") as f:
            new_json = json.dumps(json_data, indent=4)
            f.write(new_json)
        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(956642445330907138)
            msg = await channel.fetch_message(f.read())     
        await msg.edit(content=fillscreen())

    @commands.command()
    async def right(self,ctx):
        await ctx.message.delete()
        with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0]+1,json_data[str(ctx.author.id)][1]]
        with open("players.json", "w") as f:
            new_json = json.dumps(json_data, indent=4)
            f.write(new_json)
        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(956642445330907138)
            msg = await channel.fetch_message(f.read())     
        await msg.edit(content=fillscreen())
    
    @commands.command()
    async def up(self,ctx):
        await ctx.message.delete()
        with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0],json_data[str(ctx.author.id)][1]-1]
        with open("players.json", "w") as f:
            new_json = json.dumps(json_data, indent=4)
            f.write(new_json)
        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(956642445330907138)
            msg = await channel.fetch_message(f.read())     
        await msg.edit(content=fillscreen())

    @commands.command()
    async def down(self,ctx):
        await ctx.message.delete()
        with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0],json_data[str(ctx.author.id)][1]+1]
        with open("players.json", "w") as f:
            new_json = json.dumps(json_data, indent=4)
            f.write(new_json)
        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(956642445330907138)
            msg = await channel.fetch_message(f.read())     
        await msg.edit(content=fillscreen())

    @commands.command()
    async def join(self,ctx, emoji: str = None):
        """join to game"""

        if (emoji is None):
            emoji = "📦"

        await ctx.message.delete()
        with open("playerlist.txt","r") as f:
            content = f.read()
            L = content.split("\n")
        if(str(ctx.author.id) in L):
            return

        with open("emoji.json", "r+") as f:
            emokji_data = json.loads(f.read())
            emokji_data[ctx.author.id] = emoji
        
        with open("emoji.json", "w") as f:
            new_ejson = json.dumps(emokji_data, indent=4)
            f.write(new_ejson)
        
        with open("playerlist.txt", "w") as f:
            content+= f"{ctx.author.id}\n"
            f.write(content)
    
        with open("players.json", "r+") as f:
            json_data = json.loads(f.read())
            json_data[ctx.author.id] = [random.randrange(7),random.randrange(7)]
        
        with open("players.json", "w") as f:
            new_json = json.dumps(json_data, indent=4)
            f.write(new_json)
            
        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(956642445330907138)
            msg = await channel.fetch_message(f.read())

        await msg.edit(content=fillscreen())
        
    @commands.command()
    async def bC(self,ctx):
        """creates button"""
        await ctx.message.delete()
        leftb = Button(label="", style=discord.ButtonStyle.grey, emoji="⬅️")
        rightb = Button(label="", style=discord.ButtonStyle.grey, emoji="➡️")
        upb = Button(label="", style=discord.ButtonStyle.grey, emoji="⬆️")
        downb = Button(label="", style=discord.ButtonStyle.grey, emoji="⬇️")
        upleftb = Button(label="", style=discord.ButtonStyle.grey, emoji="↖️")
        uprightb = Button(label="", style=discord.ButtonStyle.grey, emoji="↗️")
        downleftb = Button(label="", style=discord.ButtonStyle.grey, emoji="↙️")
        downrightb = Button(label="", style=discord.ButtonStyle.grey, emoji="↘️")
        button = Button(label="", style=discord.ButtonStyle.grey, emoji="🟦")
        async def left(interaction):
            with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0]-1,json_data[str(ctx.author.id)][1]]
            with open("players.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)
            
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(956642445330907138)
                msg = await channel.fetch_message(f.read())
                
            await msg.edit(content=fillscreen())
            #await interaction.response.send_message('left')
        
        async def right(interaction):
            with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0]+1,json_data[str(ctx.author.id)][1]]
            with open("players.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)
            
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(956642445330907138)
                msg = await channel.fetch_message(f.read())
                
            await msg.edit(content=fillscreen())
            #await interaction.response.send_message('right')

        async def up(interaction):
            with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0],json_data[str(ctx.author.id)][1]-1]
            with open("players.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)
            
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(956642445330907138)
                msg = await channel.fetch_message(f.read())
                
            await msg.edit(content=fillscreen())
            #await interaction.response.send_message('up')

        async def down(interaction):
            with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0],json_data[str(ctx.author.id)][1]+1]
            with open("players.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)
            
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(956642445330907138)
                msg = await channel.fetch_message(f.read())
                
            await msg.edit(content=fillscreen())
            #await interaction.response.send_message('down')

        async def upleft(interaction):
            with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0]-1,json_data[str(ctx.author.id)][1]-1]
            with open("players.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)
            
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(956642445330907138)
                msg = await channel.fetch_message(f.read())
                
            await msg.edit(content=fillscreen())
            #await interaction.response.send_message('up')

        async def upright(interaction):
            with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0]+1,json_data[str(ctx.author.id)][1]-1]
            with open("players.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)
            
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(956642445330907138)
                msg = await channel.fetch_message(f.read())
                
            await msg.edit(content=fillscreen())
            #await interaction.response.send_message('up')

        async def downleft(interaction):
            with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0]-1,json_data[str(ctx.author.id)][1]+1]
            with open("players.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)
            
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(956642445330907138)
                msg = await channel.fetch_message(f.read())
                
            await msg.edit(content=fillscreen())
            #await interaction.response.send_message('down')

        async def downright(interaction):
            with open("players.json", "r+") as f:
                json_data = json.loads(f.read())
                json_data[str(ctx.author.id)] = [json_data[str(ctx.author.id)][0]+1,json_data[str(ctx.author.id)][1]+1]
            with open("players.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)
            
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(956642445330907138)
                msg = await channel.fetch_message(f.read())
                
            await msg.edit(content=fillscreen())
            #await interaction.response.send_message('down')

        leftb.callback = left
        rightb.callback = right
        upb.callback = up
        downb.callback = down
        upleftb.callback = upleft
        uprightb.callback = upright
        downrightb.callback = downright
        downleftb.callback = downleft

        upview=View()
        midview=View()
        downview=View()
        
        upview.add_item(upleftb)
        upview.add_item(upb)
        upview.add_item(uprightb)

        midview.add_item(leftb)
        midview.add_item(button)
        midview.add_item(rightb)
        
        downview.add_item(downleftb)
        downview.add_item(downb)
        downview.add_item(downrightb)

        await ctx.send("",view=upview)
        await ctx.send("",view=midview)
        await ctx.send("",view=downview)



intents = discord.Intents.default()
intents.message_content = True

bot.run(token)