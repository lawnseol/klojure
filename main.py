import disnake
from disnake.ui import button, Button
from disnake import ApplicationCommandInteraction, ButtonStyle
from disnake.ext.commands import InteractionBot
from utility.database import Database

bot = InteractionBot(test_guilds=[1047887307853795369])
categories = ["관리", "뮤직", "전적", "게임", "도박", "로깅", "빗금 명령어", "웹 대시보드", "밈", "레벨링", "유틸리티", "대화", "NSFW", "검색", "학교", "코로나19", "번역", "오버워치", "리그오브레전드", "배틀그라운드", "마인크래프트"]
with open('token.txt', 'r') as f:
    token = f.read()

def botlist_once(categories2: list[str]):
    db = Database("data/info.sql3")
    inf = list(map(list, db.selectBotList(categories[0])))
    for i in inf:
        i[3] = i[3].split("_")
    for i in categories2:
        somelist = []
        for i2 in inf:
            if i2[3].__contains__(i):
                somelist.append(i2)
        inf = somelist
    db.close()
    return inf

class DbWrapperBot:
    def __init__(self, botid: int):
        #ID,NAME,VOTES,CATEGORIES,BOT_TYPE,TAG,AVATAR,OWNERS,FLAGS,LIB,PREFIX,SERVERS,SHARDS,INTRO,DESC,WEB,GIT,URL,DISCORD,VANITY,BG,BANNER,CREATED_AT
        db = Database('data/info.sql3')
        inf = db.selectBotInfo(botid)
        db.close()
        inf = list(inf[0])
        inf[3] = inf[3].split("_")
        if inf is not None:
            self.exist = True
            self.botid = botid
            self.name = inf[1]
            self.votes = int(inf[2])
            self.categories = inf[3]
            self.owners = inf[7]
            self.lib = inf[9]
            self.prefix = inf[10]
            self.servers = int(inf[11])
            self.shards = int(inf[12])
            self.oneline = inf[13]
            self.web = inf[15]
            self.git = inf[16]
            self.durl = inf[17]
            self.discord = f"https://discord.com/invite/{inf[18]}"
            self.created_at = inf[22]
        else:
            self.exist = False

class disnake_buttons(disnake.ui.View):
    def __init__(self, values: list):
        super().__init__(timeout=None)
        self.n = 0
        self.values = values
    
    @button(label="<-", style=ButtonStyle.grey, custom_id="left")
    async def left_button(self, button: Button, inter: disnake.MessageInteraction):
        if self.n <= 0:
            await inter.response.send_message("no more page", ephemeral=True)
        else:
            self.n -= 1
            await inter.response.edit_message("", embed=self.values[self.n])
    
    @button(label="->", style=ButtonStyle.grey, custom_id="right")
    async def right_button(self, button: Button, inter: disnake.MessageInteraction):
        if self.n >= len(self.values)-1:
            await inter.response.send_message("no more page", ephemeral=True)
        else:
            self.n += 1
            await inter.response.edit_message("", embed=self.values[self.n])

class disnake_buttons2(disnake.ui.View):
    def __init__(self, bot: DbWrapperBot):
        super().__init__(timeout=60)
        self.n = 0
        self.bot = bot
    
    @button(label="invite", style=ButtonStyle.secondary)
    async def invite_button(self, button: Button, inter: disnake.MessageInteraction):
        await inter.send(f"Invite url: {self.bot.durl}", ephemeral=True)
    
    @button(label="info", style=ButtonStyle.primary)
    async def info_button(self, button: Button, inter: disnake.MessageInteraction):
        await inter.send(f"Url: https://koreanbots.dev/bots/{self.bot.botid}", ephemeral=True)
    
    @button(label="kick", style=ButtonStyle.danger)
    async def kick_button(self, button: Button, inter: disnake.MessageInteraction):
        botobj = await inter.guild.get_member(self.bot.botid)
        if botobj is not None:
            await inter.guild.kick(botobj)
            await inter.send("kicked", ephemeral=True)
        else:
            await inter.send("that bot isn't invited", ephemeral=True)

class disnake_selectmenu(disnake.ui.StringSelect):
    def __init__(self):
        options = []
        for i in categories:
            options.append(disnake.SelectOption(label=i))

        super().__init__(
            placeholder="Choose category",
            min_values=1,
            max_values=len(options),
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        labels = self._selected_values
        result = botlist_once(labels)
        values = []
        valuesa = {"name": [], "vote": [], "id": []}
        if len(result) > 0:
            for n, i in enumerate(result):
                if n != 0 and n % 10 == 0:
                    values.append(valuesa)
                    valuesa = {"name": [], "vote": [], "id": []}
                valuesa["name"].append(i[1])
                valuesa["vote"].append(str(i[2]))
                valuesa["id"].append(i[0])
            values.append(valuesa)
            del valuesa
            del n
            embeds = []
            for n, i in enumerate(values):
                embed = disnake.Embed(title=f"page: {n+1}/{len(values)}")
                embed.add_field(name="name", value="\n".join(i["name"]))
                embed.add_field(name="vote", value="\n".join(i["vote"]))
                embed.add_field(name="id", value="\n".join(i["id"]))
                embeds.append(embed)
            await inter.message.edit("", embed=embeds[0], view=disnake_buttons(embeds))
        else:
            await inter.message.edit("그런 카테고리의 봇은 존재하지 않습니다.", view=None)

class disnake_view(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(disnake_selectmenu())

@bot.slash_command(name="list", description="bot list")
async def disnake_list(inter: ApplicationCommandInteraction):
    view = disnake_view()
    await inter.send("select category", view=view)

@bot.slash_command(name="info", description="bot info")
async def disnake_info(inter: ApplicationCommandInteraction, botid: str):
    try:
        botid = int(botid)
    except ValueError:
        await inter.send("no int")
    else:
        bot = DbWrapperBot(botid)
        if bot.exist is False:
            await inter.send("no bot that has id")
        else:
            await inter.send("fetching some information")
            embed = disnake.Embed(title=bot.name, description=bot.oneline)
            embed.add_field(name="owner", value=bot.owners)
            embed.add_field(name="prefix", value=bot.prefix)
            embed.add_field(name="web", value=bot.web)
            embed.add_field(name="categories", value=', '.join(bot.categories))
            embed.add_field(name="votes", value=bot.votes) 
            embed.add_field(name="shards", value=bot.shards)
            embed.add_field(name="servers", value=bot.servers)
            embed.add_field(name="created at", value=bot.created_at)
            embed.add_field(name="git url", value=bot.git)
            embed.add_field(name="library", value=bot.lib)
            await inter.send(embed=embed, view=disnake_buttons2(bot))

bot.run(token)
