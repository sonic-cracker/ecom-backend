import sqlite3

conn = sqlite3.connect("ecom.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE orders ADD COLUMN rating INTEGER")
except:
    print("Column 'rating' already exists")

try:
    cursor.execute("ALTER TABLE orders ADD COLUMN review TEXT")
except:
    print("Column 'review' already exists")

conn.commit()
conn.close()

print("✅ Columns added successfully.")
