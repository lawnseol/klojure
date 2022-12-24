import disnake
from disnake.ui import button, Button
from disnake import ApplicationCommandInteraction, SelectMenu, ButtonStyle
from disnake.ext.commands import Bot

bot = Bot(test_guilds=[1047887307853795369])
categories = ["관리", "뮤직", "전적", "게임", "도박", "로깅", "빗금 명령어", "웹 대시보드", "밈", "레벨링", "유틸리티", "대화", "NSFW", "검색", "학교", "코로나19", "번역", "오버워치", "리그오브레전드", "배틀그라운드", "마인크래프트"]
with open('token.txt', 'r') as f:
    token = f.read()

class disnake_buttons(disnake.ui.View):
    def __init__(self, embeds: list):
        super().__init__(timeout=None)
        self.n = 0
        self.embeds = embeds
    
    @button(label="<-", style=ButtonStyle.grey, custom_id="left")
    async def left_button(self, button: Button, inter: disnake.MessageInteraction):
        if self.n <= 0:
            await inter.response.send_message("no more page", ephemeral=True)
        else:
            self.n -= 1
            await inter.response.edit_message("", embed=self.embeds[self.n])
    
    @button(label="->", style=ButtonStyle.grey, custom_id="right")
    async def right_button(self, button: Button, inter: disnake.MessageInteraction):
        if self.n >= len(self.embeds)-1:
            await inter.response.send_message("no more page", ephemeral=True)
        else:
            self.n += 1
            await inter.response.edit_message("", embed=self.embeds[self.n])

@bot.slash_command(name="list", description="bot list")
async def disnake_list(inter: ApplicationCommandInteraction):
    selmenu = SelectMenu(custom_id="selmenu", max_values=len(categories))
    for i in categories:
        selmenu.add_option(label=i, value=i)
    msg: disnake.Message = await inter.send("select category", components=[selmenu])
    #row = ActionRow(Button(style=ButtonStyle.gray, label="<-", custom_id="left"), Button(style=ButtonStyle.gray, label="->", custom_id="right"))
    intera = await msg.wait_for_dropdown()
    labels = [option.label for option in intera.select_menu.selected_options]
    #search from db and get by classes in list
    result = []
    embeds = []
    embed = disnake.Embed(title="bot list", description="bot list desc")
    n = 0
    for i in result:
        if n+1 % 6 == 0:
            embeds.append(embed)
            embed = disnake.Embed(title="bot list", description="bot list desc")
        embed.add_field(name=i, value="vote: test, categories: [test, test], id: test")
        n += 1
    msg.edit("", embed=embeds[0], components=disnake_buttons(embeds))

#@bot.slash_command(name="info", description="bot info")
#async def disnake_info(inter: ApplicationCommandInteraction, botid: int):
    # search int and get to class
    #await inter.send()

bot.run(token)
