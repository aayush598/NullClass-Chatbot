import sqlite3

DB_NAME = "chatbot.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table to store chat interactions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        chatbot_response TEXT,
        sentiment TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Table for analytics (e.g., most common topics)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_count INTEGER DEFAULT 0,
        positive_count INTEGER DEFAULT 0,
        negative_count INTEGER DEFAULT 0,
        neutral_count INTEGER DEFAULT 0
    )''')

    conn.commit()
    conn.close()

def insert_chat(user_input, chatbot_response, sentiment):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO chats (user_input, chatbot_response, sentiment) VALUES (?, ?, ?)", 
                   (user_input, chatbot_response, sentiment))
    
    conn.commit()
    conn.close()

def update_analytics(sentiment):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT query_count FROM analytics WHERE id = 1")
    row = cursor.fetchone()
    
    if row is None:
        cursor.execute("INSERT INTO analytics (query_count, positive_count, negative_count, neutral_count) VALUES (1, 0, 0, 0)")
    else:
        query_count = row[0] + 1
        cursor.execute("UPDATE analytics SET query_count = ? WHERE id = 1", (query_count,))
    
    if sentiment == "positive":
        cursor.execute("UPDATE analytics SET positive_count = positive_count + 1 WHERE id = 1")
    elif sentiment == "negative":
        cursor.execute("UPDATE analytics SET negative_count = negative_count + 1 WHERE id = 1")
    else:
        cursor.execute("UPDATE analytics SET neutral_count = neutral_count + 1 WHERE id = 1")
    
    conn.commit()
    conn.close()

create_tables()  # Initialize DB tables
