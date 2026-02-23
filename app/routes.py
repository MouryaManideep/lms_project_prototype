from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required
from sqlalchemy import asc, desc

from .models import Course, Enrollment, User
from . import db
from .decorators import role_required


# ----------------------------------
# BLUEPRINT
# ----------------------------------
main = Blueprint("main", __name__)


# ----------------------------------
# HOME (GRID + SORT + PRIORITY LOGIC)
# ----------------------------------
@main.route("/")
def home():

    sort_by = request.args.get("sort", "title")
    order = request.args.get("order", "asc")

    query = Course.query

    # Apply sorting
    if sort_by == "title":
        query = query.order_by(
            asc(Course.title) if order == "asc"
            else desc(Course.title)
        )

    elif sort_by == "instructor":
        query = query.join(User).order_by(
            asc(User.username) if order == "asc"
            else desc(User.username)
        )

    courses = query.all()

    enrolled_course_ids = []

    # Student: enrolled courses first
    if current_user.is_authenticated and current_user.role == "student":
        enrollments = Enrollment.query.filter_by(
            student_id=current_user.id
        ).all()

        enrolled_course_ids = [e.course_id for e in enrollments]

        courses.sort(
            key=lambda c: c.id not in enrolled_course_ids
        )

    # Instructor: own courses first
    if current_user.is_authenticated and current_user.role == "instructor":
        courses.sort(
            key=lambda c: c.instructor_id != current_user.id
        )

    return render_template(
        "index.html",
        courses=courses,
        enrolled_course_ids=enrolled_course_ids,
        sort_by=sort_by,
        order=order
    )


# ----------------------------------
# CREATE COURSE (Instructor Only)
# ----------------------------------
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


# ----------------------------------
# EDIT COURSE (Instructor Only)
# ----------------------------------
@main.route("/edit-course/<int:course_id>", methods=["GET", "POST"])
@login_required
@role_required("instructor")
def edit_course(course_id):

    course = Course.query.get_or_404(course_id)

    if course.instructor_id != current_user.id:
        flash("Access denied!")
        return redirect(url_for("main.home"))

    if request.method == "POST":
        course.title = request.form.get("title")
        course.description = request.form.get("description")

        db.session.commit()
        flash("Course updated successfully!")
        return redirect(url_for("main.home"))

    return render_template("edit_course.html", course=course)


# ----------------------------------
# DELETE COURSE (Instructor Only)
# ----------------------------------
@main.route("/delete-course/<int:course_id>")
@login_required
@role_required("instructor")
def delete_course(course_id):

    course = Course.query.get_or_404(course_id)

    if course.instructor_id != current_user.id:
        flash("Access denied!")
        return redirect(url_for("main.home"))

    db.session.delete(course)
    db.session.commit()

    flash("Course deleted successfully!")
    return redirect(url_for("main.home"))


# ----------------------------------
# INSTRUCTOR DASHBOARD
# ----------------------------------
@main.route("/dashboard")
@login_required
@role_required("instructor")
def instructor_dashboard():

    courses = Course.query.filter_by(
        instructor_id=current_user.id
    ).all()

    total_courses = len(courses)

    total_students = sum(len(course.enrollments) for course in courses)

    return render_template(
        "dashboard.html",
        courses=courses,
        total_courses=total_courses,
        total_students=total_students
    )


# ----------------------------------
# VIEW STUDENTS OF A COURSE
# ----------------------------------
@main.route("/course/<int:course_id>/students")
@login_required
@role_required("instructor")
def course_students(course_id):

    course = Course.query.get_or_404(course_id)

    if course.instructor_id != current_user.id:
        flash("Access denied!")
        return redirect(url_for("main.dashboard"))

    return render_template("course_students.html", course=course)


# ----------------------------------
# ENROLL (Student)
# ----------------------------------
@main.route("/enroll/<int:course_id>")
@login_required
@role_required("student")
def enroll(course_id):

    existing = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()

    if existing:
        flash("Already enrolled!")
        return redirect(url_for("main.home"))

    enrollment = Enrollment(
        student_id=current_user.id,
        course_id=course_id
    )

    db.session.add(enrollment)
    db.session.commit()

    flash("Enrolled successfully!")
    return redirect(url_for("main.home"))


# ----------------------------------
# STUDENT DASHBOARD
# ----------------------------------
@main.route("/student-dashboard")
@login_required
@role_required("student")
def student_dashboard():

    enrollments = Enrollment.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "student_dashboard.html",
        enrollments=enrollments
    )


# ----------------------------------
# UNENROLL
# ----------------------------------
@main.route("/unenroll/<int:course_id>")
@login_required
@role_required("student")
def unenroll(course_id):

    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()

    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        flash("Unenrolled successfully!")

    return redirect(url_for("main.home"))


# ----------------------------------
# TEST ROUTE
# ----------------------------------
@main.route("/test")
def test():
    return "Test route working"