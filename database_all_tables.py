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
        try:
            self.conn = psycopg2.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD,
                port=PORT
            )
            self.cur = self.conn.cursor()
            print("Успешное подключение к базе данных PostgreSQL.")
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")

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
            "CREATE TABLE IF NOT EXISTS relationships("
            "id SERIAL PRIMARY KEY,"
            "relationship VARCHAR UNIQUE)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS pairings("
            "id SERIAL PRIMARY KEY,"
            "pairing VARCHAR,"
            "fandom_id INTEGER REFERENCES fandoms(id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS narrow_tags("
            "id SERIAL PRIMARY KEY,"
            "narrow_tag VARCHAR,"
            "tag_id INTEGER REFERENCES tags(id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users("
            "id SERIAL PRIMARY KEY,"
            "chat_id INTEGER UNIQUE,"
            "username VARCHAR,"
            "chosen_language VARCHAR)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS authors("
            "id SERIAL PRIMARY KEY,"
            "username VARCHAR)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_tags("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "tag_id INTEGER REFERENCES tags(id),"
            "PRIMARY KEY(chat_id, tag_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_narrow_tags("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "narrow_tag_id INTEGER REFERENCES narrow_tags(id),"
            "PRIMARY KEY(chat_id, narrow_tag_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_narrow_tags_disliked("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "narrow_tag_id INTEGER REFERENCES narrow_tags(id),"
            "PRIMARY KEY(chat_id, narrow_tag_id))")
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
            "CREATE TABLE IF NOT EXISTS users_relationships("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "relationship_id INTEGER REFERENCES relationships(id),"
            "PRIMARY KEY(chat_id, relationship_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_language("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "language_code VARCHAR,"
            "PRIMARY KEY(chat_id, language_code))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_preferences("
            "chat_id INTEGER REFERENCES users(chat_id),"
            "preference INTEGER,"
            "ff_id INTEGER REFERENCES fanfiction(id),"
            "PRIMARY KEY(chat_id, language_code, ff_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction("
            "id SERIAL PRIMARY KEY,"
            "title VARCHAR,"
            "rating VARCHAR,"
            "ff_size VARCHAR,"
            "status VARCHAR,"
            "link VARCHAR,"
            "description VARCHAR,"
            "author_id INT REFERENCES authors(id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_tags("
            "fanfic_id INT REFERENCES fanfiction(id),"
            "tag_id INT REFERENCES tags(id),"
            "PRIMARY KEY(fanfic_id, tag_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_narrow_tags("
            "fanfic_id INT REFERENCES fanfiction(id),"
            "narrow_tag_id INT REFERENCES narrow_tags(id),"
            "PRIMARY KEY(fanfic_id, narrow_tag_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_pairings("
            "fanfic_id INT REFERENCES fanfiction(id),"
            "pairing_id INT REFERENCES pairings(id),"
            "PRIMARY KEY(fanfic_id, pairing_id))")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_relationships("
            "fanfic_id INT REFERENCES fanfiction(id),"
            "relationship_id INT REFERENCES relationships(id),"
            "PRIMARY KEY(fanfic_id, relationship_id))")
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
        self.cur.execute("SELECT COUNT(*) FROM tags WHERE tag = %s", (tag_name,))
        count = self.cur.fetchone()[0]
        if count == 0:
            self.cur.execute(f"INSERT INTO tags(tag) VALUES ('{tag_name}')")
            self.conn.commit()
        self.cur.close()

    async def add_narrow_tag(self, narrow_tag: str, tag_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO narrow_tags(narrow_tag, tag_id) VALUES ('{narrow_tag}', {tag_id})")
        self.conn.commit()
        self.cur.close()

    async def get_tag_id(self, tag_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM tags WHERE tag = %s", (tag_name,))
        tag_id = self.cur.fetchone()
        self.cur.close()
        return tag_id[0]

    async def get_tag_id_by_narrow_tag(self, narrow_tag_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT tag_id FROM narrow_tags WHERE narrow_tag = %s", (narrow_tag_id,))
        tag_id = self.cur.fetchone()
        self.cur.close()
        return tag_id[0]

    async def get_narrow_tag_id(self, narrow_tag_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM narrow_tags WHERE narrow_tag = %s", (narrow_tag_name,))
        tag_id = self.cur.fetchone()
        self.cur.close()
        return tag_id[0]

    async def get_narrow_tag_name_by_id(self, narrow_tag_id: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT narrow_tag FROM narrow_tags WHERE id = %s", (narrow_tag_id,))
        narrow_tag = self.cur.fetchone()
        self.cur.close()
        return narrow_tag[0]

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
        self.cur.execute("SELECT COUNT(*) FROM fandoms WHERE fandom = %s", (fandom_name,))
        count = self.cur.fetchone()[0]
        if count == 0:
            self.cur.execute(f"INSERT INTO fandoms(fandom) VALUES ('{fandom_name}')")
            self.conn.commit()
        self.cur.close()

    async def get_fandom_id(self, fandom_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM fandoms WHERE fandom = %s", (fandom_name,))
        fandom_id = self.cur.fetchone()
        self.cur.close()
        return fandom_id[0]

    async def get_fandom_by_id(self, fandom_id: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT fandom FROM fandoms WHERE id = %s", (fandom_id,))
        fandom_name = self.cur.fetchone()
        self.cur.close()
        return fandom_name[0]

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

    async def add_users_tags(self, chat_id, tag_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_tags (chat_id, tag_id) VALUES (%s, %s)",
            (chat_id, tag_id))
        self.conn.commit()
        self.cur.close()

    async def add_users_fandoms(self, chat_id, fandom_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_fandoms (chat_id, fandom_id) VALUES (%s, %s)",
            (chat_id, fandom_id))
        self.conn.commit()
        self.cur.close()

    async def add_users_pairings(self, chat_id, pairing_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_pairings (chat_id, pairing_id) VALUES (%s, %s)",
            (chat_id, pairing_id))
        self.conn.commit()
        self.cur.close()

    async def add_users_relationships(self, chat_id, relationship_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_relationships (chat_id, relationship_id) VALUES (%s, %s)",
            (chat_id, relationship_id))
        self.conn.commit()
        self.cur.close()

    async def add_users_language(self, chat_id, language_code):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "SELECT COUNT(*) FROM users_language WHERE chat_id = %s",
            (chat_id,))
        user_count = self.cur.fetchone()[0]
        if user_count == 0:
            self.cur.execute(
                "INSERT INTO users_language (chat_id, language_code) VALUES (%s, %s)",
                (chat_id, language_code))
        else:
            self.cur.execute(
                "UPDATE users_language SET language_code = %s WHERE chat_id = %s",
                (language_code, chat_id))
        self.conn.commit()
        self.cur.close()

    async def add_users_preferences(self, chat_id, preferences, ff_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_language (chat_id, preferences, ff_id) VALUES (%s, %s, %s)",
            (chat_id, preferences, ff_id))
        self.conn.commit()
        self.cur.close()

    async def add_users_narrow_tags(self, chat_id, tg_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_narrow_tags (chat_id, narrow_tag_id) VALUES (%s, %s)",
            (chat_id, tg_id))
        self.conn.commit()
        self.cur.close()

    async def add_users_narrow_tags_disliked(self, chat_id, tg_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "INSERT INTO users_narrow_tags_disliked (chat_id, narrow_tag_id) VALUES (%s, %s)",
            (chat_id, tg_id))
        self.conn.commit()
        self.cur.close()

    async def delete_users_tags_by_chat_id(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"DELETE FROM users_tags WHERE chat_id = %s", (chat_id,))
        self.conn.commit()
        self.cur.close()

    async def delete_users_pairings_by_chat_id(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"DELETE FROM users_pairings WHERE chat_id = %s", (chat_id,))
        self.conn.commit()
        self.cur.close()

    async def delete_users_pairings_by_chat_id_fandom(self, fandom_id, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "DELETE FROM users_pairings "
            "WHERE pairing_id IN (SELECT id FROM pairings WHERE fandom_id = %s) "
            "AND chat_id = %s", (fandom_id, chat_id)
        )
        self.conn.commit()
        self.cur.close()

    async def delete_users_fandoms_by_chat_id(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"DELETE FROM users_fandoms WHERE chat_id = %s", (chat_id,))
        self.conn.commit()
        self.cur.close()

    async def delete_users_relationships_by_chat_id(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"DELETE FROM users_relationships WHERE chat_id = %s", (chat_id,))
        self.conn.commit()
        self.cur.close()

    async def get_all_users_fandoms(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT fandom_id FROM users_fandoms WHERE chat_id = %s", (chat_id,))
        result = self.cur.fetchall()
        self.cur.close()
        return result

    async def get_all_users_tags(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT tag_id FROM users_tags WHERE chat_id = %s", (chat_id,))
        result = self.cur.fetchall()
        self.cur.close()
        return result

    async def get_all_users_pairings(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT pairing_id FROM users_pairings WHERE chat_id = %s", (chat_id,))
        result = self.cur.fetchall()
        self.cur.close()
        return result

    async def get_all_users_relationships(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT relationship_id FROM users_relationships WHERE chat_id = %s", (chat_id,))
        result = self.cur.fetchall()
        self.cur.close()
        return result

    async def get_users_language(self, chat_id):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT language_code FROM users_language WHERE chat_id = %s", (chat_id,))
        result = self.cur.fetchall()
        if not result:
            return 'ru'
        self.cur.close()
        return result[0][0]


class Pairings:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cur = self.conn.cursor()

    async def add_pairing(self, pairing_name: str, fandom_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT COUNT(*) FROM pairings WHERE pairing = %s", (pairing_name,))
        count = self.cur.fetchone()[0]
        if count == 0:
            self.cur.execute(f"INSERT INTO pairings(pairing, fandom_id) VALUES ('{pairing_name}', {fandom_id})")
            self.conn.commit()
        self.cur.close()

    async def get_pairing_id(self, pairing_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM pairings WHERE pairing = %s", (pairing_name,))
        pairing_id = self.cur.fetchone()
        self.cur.close()
        return pairing_id[0]

    async def get_all_pairings(self):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT pairing FROM pairings")
        result = self.cur.fetchall()
        self.cur.close()
        return result

    async def get_pairings_by_fandom(self, fandom_id):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT pairing FROM pairings WHERE fandom_id = %s", (fandom_id,))
        pairings = self.cur.fetchall()
        self.cur.close()
        return pairings


class Relationships:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cur = self.conn.cursor()

    async def add_relationship(self, relationship_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT COUNT(*) FROM relationships WHERE relationship = %s", (relationship_name,))
        count = self.cur.fetchone()[0]
        if count == 0:
            self.cur.execute("INSERT INTO relationships(relationship) VALUES (%s)", (relationship_name,))
            self.conn.commit()
        self.cur.close()

    async def get_all_relationships(self):
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT relationship FROM relationships")
        result = self.cur.fetchall()
        self.cur.close()
        return result

    async def get_relationship_id(self, relationship_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM relationships WHERE relationship = %s", (relationship_name,))
        relationship_id = self.cur.fetchone()
        self.cur.close()
        return relationship_id[0]


class Fanfiction:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cur = self.conn.cursor()

    async def add_fanfiction(self, title: str, rating: str, size: str,
                             status: str, link: str, description: str, author: int):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT COUNT(*) FROM fanfiction WHERE title = %s", (title,))
        count = self.cur.fetchone()[0]
        if count == 0:
            self.cur.execute("INSERT INTO fanfiction(title, rating, ff_size, status, link, description, author_id) "
                             f"VALUES ('{title}', '{rating}', '{size}', '{status}', '{link}', '{description}', {author})")
            self.conn.commit()
        self.cur.close()

    async def add_fanfiction_relationship(self, fanfic_id: int, relationship_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO fanfiction_relationships(fanfic_id, relationship_id) "
                         f"VALUES ({fanfic_id}, {relationship_id})")
        self.conn.commit()
        self.cur.close()

    async def add_fanfiction_fandom(self, fanfic_id: int, fandom_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO fanfiction_fandoms(fanfic_id, fandom_id) "
                         f"VALUES ({fanfic_id}, {fandom_id})")
        self.conn.commit()
        self.cur.close()

    async def add_fanfiction_pairing(self, fanfic_id: int, pairing_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO fanfiction_pairings(fanfic_id, pairing_id) "
                         f"VALUES ({fanfic_id}, {pairing_id})")
        self.conn.commit()
        self.cur.close()

    async def add_fanfiction_tag(self, fanfic_id: int, tag_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO fanfiction_tags(fanfic_id, tag_id) "
                         f"VALUES ({fanfic_id}, {tag_id})")
        self.conn.commit()
        self.cur.close()

    async def add_fanfiction_narrow_tag(self, fanfic_id: int, narrow_tag_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO fanfiction_narrow_tags(fanfic_id, narrow_tag_id) "
                         f"VALUES ({fanfic_id}, {narrow_tag_id})")
        self.conn.commit()
        self.cur.close()

    async def get_fanfiction_id(self, title: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM fanfiction WHERE title = %s", (title,))
        ff_id = self.cur.fetchone()
        self.cur.close()
        return ff_id[0]

    async def get_narrow_tag_id_by_ff_id(self, ff_id: int):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT narrow_tag_id FROM fanfiction_narrow_tags WHERE fanfic_id = %s", (ff_id,))
        ff_id = self.cur.fetchall()
        self.cur.close()
        id_list = [tup[0] for tup in ff_id]
        return id_list


class Authors:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        self.cur = self.conn.cursor()

    async def add_author(self, author_name: str):
        self.cur.execute(
            "SELECT COUNT(*) FROM authors WHERE username = %s",
            (author_name,))
        author_count = self.cur.fetchone()[0]
        if author_count == 0:
            self.cur.execute(f"INSERT INTO authors(username) VALUES ('{author_name}')")
            self.conn.commit()
        self.cur.close()

    async def get_author_id(self, author_name: str):
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT id FROM authors WHERE username = %s", (author_name,))
        author_id = self.cur.fetchone()
        self.cur.close()
        return author_id[0]
