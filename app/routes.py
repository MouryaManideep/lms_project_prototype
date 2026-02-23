from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from .models import Course, Enrollment
from . import db
from flask_login import login_required
from .decorators import role_required

main = Blueprint("main", __name__)

@main.route("/")
def home():

    # Get search query from URL
    search_query = request.args.get("search")

    if search_query:
        # Filter courses by title
        courses = Course.query.filter(
            Course.title.ilike(f"%{search_query}%")
        ).all()
    else:
        courses = Course.query.all()

    enrolled_course_ids = []

    if current_user.is_authenticated and current_user.role == "student":
        enrollments = Enrollment.query.filter_by(
            student_id=current_user.id
        ).all()

        enrolled_course_ids = [e.course_id for e in enrollments]

    return render_template(
        "index.html",
        courses=courses,
        enrolled_course_ids=enrolled_course_ids
    )

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

# Edit Course (Instructor Only)
@main.route("/edit-course/<int:course_id>", methods=["GET", "POST"])
@login_required
@role_required("instructor")
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    # Ensure instructor owns the course
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

# Delete Course (Instructor Only)
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
# Shows instructor courses and enrolled students
@main.route("/dashboard")
@login_required
@role_required("instructor")
def instructor_dashboard():

    # Fetch only courses created by this instructor
    courses = Course.query.filter_by(
        instructor_id=current_user.id
    ).all()

    total_courses = len(courses)

    total_students = 0

    # Count total enrollments across all courses
    for course in courses:
        total_students += len(course.enrollments)

    return render_template(
        "dashboard.html",
        courses=courses,
        total_courses=total_courses,
        total_students=total_students
    )

# ----------------------------------
# VIEW ENROLLED STUDENTS FOR A COURSE
# ----------------------------------
# Allows instructor to see list of students
# enrolled in a specific course
@main.route("/course/<int:course_id>/students")
@login_required
@role_required("instructor")
def course_students(course_id):

    # Fetch the course
    course = Course.query.get_or_404(course_id)

    # Security check:
    # Only the instructor who owns the course can view students
    if course.instructor_id != current_user.id:
        flash("Access denied!")
        return redirect(url_for("main.dashboard"))

    return render_template(
        "course_students.html",
        course=course
    )

@main.route("/enroll/<int:course_id>")
@login_required
@role_required("student")
def enroll(course_id):

    # Prevent duplicate enrollment
    existing = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()

    if existing:
        flash("Already enrolled!")
        return redirect(url_for("main.home"))

    # Create new enrollment record
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
# Shows only courses that the logged-in
# student has enrolled in
@main.route("/student-dashboard")
@login_required
@role_required("student")
def student_dashboard():

    # Fetch all enrollments of the logged-in student
    enrollments = Enrollment.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "student_dashboard.html",
        enrollments=enrollments
    )

# ----------------------------------
# UNENROLL (DELETE OPERATION)
# ----------------------------------
# Allows a student to remove their enrollment
# from a course (Delete in CRUD)
@main.route("/unenroll/<int:course_id>")
@login_required
@role_required("student")
def unenroll(course_id):

    # Find enrollment record for this student & course
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()

    # Only delete if enrollment exists
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        flash("Unenrolled successfully!")

    return redirect(url_for("main.student_dashboard"))

# test route to verify main blueprint is working
@main.route("/test")
def test():
    return "Test route working"