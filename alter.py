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

try:
    cursor.execute("ALTER TABLE order_items ADD COLUMN price_per_item FLOAT")
except:
    print("Column 'price_per_item' already exists")

try:
    cursor.execute("ALTER TABLE reviews ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
except sqlite3.OperationalError:
    print("Column 'created_at' already exists")

cursor.execute("PRAGMA table_info(reviews);")
print("\nColumns in reviews:")
for col in cursor.fetchall():
    print(col)

conn.commit()
conn.close()

print("✅ Columns added successfully.")
