from utility.botinfo import BotInfo
from utility.database import Database
from sys import argv

if __name__ == "__main__":
    try:
        argv[1]
    except IndexError:
        argv.append(1)
    botinfo = BotInfo("conf/botinfo.cnf")
    database = Database("data/info.sql3")
    rank_json = botinfo.getKoreanBotByHeartRankList(argv[1])
    rank_list = rank_json['data']['data']
    for no in range(len(rank_list)):
        is_exist_count = len(database.selectBotInfo(rank_list[no]['id']))
        if (is_exist_count == 0):
            database.insertKoreanBotInfo(rank_list[no])
    bot_list = database.selectBotList("뮤직")
    print(bot_list)

    multi_list = database.selectBotListByMultiCategory(["뮤직","유틸리티"])
    print(multi_list)
    database.close()