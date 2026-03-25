import sqlite3

conn = sqlite3.connect("attack_logs.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    attack_type TEXT,
    ip_address TEXT,
    payload TEXT,
    confidence REAL,
    country TEXT,
    city TEXT,
    latitude REAL,
    longitude REAL,
    organization TEXT,
    vpn INTEGER,
    proxy INTEGER,
    hosting INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully")