import requests
import time

class BotInfo:
    def __init__(self,key_file_path):
        self.key_file_path = key_file_path
        self.korean_bot_base_url = "https://koreanbots.dev/api/v2"
        self.korean_bot_rate_limit = 180
        self.korean_bot_rate_reset = 0
    
    def getKoreanBotByHeartRankList(self,page_no):
        url = self.korean_bot_base_url+"/list/bots/votes"
        parameters = {"page":page_no}
        self.checkKoreanbotRateLimit()
        response = requests.request("GET", url, params=parameters)
        self.saveKoreanbotRateLimit(response.headers)
        if(response is not None):
            return response.json()
        else:
            print ("ERROR(getKoreanBotByHeartRankList) : response is none of %s" % page_no)
        return None

    def getKoreaBotByNewList(self,page_no):
        url = self.korean_bot_base_url+"/list/bots/new"
        parameters = {"page":page_no}
        self.checkKoreanbotRateLimit()
        response = requests.request("GET", url, params=parameters)
        self.saveKoreanbotRateLimit(response.headers)

        if(response is not None):
            return response.json()
        else:
            print ("ERROR(getKoreaBotByNewList) : response is none of %s" % page_no)
        return None

    def getKoreanBotInfo(self,bot_id=""):
        url = self.korean_bot_base_url+"/bots/"+bot_id
        if (bot_id is None or bot_id == ""):
            print("ERROR(getKoreanBotInfo) : bot_id is None")
            return None
        self.checkKoreanbotRateLimit()
        response = requests.request("GET", url)
        self.saveKoreanbotRateLimit(response.headers)

        if(response is not None):
            return response.json()
        else:
            print ("ERROR(getKoreanBotInfo) : response is none of %s" % bot_id)
        return None

    def saveKoreanbotRateLimit(self,headers):
        self.korean_bot_rate_limit = int(headers['X-RateLimit-Remaining'])
        self.korean_bot_rate_reset = int(headers['X-RateLimit-Reset'])
        print("LIMIT: %s in %s(s)" % (self.korean_bot_rate_limit, self.korean_bot_rate_reset))

    def checkKoreanbotRateLimit(self):
        if (self.korean_bot_rate_limit < 175):
            time.sleep(self.korean_bot_rate_reset-round(time.time()))

if __name__ == "__main__":
    print("main")
    botinfo = BotInfo("/")
    korean_bot_list=botinfo.getKoreanBotByHeartRankList(1)['data']['data']
    for no in range(len(korean_bot_list)):
        print("%s %s %s %s" % (korean_bot_list[no]['id'],korean_bot_list[no]['name'],korean_bot_list[no]['votes'],korean_bot_list[no]['category']))