import discord
import json
import random
import asyncio
from discord.ext import commands
from discord.ui import Button, View

description = 'bot made by F1L1P.\n'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), description=description, intents=intents,
                   activity=discord.Activity(type=discord.ActivityType.watching, name=".help", status=discord.Status.dnd))

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


def inrange(x, y, tarx, tary, range):
    if(x-range <= tarx <= x+range):
        if(y-range <= tary <= y+range):
            return True
    return False


def getList(dict):
    return dict.keys()


def move(x, y, author):
    femoji = ""
    fcordinates = []
    with open("list.json", "r+") as f:
        json_data = json.loads(f.read())
        femoji = json_data[str(author)]["emoji"]
        fcordinates = json_data[str(author)]["cordinates"]
        ranges = json_data[str(author)]["range"]
        lives = json_data[str(author)]["life"]
        energ = json_data[str(author)]["energy"]
        if(energ > 0):
            json_data[str(author)] = {"emoji": femoji, "cordinates": [
                fcordinates[0]+x, fcordinates[1]+y], "range": ranges, "life": lives, "energy": energ-1}
    with open("list.json", "w") as f:
        new_json = json.dumps(json_data, indent=4)
        f.write(new_json)


def fillscreen():
    with open("list.json", "r") as f:
        json_data = json.loads(f.read())
    replymessage = ""
    for y in range(14):
        for x in range(14):
            replymessage += "⬛"
            for player in json_data.keys():
                if(player == ''):
                    break
                if(json_data[player]["cordinates"][0] == x and json_data[player]["cordinates"][1] == y):
                    replymessage = replymessage[:-1]
                    replymessage += json_data[player]["emoji"][0]

        replymessage += "\n"
    return replymessage


class TankTactics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("list.json", "r") as f:
            json_data = json.loads(f.read())
        energy = json_data[str(member.id)]["energy"]
        life = json_data[str(member.id)]["life"]
        msg = await ctx.send(f"{member.name} has {energy} energy {life} lifes")
        await ctx.message.delete()
        await asyncio.sleep(2)
        await msg.delete() 

    @commands.command()
    async def shoot(self, ctx, *, member: discord.Member = None):
        """shoot"""

        if member is None:
            return

        with open("list.json", "r") as f:
            json_data = json.loads(f.read())

        playerrange = json_data[str(ctx.author.id)]["range"]
        playerx = json_data[str(ctx.author.id)]["cordinates"][0]
        playery = json_data[str(ctx.author.id)]["cordinates"][1]
        tarx = json_data[str(member.id)]["cordinates"][0]
        tary = json_data[str(member.id)]["cordinates"][1]
        if(str(member.id) in json_data):
            if(inrange(playerx, playery, tarx, tary, playerrange)):
                json_data[str(member.id)]["life"] -= 1
                if (json_data[str(member.id)]["life"] == 0):
                    json_data.pop(str(member.id))
                with open("list.json", "w") as f:
                    new_json = json.dumps(json_data, indent=4)
                    f.write(new_json)
                await ctx.message.add_reaction("✅")

                with open("viewmessage.txt", "r+") as f:
                    channel = bot.get_channel(ctx.channel.id)
                    msg = await channel.fetch_message(f.read())

                await msg.edit(content=fillscreen())
                await asyncio.sleep(2)
                await ctx.message.delete()
                return

        await ctx.message.add_reaction("❌")
        await asyncio.sleep(2)
        await ctx.message.delete()

    @commands.command()
    async def give(self, ctx, member: discord.Member = None, energy: int = None):
        """give energy points"""

        if member is None:
            return

        if energy is None:
            energy = 1

        with open("list.json", "r") as f:
            json_data = json.loads(f.read())
        playerrange = json_data[str(ctx.author.id)]["range"]
        playerx = json_data[str(ctx.author.id)]["cordinates"][0]
        playery = json_data[str(ctx.author.id)]["cordinates"][1]
        tarx = json_data[str(member.id)]["cordinates"][0]
        tary = json_data[str(member.id)]["cordinates"][1]
        if inrange(playerx, playery, tarx, tary, playerrange):
            print(f"Gave {energy} to {member.name}")
            json_data[str(ctx.author.id)]["energy"] -= energy
            json_data[str(member.id)]["energy"] += energy
            with open("list.json", "w") as f:
                new_json = json.dumps(json_data, indent=4)
                f.write(new_json)

            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
            await ctx.message.add_reaction("✅")
            await asyncio.sleep(2)
            await ctx.message.delete()
            return

        await ctx.message.add_reaction("❌")
        await asyncio.sleep(2)
        await ctx.message.delete()

    @commands.command()
    async def join(self, ctx, emoji: str = None):
        """join to game"""

        if (emoji is None):
            emoji = "📦"

        with open("list.json", "r") as f:
            json_data = json.loads(f.read())

        json_data[ctx.author.id] = {"emoji": emoji, "cordinates": [
            random.randrange(12), random.randrange(12)], "range": 2, "life": 3, "energy": 3}
        new_json = json.dumps(json_data, indent=4)

        with open("list.json", "w") as f:
            new_json = json.dumps(json_data, indent=4)
            f.write(new_json)

        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(ctx.channel.id)
            msg = await channel.fetch_message(f.read())

        await msg.edit(content=fillscreen())
        await ctx.message.delete()

    @commands.command()
    async def nS(self, ctx):
        """Creates a new screen"""

        screen = await ctx.send(fillscreen())
        f = open("viewmessage.txt", "w+")
        f.write(str(screen.id))
        f.close()
        await ctx.message.delete()

    @commands.command()
    async def rS(self, ctx):
        """refreshes screen"""

        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(ctx.channel.id)
            msg = await channel.fetch_message(f.read())

        await msg.edit(content=fillscreen())
        await ctx.message.delete()

    @commands.command()
    async def left(self, ctx):

        move(-1, 0, ctx.author.id)

        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(ctx.channel.id)
            msg = await channel.fetch_message(f.read())
        await msg.edit(content=fillscreen())
        await ctx.message.delete()

    @commands.command()
    async def right(self, ctx):

        move(1, 0, ctx.author.id)

        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(ctx.channel.id)
            msg = await channel.fetch_message(f.read())
        await msg.edit(content=fillscreen())
        await ctx.message.delete()

    @commands.command()
    async def up(self, ctx):

        move(0, -1, ctx.author.id)

        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(ctx.channel.id)
            msg = await channel.fetch_message(f.read())
        await msg.edit(content=fillscreen())
        await ctx.message.delete()

    @commands.command()
    async def down(self, ctx):

        move(0, 1, ctx.author.id)

        with open("viewmessage.txt", "r+") as f:
            channel = bot.get_channel(ctx.channel.id)
            msg = await channel.fetch_message(f.read())
        await msg.edit(content=fillscreen())
        await ctx.message.delete()

    @commands.command()
    async def bC(self, ctx):
        """creates button"""

        leftb = Button(label="", style=discord.ButtonStyle.grey, emoji="⬅️")
        rightb = Button(label="", style=discord.ButtonStyle.grey, emoji="➡️")
        upb = Button(label="", style=discord.ButtonStyle.grey, emoji="⬆️")
        downb = Button(label="", style=discord.ButtonStyle.grey, emoji="⬇️")
        upleftb = Button(label="", style=discord.ButtonStyle.grey, emoji="↖️")
        uprightb = Button(label="", style=discord.ButtonStyle.grey, emoji="↗️")
        downleftb = Button(
            label="", style=discord.ButtonStyle.grey, emoji="↙️")
        downrightb = Button(
            label="", style=discord.ButtonStyle.grey, emoji="↘️")
        button = Button(label="", style=discord.ButtonStyle.grey, emoji="🟦")

        async def left(interaction):
            move(-1, 0, interaction.user.id)
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
           # await interaction.response.send_message('left')

        async def right(interaction):
            move(1, 0, interaction.user.id)
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
           # await interaction.response.send_message('left')

        async def up(interaction):
            move(0, -1, interaction.user.id)
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
           # await interaction.response.send_message('left')

        async def down(interaction):
            move(0, 1, interaction.user.id)
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
           # await interaction.response.send_message('left')

        async def upleft(interaction):
            move(-1, -1, interaction.user.id)
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
           # await interaction.response.send_message('left')

        async def upright(interaction):
            move(1, -1, interaction.user.id)
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
           # await interaction.response.send_message('left')

        async def downleft(interaction):
            move(-1, 1, interaction.user.id)
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
           # await interaction.response.send_message('left')

        async def downright(interaction):
            move(1, 1, interaction.user.id)
            with open("viewmessage.txt", "r+") as f:
                channel = bot.get_channel(ctx.channel.id)
                msg = await channel.fetch_message(f.read())

            await msg.edit(content=fillscreen())
           # await interaction.response.send_message('left')

        leftb.callback = left
        rightb.callback = right
        upb.callback = up
        downb.callback = down
        upleftb.callback = upleft
        uprightb.callback = upright
        downrightb.callback = downright
        downleftb.callback = downleft

        upview = View()
        midview = View()
        downview = View()

        upview.add_item(upleftb)
        upview.add_item(upb)
        upview.add_item(uprightb)

        midview.add_item(leftb)
        midview.add_item(button)
        midview.add_item(rightb)

        downview.add_item(downleftb)
        downview.add_item(downb)
        downview.add_item(downrightb)

        await ctx.send("", view=upview)
        await ctx.send("", view=midview)
        await ctx.send("", view=downview)
        await ctx.message.delete()


intents = discord.Intents.default()
intents.message_content = True

bot.run(token)
