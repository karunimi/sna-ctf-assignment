from flask import Flask, request, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sql_injection', methods=['GET', 'POST'])
def sql_injection():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            flag = "FLAG{sql_injection_success}"
            return f"Welcome, {username}. Here is your flag: {flag}"
        else:
            return "Invalid credentials. Try again."
    return render_template('sql_injection.html')

@app.route('/submit_flag', methods=['GET', 'POST'])
def submit_flag():
    message = ''
    if request.method == 'POST':
        flag = request.form['flag']
        if flag == '{sql_injection_success}': 
            message = "Congratulations! You've captured the flag!"
        else:
            message = "Sorry, that's not the correct flag. Try again."
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5650)
