from disnake import ActionRow, ApplicationCommandInteraction, Button, ButtonStyle
from disnake.ext.commands import Bot

bot = Bot(test_guilds=[1047887307853795369])
categories = ["관리", "뮤직", "전적", "게임", "도박", "로깅", "빗금 명령어", "웹 대시보드", "밈", "레벨링", "유틸리티", "대화", "NSFW", "검색", "학교", "코로나19", "번역", "오버워치", "리그오브레전드", "배틀그라운드", "마인크래프트"]
rowlist = []
rowtemp = []

for i, i2 in enumerate(categories):
    if i+1 % 6 == 0:
        rowlist.append(ActionRow(rowtemp))
        rowtemp = []
    rowtemp.append(Button(style=ButtonStyle.gray, label=i2, custom_id=i2))
if rowtemp != []:
    rowlist.append(ActionRow(rowtemp))
    rowtemp = []
del rowtemp

@bot.slash_command(name="list", description="bot list")
async def disnake_list(inter: ApplicationCommandInteraction):
    await inter.reply("select category", components=rowlist)
    row = ActionRow(Button(style=ButtonStyle.gray, label="<-", custom_id="left"), Button(style=ButtonStyle.gray, label="->", custom_id="right"))

bot.run("token")
