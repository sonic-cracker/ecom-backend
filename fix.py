import sqlite3

# Connect to your existing database
conn = sqlite3.connect("ecom.db")
cursor = conn.cursor()

try:
    # Try adding the missing column
    cursor.execute("ALTER TABLE users ADD COLUMN profile_image TEXT;")
    print("✅ Column 'profile_image' added successfully.")
except sqlite3.OperationalError as e:
    print("⚠️ Could not add column (maybe already exists):", e)

conn.commit()
conn.close()
