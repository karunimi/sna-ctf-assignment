import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE users
                  (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

cursor.execute('''CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comment TEXT
)''')

# Insert a sample user
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")

cursor.execute('''
        CREATE TABLE IF NOT EXISTS fruits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge TEXT NOT NULL,
            flag TEXT NOT NULL
        )
    ''')

cursor.execute('INSERT INTO fruits (name, description) VALUES (?, ?)', ('Apple', 'A sweet red fruit'))
cursor.execute('INSERT INTO fruits (name, description) VALUES (?, ?)', ('Banana', 'A long yellow fruit'))
cursor.execute('INSERT INTO fruits (name, description) VALUES (?, ?)', ('Cherry', 'A small red fruit'))
cursor.execute('INSERT INTO fruits (name, description) VALUES (?, ?)', ('Date', 'A sweet brown fruit'))
cursor.execute('INSERT INTO fruits (name, description) VALUES (?, ?)', ('Elderberry', 'A dark purple fruit'))

cursor.execute('INSERT INTO flags (challenge, flag) VALUES (?, ?)', ('XSS Challenge', 'flag{XSS_Challenge_Completed}'))

# Save (commit) the changes and close the connection
conn.commit()
conn.close()
