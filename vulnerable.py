"""
Intentionally Vulnerable Python Flask App
FOR SECURITY TRAINING / EDUCIONAL USE ONLY

This file demonstrates common security vulnerabilities:
- SQL Injection
- Command Injection
- Hardcoded Secrets
- Weak Authentication
- Unsafe File Upload Handling
- Debug Mode Enabled
- Insecure Deserialization

DO NOT deploy this application to production.
"""

from flask import Flask, request
import sqlite3
import os
import pickle

app = Flask(__name__)

# Hardcoded secret (vulnerability)
app.secret_key = "super-secret-password"

DATABASE = "users.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    c.execute(
        "INSERT INTO users (username, password) VALUES ('admin', 'admin123')"
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "Vulnerable demo app is running."


# SQL Injection vulnerability
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Vulnerable query construction
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Executing query:", query)

    result = c.execute(query).fetchone()
    conn.close()

    if result:
        return "Login successful!"
    return "Invalid credentials"


# Command Injection vulnerability
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # Unsafe shell execution
    output = os.popen(f"ping -c 1 {host}").read()

    return f"<pre>{output}</pre>"


# Unsafe file upload
@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files["file"]

    # No validation of filename or content
    save_path = os.path.join("uploads", uploaded_file.filename)
    uploaded_file.save(save_path)

    return f"Saved to {save_path}"


# Insecure deserialization vulnerability
@app.route("/deserialize", methods=["POST"])
def deserialize():
    raw = request.data

    # Dangerous: arbitrary code execution possible
    obj = pickle.loads(raw)

    return f"Deserialized object: {obj}"


# Weak authentication logic
@app.route("/admin")
def admin():
    token = request.args.get("token")

    # Easily guessable token
    if token == "1234":
        return "Welcome admin!"

    return "Access denied", 403


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    init_db()

    # Debug mode enabled (vulnerability)
    app.run(debug=True, host="0.0.0.0", port=5000)
