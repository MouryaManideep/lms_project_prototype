from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

"""Authentication blueprint.

Provides registration, login and logout routes. Uses `User` model
and stores password hashes via Werkzeug utilities.
"""

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration.

    POST: validate form, create `User` with hashed password.
    GET: render registration template.
    """

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login.

    POST: validate credentials and call `login_user`.
    GET: render login template.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid email or password!")

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    """Log the current user out and redirect to home."""
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for("main.home"))