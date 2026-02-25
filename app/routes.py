from flask import Blueprint, render_template
from flask_login import login_required
from .decorators import role_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/instructor")
@login_required
@role_required("instructor")
def instructor_dashboard():
    return "<h2>Instructor Dashboard</h2>"

@main.route("/student")
@login_required
@role_required("student")
def student_dashboard():
    return "<h2>Student Dashboard</h2>"