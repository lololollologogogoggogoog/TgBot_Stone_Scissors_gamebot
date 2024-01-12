import sqlite3


class Stats:
    __slots__ = 'user_id'

    def __init__(self, user_id):
        self.user_id = user_id

    def update_wins(self):
        with sqlite3.connect('DB_game.sql') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM DB_game WHERE user_id=?",
                           (self.user_id,))
            data = cursor.fetchone()
            if not data:
                cursor.execute("INSERT INTO DB_game VALUES (?, 1, 0, 0)",
                               (self.user_id,))

            cursor.execute(
                "UPDATE DB_game SET wins = wins + 1 WHERE user_id=?",
                (self.user_id,))
            conn.commit()

    def update_losses(self):
        with sqlite3.connect('DB_game.sql') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM DB_game WHERE user_id=?",
                           (self.user_id,))
            data = cursor.fetchone()
            if not data:
                cursor.execute("INSERT INTO DB_game VALUES (?, 0, 1, 0)",
                               (self.user_id,))
            cursor.execute(
                "UPDATE DB_game SET defeats = defeats + 1 WHERE user_id=?",
                (self.user_id,))
            conn.commit()

    def update_draw(self):
        with sqlite3.connect('DB_game.sql') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM DB_game WHERE user_id=?",
                           (self.user_id,))
            data = cursor.fetchone()
            if not data:
                cursor.execute("INSERT INTO DB_game VALUES (?, 0, 0, 1)",
                               (self.user_id,))
            cursor.execute(
                "UPDATE DB_game SET draws = draws + 1 WHERE user_id=?",
                (self.user_id,))
            conn.commit()

    def get_stats(self):
        with sqlite3.connect('DB_game.sql') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT  wins, defeats, draws FROM DB_game WHERE "
                           "user_id=?",
                           (self.user_id,))
            data = cursor.fetchone()
            if data:
                return data
            else:
                return 0, 0, 0
