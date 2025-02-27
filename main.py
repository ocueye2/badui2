import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,"/static","static")
app.secret_key = 'your_secret_key'

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('static/db/users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        birth TEXT NOT NULL,
                        ssn TEXT NOT NULL,
                        email TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

@app.route('/main')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and user['password'] == password:
        return redirect(url_for('welcome'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        birth = request.form.get('birth')
        ssn = request.form.get('ssn')
        email = request.form.get('email')

        conn = get_db_connection()
        # Check if the user already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            flash('Username already exists!', 'danger')
            conn.close()
            return redirect(url_for('register'))

        conn.execute('INSERT INTO users (username, password,birth,ssn,email) VALUES (?, ?, ?, ?, ?)', (username, password,birth,ssn,email))
        conn.commit()
        conn.close()

        flash('User registered successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/welcome')
def welcome():
    return 'Welcome! You are logged in.'

@app.route('/hack', methods=['GET', 'POST'])
def hack():
    return  render_template('caphttthasca.html')

@app.route('/hacker', methods=['GET', 'POST'])
def surrender():
    if request.method == 'POST':
        if request.form.get('ans') == "cd /":
            return render_template("surrender.html")
    return  "wrong"

if __name__ == '__main__':
    init_db()  # Create the database and table if not already created
    app.run(debug=True)
