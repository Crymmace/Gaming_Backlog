import sqlite3


class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db, timeout=30)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS backlog (id INTEGER PRIMARY KEY, title text, genre text,"
                         "rating text, score text, time text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS preference(id INTEGER PRIMARY KEY, completion, genre)")
        self.conn.commit()

    def insert_backlog(self, game, genre, rating, main_story, main_story_and_extras, completionist, score,):
        self.cur.execute("INSERT INTO backlog VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (game, genre, rating,
                                                                                    main_story, main_story_and_extras,
                                                                                    completionist, score))
        self.conn.commit()

    def insert_preference(self, completion, genre):
        self.cur.execute("INSERT INTO preference VALUES(NULL, ?, ?)", (completion, genre))

        self.conn.commit()

    def view_backlog(self):
        self.cur.execute("SELECT * FROM backlog")
        rows = self.cur.fetchall()
        return rows

    def view_preference(self):
        self.cur.execute("SELECT * FROM preference")
        rows = self.cur.fetchall()
        return rows

    def search_backlog(self, game="", genre=""):
        self.cur.execute("SELECT * FROM backlog WHERE title=? OR genre=?", (game, genre))
        rows = self.cur.fetchall()
        return rows

    def search_preference_genre(self):
        self.cur.execute("SELECT genre FROM preference")
        rows = self.cur.fetchall()
        return rows

    def search_preference_completion(self):
        self.cur.execute("SELECT completion FROM preference")
        rows = self.cur.fetchall()
        return rows

    def delete_backlog(self, id):
        self.cur.execute("DELETE FROM backlog WHERE id=?", (id,))
        self.conn.commit()

    def delete_preference(self, id):
        self.cur.execute("DELETE FROM preference WHERE id=?", (id,))
        self.conn.commit()

    def update_backlog(self, id, game, genre):
        self.cur.execute("UPDATE backlog SET title=?, genre=? WHERE id=?", (game, genre, id))
        self.conn.commit()

    def update_preference(self, id, completion, genre):
        self.cur.execute("UPDATE preference SET completion=?, genre=? WHERE id=?", (completion, genre, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
