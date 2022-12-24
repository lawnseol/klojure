import sqlite3
from datetime import datetime

class Database:
    def __init__(self,sql_file_path):
        self.sql_file_path = sql_file_path
        self.connect()

    def connect(self):
        self.con = sqlite3.connect(self.sql_file_path)
        self.curs = self.con.cursor()

    def init(self):
        self.curs.execute("CREATE TABLE IF NOT EXISTS BOTS (ID INTEGER PRIMARY KEY, NAME TEXT, VOTES INTEGER, CATEGORIES TEXT, TYPE TEXT, CREATED_AT TEXT)")
        self.con.commit()

    def insertKoreanBotInfo(self,info,bot_type="KOREANBOT"):
        now = datetime.datetime.now()
        created_at = now.strftime("%Y-%m-%d %H:%M:%S")
        self.curs.execute("INSERT INTO BOTS (ID,NAME,VOTES,CATEGORIES,TYPE,CREATED_AT) VALUES (%i,%i,'%s','%s','%s')" % (info['id'],info['name'],info['votes'],info['category'],bot_type,created_at))
        self.con.commit()

    def selectBotList(self,category_name,bot_type=""):
        self.curs.execute("SELECT ID, NAME, VOTES, CATEGORIES, TYPE FROM BOTS WHERE CATEGORIES IN ('*%s*')" % category_name)
        return self.curs.fetchall()
    
    def close(self):
        self.curs.close()
        self.con.close()
        self.curs = None
        self.con = None