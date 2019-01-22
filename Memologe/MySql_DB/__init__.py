
import mysql.connector
from config import config
import time

class DB:
    def __init__(self) -> 'DB':
        self.mydb = mysql.connector.connect(
            host=config["db_host"],
            user=config["db_user"],
            passwd=config["db_pw"],
            database = "memes",
        )
        self.cursor = self.mydb.cursor()

        try:
            self.cursor.execute("CREATE TABLE memes( meme_id INTEGER ,link varchar(4096), tags varchar(512), ptime INTEGER , rating INTEGER )")
        except:
            print("Table memes already exists")

    def max_id(self):

        self.cursor.execute("SELECT MAX(meme_id) FROM memes;")

        res:list = self.cursor.fetchall()

        if res[0][0] is None:
            id:int = 0
        else:
            id:int = res[0][0]

        return id

    def add_meme(self, link:str,time:int, tags:str = "") -> None:

        id : int = self.max_id() + 1

        self.cursor.execute("INSERT INTO memes (meme_id, link, tags, ptime, rating) VALUES (%s, %s, %s, %s, %s)",(id,link,tags.lower(),time,0))

        self.mydb.commit()

    def add_tags_by_id(self, id: int, tags:str) -> None:

        self.cursor.execute( "UPDATE memes SET tags += '%s' WHERE meme_id = '%s'",(tags, id))

        self.mydb.commit()

    def search_meme(self, tags:str)->list:

        self.cursor.execute("SELECT * FROM memes WHERE tags LIKE '%" + tags + "%'")

        data = self.cursor.fetchall()

        print(data)

        return data

    def reset_db(self):

        self.cursor.execute("DELETE FROM memes")
        self.mydb.commit()

    def check_ex(self, link: str):
        print(link)
        self.cursor.execute("SELECT * FROM memes WHERE link = %s",(link,))

        data = self.cursor.fetchall()

        if data == []:
            return False
        return True

    def get_meme_by_id(self, id:int):
        self.cursor.execute("SELECT * FROM memes WHERE meme_id = %s",(id,))

        data = self.cursor.fetchall()
        print(data,id)


        return data[0]

    def size_of_db(self):
        self.cursor.execute("SELECT COUNT(*) FROM memes")
        data = self.cursor.fetchall()
        return data
