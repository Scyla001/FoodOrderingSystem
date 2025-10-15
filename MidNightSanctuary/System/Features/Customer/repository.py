import datetime
from Features.Customer.model import Food, Category, Logs

class ReadFood:
    def __init__(self, conn):
        self.conn = conn
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT DEFAULT 'Type0',
                category TEXT NOT NULL,
                variety TEXT NOT NULL,
                price TEXT NOT NULL,
                sizes TEXT DEFAULT 'N/A'
            )
        """)
        self.conn.commit()
        cur.close()

    def retrieve_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, type, category, variety, price, sizes FROM foods ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        return [Food(*r) for r in rows] if rows else []

class SaveLogs:
    def __init__(self, conn):
        self.connL = conn
        cur = self.connL.cursor()
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
        self.connL.commit()
        cur.close()

    def save_all(self, x: Logs):
        cur = self.connL.cursor()
        dt = datetime.datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")
        cur.execute("""
            INSERT INTO logs(datetime, category, variety, price, sizes, quantity, total)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (dt, x.category, x.variety, x.price, x.size, x.qty, x.total))
        self.connL.commit()
        cur.close()
        return x

class ReadCategory:
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

    def retrieve_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, path, type FROM category ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        return [Category(*r) for r in rows] if rows else []
