import sqlite3


class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db, timeout=30)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS backlog (id INTEGER PRIMARY KEY, title text, genre text,"
                         "rating text, score text, time text)")
        self.conn.commit()

    def insert(self, game, genre, rating, main_story, main_story_and_extras, completionist, score,):
        self.cur.execute("INSERT INTO backlog VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (game, genre, rating,
                                                                                    main_story, main_story_and_extras,
                                                                                    completionist, score))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM backlog")
        rows = self.cur.fetchall()
        return rows

    def search(self, game="", genre=""):
        self.cur.execute("SELECT * FROM backlog WHERE title=? OR genre=?", (game, genre))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM backlog WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, game, genre):
        self.cur.execute("UPDATE backlog SET title=?, genre=? WHERE id=?", (game, genre, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
