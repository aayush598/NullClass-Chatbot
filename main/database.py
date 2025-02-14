import sqlite3

DB_NAME = "chatbot.db"

def create_tables():
    """Create database tables if not exists."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            ai_response TEXT,
            sentiment TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentiment TEXT,
            count INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def insert_chat(user_message, ai_response, sentiment):
    """Insert chat record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user_message, ai_response, sentiment) VALUES (?, ?, ?)", 
                   (user_message, ai_response, sentiment))
    conn.commit()
    conn.close()

def update_analytics(sentiment):
    """Update sentiment analytics."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT count FROM analytics WHERE sentiment = ?", (sentiment,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE analytics SET count = count + 1 WHERE sentiment = ?", (sentiment,))
    else:
        cursor.execute("INSERT INTO analytics (sentiment, count) VALUES (?, 1)", (sentiment,))
    
    conn.commit()
    conn.close()

def get_analytics():
    """Fetch sentiment analytics."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT sentiment, count FROM analytics")
    data = cursor.fetchall()
    conn.close()

    return [{"sentiment": row[0], "count": row[1]} for row in data]

create_tables()
