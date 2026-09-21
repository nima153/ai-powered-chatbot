import sqlite3

def init_db():
    conn = sqlite3.connect('chatbot_logs.db')
    cursor = conn.cursor()
    # Create logs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interaction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(user_query, bot_response):
    conn = sqlite3.connect('chatbot_logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interaction_logs (user_query, bot_response)
        VALUES (?, ?)
    ''', (user_query, bot_response))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
