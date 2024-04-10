import psycopg2


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host='',
            database='',
            user='',
            password='',
            port=5433
        )
        self.cur = self.conn.cursor()

    async def create_table_tags(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS tags("
            "id INTEGER PRIMARY KEY,"
            "tag VARCHAR)")
        self.conn.commit()
        self.cur.close()

    async def create_table_fandoms(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fandoms("
            "id INTEGER PRIMARY KEY,"
            "fandom VARCHAR)")
        self.conn.commit()
        self.cur.close()

    async def create_table_pairings(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS pairings("
            "id INTEGER PRIMARY KEY,"
            "pairing VARCHAR,"
            "fandom_id INTEGER REFERENCES fandoms(id))")
        self.conn.commit()
        self.cur.close()

    async def create_table_users(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users("
            "id INTEGER PRIMARY KEY,"
            "chat_id INTEGER UNIQUE,"
            "username VARCHAR)")
        self.conn.commit()
        self.cur.close()

    async def create_table_authors(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS authors("
            "id INTEGER PRIMARY KEY,"
            "chat_id INTEGER UNIQUE,"
            "username VARCHAR)")
        self.conn.commit()
        self.cur.close()

    async def create_table_users_preferences(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users_preferences("
            "user_id INTEGER REFERENCES users(id),"
            "tag_id INTEGER REFERENCES tags(id),"
            "fandom_id INTEGER REFERENCES fandoms(id),"
            "pairing_id INTEGER REFERENCES pairings(id),"
            "PRIMARY KEY(user_id, tag_id, fandom_id, pairing_id))")
        self.conn.commit()
        self.cur.close()

    async def create_table_fanfiction(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction("
            "id INTEGER PRIMARY KEY,"
            "title VARCHAR,"
            "rating VARCHAR,"
            "status VARCHAR,"
            "author_id REFERENCES authors(id))")
        self.conn.commit()
        self.cur.close()

    async def create_table_fanfiction_tags(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_tags("
            "fanfic_id REFERENCES fanfiction(id),"
            "tag_id REFERENCES tags(id)"
            "PRIMARY KEY(fanfic_id, tag_id))")
        self.conn.commit()
        self.cur.close()

    async def create_table_fanfiction_pairings(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_pairings("
            "fanfic_id REFERENCES fanfiction(id),"
            "pairing_id REFERENCES pairings(id)"
            "PRIMARY KEY(fanfic_id, pairing_id))")
        self.conn.commit()
        self.cur.close()

    async def create_table_fanfiction_fandoms(self):
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS fanfiction_fandoms("
            "fanfic_id REFERENCES fanfiction(id),"
            "fandom_id REFERENCES fandoms(id)"
            "PRIMARY KEY(fanfic_id, fandom_id))")
        self.conn.commit()
        self.cur.close()


