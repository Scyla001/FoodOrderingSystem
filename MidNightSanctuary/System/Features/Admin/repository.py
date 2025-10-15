import datetime
from Features.Admin.model import Food
from Features.Admin.model import Logs
from Features.Admin.model import Category

class SaveFood:
    def __init__(self, conn):
        self.conn = conn
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT DEFAULT 'single-size',
                category TEXT NOT NULL,
                variety TEXT NOT NULL,
                price TEXT NOT NULL,
                sizes TEXT DEFAULT 'N/A'
            )
        """)
        self.conn.commit()
        cur.close()

    def save_all(self, x: Food):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO foods(type, category, variety, price, sizes) VALUES (?, ?, ?, ?, ?)",
            (x.type, x.category, x.variety, str(x.price), x.size)
        )
        self.conn.commit()
        cur.close()
        return x

    def retrieve_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, type, category, variety, price, sizes FROM foods ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        return [Food(*r) for r in rows] if rows else []

    def update(self, x: Food):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE foods SET type=?, category=?, variety=?, price=?, sizes=? WHERE id=?",
            (x.type, x.category, x.variety, str(x.price), x.size, x.id)
        )
        self.conn.commit()
        cur.close()

    def delete(self, id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM foods WHERE id=?", (id,))
        self.conn.commit()
        cur.close()
        return True

class ReadLogs:
    def __init__(self, conn):
        self.conn = conn
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT DEFAULT '',
                category TEXT NOT NULL,
                variety TEXT NOT NULL,
                price INTEGER NOT NULL,
                sizes TEXT DEFAULT 'N/A',
                quantity INTEGER NOT NULL,
                total INTEGER NOT NULL
            )
        """)
        self.conn.commit()
        cur.close()

    def retrieve_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, datetime, category, variety, price, sizes, quantity, total FROM logs ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        result = []
        for r in rows:
            log_item = Logs(*r)
            # r mapping order matches constructor
            result.append(log_item)
        return result

class SaveCategory:
    def __init__(self, conn):
        self.conn = conn
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                path TEXT NOT NULL,
                type TEXT NOT NULL
            )
        """)
        self.conn.commit()
        cur.close()

    def save_all(self, x: Category):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO category(title, path, type) VALUES (?, ?, ?)",
            (x.title, x.path, x.type)
        )
        self.conn.commit()
        cur.close()
        return x

    def retrieve_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, path, type FROM category ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        return [Category(*r) for r in rows] if rows else []

    def update(self, x: Category):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE category SET title=?, path=?, type=? WHERE id=?",
            (x.title, x.path, x.type, x.id)
        )
        self.conn.commit()
        cur.close()

    def delete(self, id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM category WHERE id=?", (id,))
        self.conn.commit()
        cur.close()
        return True
