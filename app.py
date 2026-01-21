from flask import Flask, render_template, request, redirect, url_for
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))

# In-memory database
USERS = {}

# Email regex pattern
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def is_valid_email(email):
    return re.match(EMAIL_PATTERN, email)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Email format validation
        if not is_valid_email(email):
            message = "Invalid email format"

        # Duplicate email check
        elif email in USERS:
            message = "Email already registered"

        else:
            USERS[email] = {
                "username": username,
                "password": password
            }
            message = "Registration successful. Please login."

    return render_template("register.html", message=message)


@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        for email, data in USERS.items():
            if data["username"] == username and data["password"] == password:
                return "Login Successful"

        error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    message = ""

    if request.method == "POST":
        email = request.form.get("email")

        # Email format check
        if not is_valid_email(email):
            message = "Invalid email format"

        # Registered email check
        elif email not in USERS:
            message = "Email not registered"

        else:
            return redirect(url_for("reset_password", email=email))

    return render_template("forgot_password.html", message=message)


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    message = ""
    email = request.args.get("email")

    if request.method == "POST":
        new_password = request.form.get("new_password")
        USERS[email]["password"] = new_password
        message = "Password reset successful. Please login."

    return render_template("reset_password.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
