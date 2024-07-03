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
            UserName TEXT,
            Month INTEGER,
            Day INTEGER,
            Year INTEGER
        )
        ''')
        self.conn.commit()

    def insert_user(self, userid, username, month, day, year):
        self.cursor.execute('INSERT INTO Users (UserID, UserName, Month, Day, Year) VALUES (?, ?, ?, ?, ?)', (userid, username, month, day, year))
        self.conn.commit()

    def retrieve_users(self):
        self.cursor.execute("SELECT UserID FROM Users")
        return self.cursor.fetchall()
    
    def retrieve_all(self):
        self.cursor.execute("SELECT UserID, UserName, Month, Day, Year FROM Users")
        return self.cursor.fetchall()
    
    def user_exists(self, userid):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE UserID=?", (userid,))
        count = self.cursor.fetchone()[0]
        return count > 0
    
    def user_name_exists(self, username):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE UserName=?", (username,))
        count = self.cursor.fetchone()[0]
        return count > 0
    
    def get_birthday_via_username(self, username):
        self.cursor.execute('SELECT Month, Day FROM Users WHERE UserName = ?', (username,))
        return self.cursor.fetchone()
    
    def get_birthday_via_id(self, userid):
        self.cursor.execute('SELECT Month, Day, Year FROM Users WHERE UserID = ?', (userid,))
        return self.cursor.fetchone()
    
    def get_id(self, username, month, day):
        self.cursor.execute('SELECT UserId FROM Users WHERE Username = ? AND Month = ? AND Day = ?', (username, month, day))
        return self.cursor.fetchone()[0]
    
    def remove_user(self, userid):
        self.cursor.execute('DELETE FROM Users WHERE UserID = ?', (userid,))
        self.conn.commit()

    def close(self):
        self.conn.close()