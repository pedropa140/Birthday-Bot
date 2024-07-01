import sqlite3

class UserDatabase:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID TEXT PRIMARY KEY,
            Month INTEGER,
            Day INTEGER,
            Year INTEGER
        )
        ''')
        self.conn.commit()

    def insert_user(self, userid, month, day, year):
        self.cursor.execute('INSERT INTO Users (UserID, Month, Day, Year) VALUES (?, ?, ?, ?)', (userid, month, day, year))
        self.conn.commit()

    def retrieve_users(self):
        self.cursor.execute("SELECT UserID FROM Users")
        return self.cursor.fetchall()
    
    def user_exists(self, userid):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE UserID=?", (userid,))
        count = self.cursor.fetchone()[0]
        return count > 0
    
    def remove_user(self, userid):
        self.cursor.execute('DELETE FROM Users WHERE UserID = ?', (userid,))
        self.conn.commit()

    def close(self):
        self.conn.close()