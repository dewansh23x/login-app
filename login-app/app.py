from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Helper: read users from file
def load_users():
    users = {}
    try:
        with open("users.txt", "r") as f:
            for line in f:
                email, password = line.strip().split(",")
                users[email] = password
    except FileNotFoundError:
        pass
    return users

# Helper: save new user
def save_user(email, password):
    with open("users.txt", "a") as f:
        f.write(f"{email},{password}\n")

@app.route('/')
def home():
    return redirect(url_for('login'))

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_users()
        if email in users:
            return "❌ User already exists! Please go to login."

        save_user(email, password)
        return redirect(url_for('login'))

    return render_template('signup.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_users()
        if email in users and users[email] == password:
            return render_template('welcome.html', email=email)
        else:
            return "❌ Invalid email or password."

    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
