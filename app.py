"""
author @ kumar dahal
"""

from flask import Flask, render_template, request, jsonify
import sqlite3


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


   
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact-us')
def contact():
    return render_template('contact.html')

@app.route('/team')
def team():
    return render_template('Team.html')



def get_db_connection():
    return sqlite3.connect('login.db')

# Route to handle sign-in page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the username or email and password exist in the database
        cur.execute('SELECT * FROM login WHERE (username = ? OR email = ?) AND password = ?', (username_or_email, username_or_email, password))
        user = cur.fetchone()

        conn.close()

        if user:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid username/email or password'})
    else:
        return render_template('register.html')






@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Connect to the SQLite database
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()

    # Check if the username or email already exists
    cursor.execute('SELECT * FROM signup WHERE username=? OR email=?', (username, email))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return jsonify({'error': 'Username or email already exists'})

    # Insert the new user into the signup table
    cursor.execute('INSERT INTO signup (username, email, password) VALUES (?, ?, ?)', (username, email, password))
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'success': True, 'message': 'User registered successfully'})

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8001)    