import disnake
from disnake import ApplicationCommandInteraction, ButtonStyle, Forbidden
from disnake.ui import button, Button
from disnake.ext.commands import InteractionBot
from disnake.ext import commands
from utility.database import Database
from math import ceil

bot = InteractionBot(test_guilds=[1047887307853795369])
categories = ["관리", "뮤직", "전적", "게임", "도박", "로깅", "빗금 명령어", "웹 대시보드", "밈", "레벨링", "유틸리티", "대화", "NSFW", "검색", "학교", "코로나19", "번역", "오버워치", "리그오브레전드", "배틀그라운드", "마인크래프트"]
with open('token.txt', 'r') as f:
    token = f.read()

db = Database("data/info.sql3")

def botlist_once(categories2: list[str]):
    inf = list(map(list, db.selectBotList(categories[0])))
    for i in inf:
        i[3] = i[3].split("_")
    for i in categories2:
        somelist = []
        for i2 in inf:
            if i2[3].__contains__(i):
                somelist.append(i2)
        inf = somelist
    return inf

class DbWrapperBot:
    def __init__(self, botid: int):
        inf = db.selectBotInfo(botid)
        if inf is not None and len(inf) != 0:
            inf = list(inf[0])
            inf[3] = inf[3].split("_")
            self.exist = True
            self.botid = botid
            self.name = inf[1]
            self.votes = int(inf[2])
            self.categories = inf[3]
            self.owners = inf[7].split("_")
            self.lib = inf[9]
            self.prefix = inf[10]
            self.servers = int(inf[11])
            if inf[12] is not None and inf[12] != "None":
                self.shards = int(inf[12])
            else:
                self.shards = 1
            self.oneline = inf[13]
            self.web = inf[15]
            self.git = inf[16]
            self.durl = inf[17]
            self.discord = f"https://discord.com/invite/{inf[18]}"
            self.created_at = inf[22]
        else:
            self.exist = False

class disnake_button(disnake.ui.Button):
    def __init__(self, inter: ApplicationCommandInteraction | disnake.ModalInteraction, values: list, pos: str):
        if pos == "left":
            _label = "<-"
        else:
            _label = "->"
        
        self.pos = pos
        self.n = 0
        self.values = values
        self.interaction = inter

        super().__init__(label=_label, style=ButtonStyle.primary)

    async def callback(self, inter: disnake.MessageInteraction):
        if self.pos == "left":
            _nplus = -1
            _ncompare = 0
        else:
            _nplus = 1
            _ncompare = len(self.values)-1
        
        if inter.author == self.interaction.author:
            if self.pos == "left":
                _cond = self.n <= _ncompare
            else:
                _cond = self.n > _ncompare
            if _cond:
                await inter.response.send_message("더 이상 페이지가 없습니다.", ephemeral=True)
            else:
                self.n += _nplus
                await inter.response.edit_message("", view=disnake_view([self.values[self.n]]))
        else:
            await inter.response.send_message("당신은 명령어를 사용한 사람이 아닙니다.", ephemeral=True)

class disnake_buttons2(disnake.ui.View):
    def __init__(self, bot: DbWrapperBot):
        super().__init__(timeout=60)
        self.n = 0
        self.bot = bot
    
    @button(label="invite", style=ButtonStyle.secondary)
    async def invite_button(self, button: Button, inter: disnake.MessageInteraction):
        await inter.send(f"초대 링크: {self.bot.durl}", ephemeral=True)
    
    @button(label="info", style=ButtonStyle.primary)
    async def info_button(self, button: Button, inter: disnake.MessageInteraction):
        await inter.send(f"봇의 정보: https://koreanbots.dev/bots/{self.bot.botid}", ephemeral=True)
    
    @button(label="kick", style=ButtonStyle.danger)
    async def kick_button(self, button: Button, inter: disnake.MessageInteraction):
        botobj = inter.guild.get_member(self.bot.botid)
        if botobj is not None:
            try:
                await inter.guild.kick(botobj)
            except Forbidden:
                await inter.send("봇이 권한을 가지고 있는 것 같지 않습니다.", ephemeral=True)
            else:
                await inter.send("킥에 성공하였습니다.", ephemeral=True)
        elif inter.author.guild_permissions.kick_members is False:
            await inter.send("당신은 킥할 권한이 없습니다.", ephemeral=True)
        else:
            await inter.send("봇이 이 서버에 없습니다.", ephemeral=True)

class disnake_selectmenu(disnake.ui.StringSelect):
    def __init__(self, inter: ApplicationCommandInteraction | disnake.ModalInteraction):
        self.interaction = inter
        options = []
        for i in categories:
            options.append(disnake.SelectOption(label=i))

        super().__init__(
            placeholder="카테고리를 선택하세요.",
            min_values=1,
            max_values=len(options),
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author != self.interaction.author:
            await inter.send("당신은 명령어를 사용한 사람이 아닙니다.", ephemeral=True)
            return
        labels = self._selected_values
        result = botlist_once(labels)
        values = []
        if len(result) > 0:
            for n, i in enumerate(result):
                valuesa = {"name": "", "vote": "", "id": "", "desc": ""}
                valuesa["name"] = i[1]
                valuesa["vote"] = str(i[2])
                valuesa["id"] = i[0]
                valuesa["desc"] = i[13]
                values.append(valuesa)
            del valuesa
            del n
            smenus = []
            _values = []
            for n, i in enumerate(values):
                if (n+1) % 25 == 0:
                    smenus.append(disnake_selectmenu2(title=f"페이지: {ceil((n+1) / 25)}/{ceil(len(values) / 25)}", values=_values, inter=self.interaction))
                    _values = []    
                _values.append(disnake.SelectOption(label=i["name"], value=i["id"], description=f"투표 수: {i['vote']}, 설명: {i['desc']}"))
            if len(_values) != 0:
                smenus.append(disnake_selectmenu2(title=f"페이지: {ceil((n+1) / 25)}/{ceil(len(values) / 25)}", values=_values, inter=self.interaction))
            del _values
            del n    
            await inter.message.edit("", view=disnake_view([smenus[0], disnake_button(self.interaction, smenus, "left"), disnake_button(self.interaction, smenus, "right")]))
        else:
            await inter.message.edit("그런 카테고리의 봇은 존재하지 않습니다.", view=None)

class disnake_selectmenu2(disnake.ui.StringSelect):
    def __init__(self, inter: ApplicationCommandInteraction | disnake.ModalInteraction, values: list, title: str):
        self.interaction = inter

        super().__init__(
            placeholder=title,
            min_values=1,
            max_values=1,
            options=values
        )
        
    
    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author != self.interaction.author:
            await inter.send("당신은 명령어를 사용한 사람이 아닙니다.", ephemeral=True)
            return
        await inter.send(self._selected_values[0], ephemeral=True)

class disnake_modal(disnake.ui.Modal):
    def __init__(self):
        components = [disnake.ui.TextInput(label="search", placeholder="검색할 이름을 입력해주세요.", custom_id="search", max_length=30)]
        super().__init__(title="검색", custom_id="search_modal", components=components)
    
    async def callback(self, inter: disnake.ModalInteraction):
        _result = botlist_once([])
        result = []
        for i in _result:
            if (i[1]).replace(' ', '').lower().__contains__(inter.text_values["search"].replace(' ', '').lower()):
                result.append(i)
        values = []
        valuesa = {"name": [], "vote": [], "id": []}
        if len(result) > 0:
            for n, i in enumerate(result):
                valuesa = {"name": "", "vote": "", "id": "", "desc": ""}
                valuesa["name"] = i[1]
                valuesa["vote"] = str(i[2])
                valuesa["id"] = i[0]
                valuesa["desc"] = i[13]
                values.append(valuesa)
            del valuesa
            del n
            smenus = []
            _values = []
            for n, i in enumerate(values):
                if (n+1) % 25 == 0:
                    smenus.append(disnake_selectmenu2(title=f"페이지: {ceil((n+1) / 25)}/{ceil(len(values) / 25)}", values=_values, inter=inter))
                    _values = []    
                _values.append(disnake.SelectOption(label=i["name"], value=i["id"], description=f"투표 수: {i['vote']}, 설명: {i['desc']}"))
            if len(_values) != 0:
                smenus.append(disnake_selectmenu2(title=f"페이지: {ceil((n+1) / 25)}/{ceil(len(values) / 25)}", values=_values, inter=inter))
            del _values
            del n    
            await inter.send("", view=disnake_view([smenus[0], disnake_button(inter, smenus, "left"), disnake_button(inter, smenus, "right")]))
        else:
            await inter.send("검색 결과가 없습니다.")

class disnake_view(disnake.ui.View):
    def __init__(self, views: list):
        super().__init__()

        for i in views:
            self.add_item(i)

@bot.slash_command(name="search", description="봇을 검색 할 수 있습니다.")
async def disnake_list(inter: ApplicationCommandInteraction, by = commands.Param(choices = ["category", "name"], description="봇을 이름이나 카테고리로 검색하세요.")):
    if by == "category":
        view = disnake_view([disnake_selectmenu(inter)])
        await inter.send(view=view)
    else:
        view = disnake_modal()
        await inter.response.send_modal(view)

@bot.slash_command(name="info", description="봇의 세부적인 정보를 알 수 있습니다.")
async def disnake_info(inter: ApplicationCommandInteraction, botid: str = commands.Param(description="봇의 아이디입니다. 무조건 정수여야 합니다.")):
    try:
        botid = int(botid)
    except ValueError:
        await inter.send("아이디가 정수가 아닌 것 같습니다.", ephemeral=True)
    else:
        bot = DbWrapperBot(botid)
        if bot.exist is False:
            await inter.send("이 아이디를 가진 봇이 없는 것 같습니다.", ephemeral=True)
        else:
            await inter.send("정보를 가져오는 중..")
            embed = disnake.Embed(title=bot.name, description=bot.oneline)
            embed.add_field(name="제작자", value=', '.join(bot.owners))
            embed.add_field(name="접두사", value=bot.prefix)
            embed.add_field(name="웹페이지", value=bot.web)
            embed.add_field(name="카테고리", value=', '.join(bot.categories))
            embed.add_field(name="투표 수", value=bot.votes) 
            embed.add_field(name="샤드 수", value=bot.shards)
            embed.add_field(name="서버 수", value=bot.servers)
            embed.add_field(name="만들어진 날짜", value=bot.created_at)
            embed.add_field(name="git url", value=bot.git)
            embed.add_field(name="라이브러리", value=bot.lib)
            await inter.edit_original_message("", embed=embed, view=disnake_buttons2(bot))

bot.run(token)
