from flask import Flask, request, render_template, g, jsonify, redirect, url_for
import os
import sqlite3
import shlex
import subprocess

app = Flask(__name__)
DATABASE = 'database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

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

# Secret flags for challenges
flags = {
    'challenge1': 'flag{sql_injection_flag_found}',
    'challenge2': 'flag{XSS_Vulnerability_Found}',
    'challenge3': 'flag{command-injection}',
    'challenge4': 'flag{FiLe_upload}'
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        
        # WARNING: Vulnerable to SQL injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return f"Welcome, {username}. Here is your flag: {flags['challenge1']}"
        else:
            return "Invalid credentials. Try again."
    return render_template('login1.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fruits WHERE name LIKE ?", ('%' + search_query + '%',))
        results = cursor.fetchall()

        if results:
            message = f"Results for: {search_query}"
            return render_template('search.html', message=message, results=results)
        else:
            message = f"No results found for: {search_query}"
            return render_template('search.html', message=message, results=[])

    return render_template('search.html', message='', results=[])

# Route to render index.html
@app.route('/index')
def index():
    return render_template('index.html', result='')

# Route to execute commands
@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    
    if command.startswith('status'):
        parts = command.split(';')
        if len(parts) == 2:
            status_command = parts[0].strip()
            other_command = parts[1].strip()
            
            if status_command.startswith('status'):
                device_name = status_command.split()[1].strip()
                filepath = os.path.join('iot_device_files', f'{device_name}.txt')
                
                if os.path.isfile(filepath):
                    with open(filepath, 'r') as file:
                        output = file.read()
                else:
                    output = 'Device status file not found.'
            else:
                output = 'Invalid status command. Usage: status device_name'
            
            if other_command.startswith('ls'):
                output += '\n\n'
                output += subprocess.check_output('ls iot_device_files', shell=True).decode('utf-8')
            elif other_command.startswith('cat'):
                parts = other_command.split()
                if len(parts) == 2:
                    filename = parts[1]
                    filepath = os.path.join('iot_device_files', filename)
                    if os.path.isfile(filepath):
                        output += '\n\n'
                        output += subprocess.check_output(f'cat {filepath}', shell=True).decode('utf-8')
                    else:
                        output = 'File not found.'
                else:
                    output = 'Invalid cat command. Usage: cat filename'
            else:
                output += '\n\n'
                output += subprocess.check_output(f'{other_command}', shell=True).decode('utf-8')
        else:
            output = 'Invalid command. Usage: status device_name; ls/cat command'
    else:
        output = 'Invalid command. You must start with "status".'

    return render_template('index.html', output=output)




@app.route('/file', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        allowed_extensions = {'.sh', '.txt', '.jpg', '.png'}
        if file and any(file.filename.endswith(ext) for ext in allowed_extensions):
            filepath = os.path.join('uploads', file.filename)
            file.save(filepath)
            
            # Convert Windows line endings to Unix line endings
            with open(filepath, 'rb') as f:
                content = f.read().replace(b'\r\n', b'\n')
            with open(filepath, 'wb') as f:
                f.write(content)
                
            os.chmod(filepath, 0o755)  # Ensure the file has execute permissions
            if file.filename.endswith('.sh'):
                return redirect(url_for('execute_file', filename=file.filename))
            else:
                return f"File {file.filename} uploaded successfully."
        return 'Invalid file type'
    return render_template('file.html')

@app.route('/execute_file/<filename>')
def execute_file(filename):
    filepath = os.path.join('uploads', filename)
    if os.path.exists(filepath):
        try:
            # Change working directory to 'uploads' and execute the script
            result = subprocess.check_output(['bash', filename], cwd='uploads', stderr=subprocess.STDOUT)
            return f"<pre>{result.decode()}</pre>"
        except subprocess.CalledProcessError as e:
            return f"Error executing file: {e.output.decode()}"
    return 'File not found'


total_points = 0

@app.route('/submit_flag', methods=['POST'])
def submit_flag():
    data = request.get_json()
    flag = data.get('flag')
    challenge = data.get('challenge')

    global total_points
    
    if challenge in flags and flag == flags[challenge]:
        total_points += 1
        return jsonify({'correct': True, 'total_points': total_points})
    else:
        return jsonify({'correct': False})

@app.route('/flags')
def view_flags():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flags")
    flags = cursor.fetchall()
    flag_data = "<br>".join([f"Challenge: {flag[1]}, Flag: {flag[2]}" for flag in flags])
    return flag_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222)
