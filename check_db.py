import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="fastapi",
    user="postgres",
    password="Raj@2001"
)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = cur.fetchall()
print("Tables in fastapi database:", tables)

if not any('posts' in t for t in tables):
    print("\n'posts' table NOT FOUND! Creating it...")
    cur.execute("""
        CREATE TABLE posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            published BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    print("'posts' table created successfully!")
else:
    print("'posts' table exists!")

conn.close()
