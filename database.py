import sqlite3
import bcrypt

def init_db():
    with sqlite3.connect("main.db") as db:
        cursor = db.cursor()
        
        # Drop existing tables to update schema
        cursor.execute("DROP TABLE IF EXISTS info")
        cursor.execute("DROP TABLE IF EXISTS sessions")
        
        # Create users table with enhanced security
        cursor.execute('''
        CREATE TABLE info(
            userID INTEGER PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            firstname VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            password_hash BLOB NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )''')
        
        # Create sessions table
        cursor.execute('''
        CREATE TABLE sessions(
            session_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            token VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES info(userID)
        )''')
        
        db.commit()

if __name__ == "__main__":
    init_db()