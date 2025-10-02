import sqlite3

DB_PATH = r"C:\Users\apson\PycharmProjects\FastAPIProject\ecom.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Add the column without default
try:
    cursor.execute("ALTER TABLE reviews ADD COLUMN created_at DATETIME")
    print("Column 'created_at' added.")
except sqlite3.OperationalError:
    print("Column 'created_at' already exists.")

# Set default value for existing rows
cursor.execute("UPDATE reviews SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")

conn.commit()
conn.close()
print("✅ 'created_at' column updated successfully.")
