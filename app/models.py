from . import db, login_manager
from flask_login import UserMixin


# ----------------------------------
# USER MODEL
# ----------------------------------
# Represents all users in the system
# A user can be either:
# - student
# - instructor
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Username must be unique
    username = db.Column(db.String(100), unique=True, nullable=False)

    # Email used for login
    email = db.Column(db.String(150), unique=True, nullable=False)

    # Password is stored as a HASH (never plain text)
    password = db.Column(db.String(200), nullable=False)

    # Role-based access control (student / instructor)
    role = db.Column(db.String(50), nullable=False, default="student")


# ----------------------------------
# COURSE MODEL
# ----------------------------------
class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # NEW: thumbnail image URL
    thumbnail = db.Column(db.String(300), nullable=True)

    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    instructor = db.relationship('User', backref='courses')


# ----------------------------------
# ENROLLMENT MODEL
# ----------------------------------
class Enrollment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # Student enrolling
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Course being enrolled
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

    # Relationship for accessing student info
    student = db.relationship('User', backref='enrollments')


# ----------------------------------
# FLASK-LOGIN USER LOADER
# ----------------------------------
# Tells Flask-Login how to load user from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))