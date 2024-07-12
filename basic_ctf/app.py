from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/challenge1')
def challenge1():
    return render_template('challenge1.html')


@app.route('/submit_flag', methods=['GET', 'POST'])
def submit_flag():
    message = ''
    if request.method == 'POST':
        flag = request.form['flag']
        if flag == '{karthikaa_hidden_flag}': 
            message = "Congratulations! You've captured the flag!"
        else:
            message = "Sorry, that's not the correct flag. Try again."
    return render_template('challenge1.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000) 
