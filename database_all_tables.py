import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cur = self.conn.cursor()

    async def create_tables(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tags("
            "id SERIAL PRIMARY KEY,"
            "tag VARCHAR)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fandoms("
            "id SERIAL PRIMARY KEY,"
            "fandom VARCHAR UNIQUE)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS pairings("
            "id SERIAL PRIMARY KEY,"
            "pairing VARCHAR,"
            "fandom_id INTEGER REFERENCES fandoms(id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users("
            "id SERIAL PRIMARY KEY,"
            "chat_id INTEGER UNIQUE,"
            "username VARCHAR)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS authors("
            "id SERIAL PRIMARY KEY,"
            "chat_id INTEGER UNIQUE,"
            "username VARCHAR)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_tags("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "tag_id INTEGER REFERENCES tags(id),"
            "PRIMARY KEY(chat_id, tag_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_fandoms("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "fandom_id INTEGER REFERENCES fandoms(id),"
            "PRIMARY KEY(chat_id, fandom_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_pairings("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "pairing_id INTEGER REFERENCES pairings(id),"
            "PRIMARY KEY(chat_id, pairing_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction("
            "id SERIAL PRIMARY KEY,"
            "title VARCHAR,"
            "rating VARCHAR,"
            "status VARCHAR,"
            "author_id INT REFERENCES authors(id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_tags("
            "fanfic_id INT REFERENCES fanfiction(id),"
            "tag_id INT REFERENCES tags(id),"
            "PRIMARY KEY(fanfic_id, tag_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_pairings("
            "fanfic_id INT REFERENCES fanfiction(id),"
            "pairing_id INT REFERENCES pairings(id),"
            "PRIMARY KEY(fanfic_id, pairing_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_fandoms("
            "fanfic_id INT REFERENCES fanfiction(id),"
            "fandom_id INT REFERENCES fandoms(id),"
            "PRIMARY KEY(fanfic_id, fandom_id))")
        self.conn.commit()
        self.cur.close()


class Tags:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cur = self.conn.cursor()

    async def add_tag(self, tag_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO tags(tag) VALUES ('{tag_name}')")
        self.conn.commit()
        self.cur.close()

    async def get_tag_id(self, tag_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM tags WHERE tag = %s", (tag_name,))
        tag_id = self.cur.fetchone()
        self.cur.close()
        return tag_id[0]

    async def get_all_tags(self):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT tag FROM tags")
        result = self.cur.fetchall()
        self.cur.close()
        return result


class Fandoms:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cur = self.conn.cursor()

    async def add_fandom(self, fandom_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO fandoms(fandom) VALUES ('{fandom_name}')")
        self.conn.commit()
        self.cur.close()

    async def get_fandom_id(self, fandom_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM fandoms WHERE fandom = %s", (fandom_name,))
        fandom_id = self.cur.fetchone()
        self.cur.close()
        return fandom_id[0]

    # async
    async def get_all_fandoms(self):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT fandom FROM fandoms")
        result = self.cur.fetchall()
        self.cur.close()
        return result


class Users:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cur = self.conn.cursor()

    async def add_users(self, chat_id, username):
        self.cur = self.conn.cursor()

        self.cur.execute(
            "SELECT COUNT(*) FROM users WHERE chat_id = %s",
            (chat_id,))
        user_count = self.cur.fetchone()[0]

        if user_count == 0:
            self.cur.execute(
                "INSERT INTO users (chat_id, username) VALUES (%s, %s)",
                (chat_id, username))
            self.conn.commit()

        self.cur.close()

    async def get_all_users_tags(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT tag_id FROM users_tags WHERE chat_id = %s", (chat_id,))
        result = self.cur.fetchall()
        self.cur.close()
        return result

    async def add_users_tags(self, chat_id, tag_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_tags (chat_id, tag_id) VALUES (%s, %s)",
            (chat_id, tag_id))
        self.conn.commit()
        self.cur.close()

    async def get_all_users_fandoms(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT fandom_id FROM users_fandoms WHERE chat_id = %s", (chat_id,))
        result = self.cur.fetchall()
        self.cur.close()
        return result

    async def add_users_fandoms(self, chat_id, fandom_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_fandoms (chat_id, fandom_id) VALUES (%s, %s)",
            (chat_id, fandom_id))
        self.conn.commit()
        self.cur.close()
