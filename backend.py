import sqlite3


class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS backlog (id INTEGER PRIMARY KEY, title text, genre text)")
        self.conn.commit()

    def insert(self, title, genre):
        self.cur.execute("INSERT INTO backlog VALUES (NULL, ?, ?)", (title, genre))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM backlog")
        rows = self.cur.fetchall()
        return rows

    def search(self, title="", genre=""):
        self.cur.execute("SELECT * FROM backlog WHERE title=? OR genre=?", (title, genre))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM backlog WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, title, genre):
        self.cur.execute("UPDATE backlog SET title=?, genre=? WHERE id=?", (title, genre, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
