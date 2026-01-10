import sqlite3

# This is a helper function to open a connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn
#setting up the tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # We added 'data_hash' to store the digital fingerprint
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            nrc TEXT NOT NULL,
            category TEXT,
            receipt_id TEXT,
            data_hash TEXT, 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
if __name__ == '__main__':
    init_db()
    print("✓ Database file 'database.db' created and table initialized.")