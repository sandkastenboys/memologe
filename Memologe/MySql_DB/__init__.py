from config import config
import time
import random
import pymysql

class DB:
    def __init__(self):
        self.mydb = pymysql.connect(
            host=config["db_host"],
            port=config["db_port"],
            user=config["db_user"],
            passwd=config["db_pw"],
            database="memes",
        )
        self.cursor = self.mydb.cursor()
        self.tags = []
        self.cursor.execute("SET GLOBAL connect_timeout=600")
        try:
            self.cursor.execute(
                "CREATE TABLE memes( meme_id INTEGER ,link varchar(4096), tags varchar(512), ptime INTEGER , rating INTEGER )")
        except:
            print("Table memes already exists")

        self.db2tags()

    def max_id(self):

        self.cursor.execute("SELECT MAX(meme_id) FROM memes;")

        res = self.cursor.fetchall()

        if res[0][0] is None:
            id = 0
        else:
            id = res[0][0]

        return id

    def add_meme(self, link, time, tags=""):

        id = self.max_id() + 1

        self.cursor.execute("INSERT INTO memes (meme_id, link, tags, ptime, rating) VALUES (%s, %s, %s, %s, %s)",
                            (id, link, tags.lower(), time, 0))

        self.mydb.commit()

    def add_tags_by_id(self, id, tags):

        self.cursor.execute("UPDATE memes SET tags = %s WHERE meme_id = %s", (tags, id))

        self.mydb.commit()

    def search_meme(self, tags):

        self.cursor.execute("SELECT * FROM memes WHERE tags LIKE '%" + tags + "%'")

        data = self.cursor.fetchall()

        print(data)

        return data

    def reset_db(self):

        self.cursor.execute("DELETE FROM memes")
        self.mydb.commit()

    def check_ex(self, link):
        print(link)
        self.cursor.execute("SELECT * FROM memes WHERE link = %s", (link,))

        data = self.cursor.fetchall()

        if data == []:
            return False
        return True

    def get_meme_by_id(self, id):
        self.cursor.execute("SELECT * FROM memes WHERE meme_id = %s", (id,))

        data = self.cursor.fetchall()
        print(data, id)

        return data[0]

    def size_of_db(self):
        self.cursor.execute("SELECT COUNT(*) FROM memes")
        data = self.cursor.fetchall()
        return data

    def get_memes_with_tags(self):
        self.cursor.execute("SELECT * FROM memes WHERE tags != ''")

        data = self.cursor.fetchall()

        return data

    def get_meme_id_by_link(self, link):
        self.cursor.execute("SELECT * FROM memes WHERE link = %s", (link,))

        data = self.cursor.fetchall()

        return data

    def get_recent(self, threshhold, max):

        return_list = []

        self.cursor.execute("SELECT * FROM memes WHERE ptime > %s;" ,(time.time()-threshhold,))

        data = self.cursor.fetchall()
        print(data)
        if len(data) < max:
            for x in data:
                return_list.append(x)
        else:
            for x in range(max):
                return_list.append(random.choice(data))

        return return_list

    def db2tags(self):

        memes = self.get_memes_with_tags()
        for meme in memes:

            for tag in meme[2].split(";"):

                if tag not in self.tags:
                    self.tags.append(tag)

        self.tags = sorted(self.tags)

    def add_tags(self,string):
        for mtag in string.split(";"):

            if mtag not in self.tags:
                self.tags.append(mtag)

        self.tags = sorted(self.tags)

db = DB()
