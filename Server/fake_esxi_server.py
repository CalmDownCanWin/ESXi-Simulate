from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define your authentication logic (replace with your actual validation)
def authenticate(username, password):
    # Sample logic:
    valid_users = {"admin": "password", "user": "secret"}
    if username in valid_users and valid_users[username] == password:
        return True
    return False

@app.route('/')
def login_page():
    return render_template('login.html') 

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if authenticate(username, password):
        return "Login Successful! Welcome, " + username 
    else:
        return "Invalid username or password"

if __name__ == '__main__':
    app.run(debug=True)