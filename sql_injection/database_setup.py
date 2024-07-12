import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE users
                  (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

# Insert a sample user
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")

# Save (commit) the changes and close the connection
conn.commit()
conn.close()
