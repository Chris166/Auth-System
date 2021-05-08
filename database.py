import sqlite3

with sqlite3.connect("main.db") as db:
    cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS info(
userID INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL,
firstname VARCHAR(20) NOT NULL,
surname VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL);
''')

cursor.execute("""
INSERT INTO info(username,firstname,surname,password)
VALUES("test_User","Bob","Smith","MrBob")
""")
db.commit()

cursor.execute("SELECT * FROM info")
print(cursor.fetchall())
