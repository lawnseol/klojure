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
        if self.n >= len(self.embeds)-1:
            await inter.response.send_message("no more page", ephemeral=True)
        else:
            self.n += 1
            await inter.response.edit_message("", embed=self.values[self.n])

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
        n = 0
        if len(result) > 0:
            for i in result:
                if n+1 % 10 == 0:
                    n = 0
                    values.append(valuesa)
                    valuesa = {"name": [], "vote": [], "id": []}
                valuesa["name"].append(i[1])
                valuesa["vote"].append(str(i[2]))
                valuesa["id"].append(i[0])
                n += 1
            values.append(valuesa)
            del valuesa
            del n
            embeds = []
            for i in values:
                embed = disnake.Embed()
                embed.add_field(name="name", value="\n".join(i["name"]))
                embed.add_field(name="vote", value="\n".join(i["vote"]))
                embed.add_field(name="id", value="\n".join(i["id"]))
                embeds.append(embed)
            await inter.message.edit("", embed=embeds[0], view=disnake_buttons(values))
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

#@bot.slash_command(name="info", description="bot info")
#async def disnake_info(inter: ApplicationCommandInteraction, botid: int):
    # search int and get to class
    #await inter.send()

bot.run(token)
