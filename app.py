# Import necessary libraries
from flask import Flask, render_template, request, redirect
import sqlite3

# Create a Flask app
app = Flask(__name__)

#SQLite setup
conn = sqlite3.connect('flaskapp.db')
c=conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
          (username TEXT,password TEXT,firstname TEXT,lastname TEXT,email TEXT);''')
conn.commit()
conn.close()


# Route for the main page
@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # Save to SQLite3 Database
        conn = sqlite3.connect('flaskapp.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)", 
                       (username, password, first_name, last_name, email))
        conn.commit()
        conn.close()

        return render_template('success.html', first_name=first_name, last_name=last_name, email=email)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('flaskapp.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return f"Welcome {user[2]} {user[3]}, Email: {user[4]}"
        else:
            return "Login failed, please try again."
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
