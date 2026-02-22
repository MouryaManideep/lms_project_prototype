from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from .models import Course
from . import db
from flask_login import login_required
from .decorators import role_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
    courses = Course.query.all()
    return render_template("index.html", courses=courses)

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

# Create Course (Instructor Only)
@main.route("/create-course", methods=["GET", "POST"])
@login_required
@role_required("instructor")
def create_course():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")

        new_course = Course(
            title=title,
            description=description,
            instructor_id=current_user.id
        )

        db.session.add(new_course)
        db.session.commit()

        flash("Course created successfully!")
        return redirect(url_for("main.home"))

    return render_template("create_course.html")