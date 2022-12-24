import sqlite3
import datetime

class Database:
    def __init__(self,sql_file_path):
        self.sql_file_path = sql_file_path
        self.connect()
        self.init()

    def connect(self):
        self.con = sqlite3.connect(self.sql_file_path)
        self.curs = self.con.cursor()

    def init(self):
        self.curs.execute("CREATE TABLE IF NOT EXISTS BOTS (ID TEXT, NAME TEXT, VOTES INTEGER, CATEGORIES TEXT, BOT_TYPE TEXT, CREATED_AT TEXT, UNIQUE (ID, BOT_TYPE))")
        self.curs.execute("CREATE INDEX IF NOT EXISTS IDX_BOTS_01 ON BOTS(ID,BOT_TYPE)")
        self.con.commit()

    def insertKoreanBotInfo(self,info,bot_type="KOREANBOT"):
        now = datetime.datetime.now()
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")

        self.curs.execute("INSERT INTO BOTS (ID,NAME,VOTES,CATEGORIES,BOT_TYPE,CREATED_AT) VALUES ('%s', '%s', %s, '%s','%s', '%s')" % (info['id'],info['name'],info['votes'],'_'.join(info['category']),bot_type,created_at))
        self.con.commit()

    def selectBotList(self,category_name,bot_type=""):
        self.curs.execute("SELECT ID, NAME, VOTES, CATEGORIES, BOT_TYPE FROM BOTS WHERE CATEGORIES LIKE ('%%%s%%')" % category_name)
        result = self.curs.fetchall()
        self.con.commit()
        return result


    def selectBotInfo(self,bot_id,bot_type="KOREANBOT"):
        self.curs.execute("SELECT ID, NAME, VOTES, CATEGORIES, BOT_TYPE FROM BOTS WHERE ID = '%s' AND BOT_TYPE = '%s'" % (bot_id, bot_type))
        result = self.curs.fetchall()
        self.con.commit()
        return result
    
    def close(self):
        self.curs.close()
        self.con.close()
        self.curs = None
        self.con = None