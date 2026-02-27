from . import db, login_manager
from flask_login import UserMixin

"""app.models

Database models used by the LMS prototype.

Contains:
- User: represents students and instructors
- Course: course metadata and instructor relation
- Enrollment: association between students and courses
"""


# ==========================================================
# USER MODEL
# ==========================================================
# Represents both students and instructors
# Role-based access control handled using `role` field
# ==========================================================
class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    # Basic Info
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Role: "student" or "instructor"
    role = db.Column(db.String(50), nullable=False, default="student")

    # -------------------------
    # Relationships
    # -------------------------

    # Instructor -> Courses created
    courses = db.relationship(
        "Course",
        backref="instructor",
        lazy=True,
        cascade="all, delete"
    )

    # Student -> Enrollments
    enrollments = db.relationship(
        "Enrollment",
        backref="student",
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

    """User model docstring.

    Attributes:
        id: primary key
        username: display name
        email: contact/login email
        password: hashed password
        role: 'student' or 'instructor'
        courses: relationship to courses (if instructor)
        enrollments: relationship to Enrollment (if student)
    """


# ==========================================================
# COURSE MODEL
# ==========================================================
# Each course belongs to one instructor
# ==========================================================
class Course(db.Model):

    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Thumbnail image URL
    thumbnail = db.Column(db.String(500))

    # Foreign key -> instructor
    instructor_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    # -------------------------
    # Relationships
    # -------------------------

    # Course -> Enrollments
    enrollments = db.relationship(
        "Enrollment",
        backref="course",
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Course {self.title}>"

    """Course model docstring.

    Attributes:
        id: primary key
        title: course title
        description: full course description
        thumbnail: image URL
        instructor_id: FK to User (instructor)
        enrollments: relationship to Enrollment
    """


# ==========================================================
# ENROLLMENT MODEL
# ==========================================================
# Many-to-Many relationship between:
#   - Students
#   - Courses
# ==========================================================
class Enrollment(db.Model):

    __tablename__ = "enrollment"

    id = db.Column(db.Integer, primary_key=True)

    # Student who enrolled
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    # Course enrolled into
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Enrollment student={self.student_id} course={self.course_id}>"

    """Enrollment model docstring.

    Represents a student's enrollment in a course.
    Attributes:
        id: primary key
        student_id: FK to User
        course_id: FK to Course
    """


# ==========================================================
# FLASK-LOGIN USER LOADER
# ==========================================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))