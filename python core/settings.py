import sqlite3


class Settings:
    __slots__ = 'user_id', 'language'

    def __init__(self, user_id, language='eng'):
        self.user_id = user_id
        self.language = language

    def save_language(self):
        conn = sqlite3.connect('settings_db.sql')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS settings_db '
                    '(user_id INTEGER PRIMARY KEY UNIQUE NOT NULL, '
                    'language VARCHAR(10) NOT NULL)')
        conn.commit()
        conn.close()

    def insert(self):
        with sqlite3.connect('settings_db.sql') as conn:
            cur = conn.cursor()

            try:
                cur.execute('INSERT INTO settings_db VALUES (?, ?)',
                            (self.user_id, self.language))
                conn.commit()

            except:
                cur.execute('UPDATE settings_db '
                            'SET language=? '
                            'WHERE user_id=?',
                            (self.language, self.user_id,))
                conn.commit()

    def select_language(self):
        conn = sqlite3.connect('settings_db.sql')
        cur = conn.cursor()
        cur.execute('SELECT language FROM settings_db WHERE user_id=?',
                    (self.user_id,))
        data = cur.fetchone()
        conn.close()
        if data:
            language = data[0]
            return language
        else:
            return None
