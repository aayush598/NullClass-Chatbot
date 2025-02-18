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
            sentiment TEXT,
            topic TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            metric TEXT PRIMARY KEY,
            value INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_chat(user_message, ai_response, sentiment, topic):
    """Insert chat record into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user_message, ai_response, sentiment, topic) VALUES (?, ?, ?, ?)", 
                   (user_message, ai_response, sentiment, topic))
    conn.commit()
    conn.close()
    update_analytics("total_queries")
    update_analytics(f"sentiment_{sentiment}")
    update_analytics(f"topic_{topic}")

def update_analytics(metric):
    """Update analytics count."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM analytics WHERE metric = ?", (metric,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE analytics SET value = value + 1 WHERE metric = ?", (metric,))
    else:
        cursor.execute("INSERT INTO analytics (metric, value) VALUES (?, 1)", (metric,))
    conn.commit()
    conn.close()

def get_analytics():
    """Fetch analytics."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT metric, value FROM analytics")
    data = cursor.fetchall()
    conn.close()
    return [{"metric": row[0], "value": row[1]} for row in data]

create_tables()