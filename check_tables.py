import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="fastapi",
    user="postgres",
    password="Raj@2001"
)
cur = conn.cursor()

# Check exact table names
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = cur.fetchall()

for t in tables:
    print(f"Table name: '{t[0]}'")
    print(f"  Characters: {[c for c in t[0]]}")

# Try different queries
for name in ['Fast_API2', 'fast_api2', '"FasT_API2"']:
    try:
        cur.execute(f"SELECT * FROM {name}")
        rows = cur.fetchall()
        print(f"\nQuery 'SELECT * FROM {name}' => SUCCESS! Rows: {len(rows)}")
        print(f"  Data: {rows}")
    except Exception as e:
        conn.rollback()
        print(f"\nQuery 'SELECT * FROM {name}' => FAILED: {e}")

conn.close()
