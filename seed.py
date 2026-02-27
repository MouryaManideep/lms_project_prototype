"""Database seeder for demo data.

This script resets the local SQLite database, creates demo instructors
and students, creates a set of sample courses, and enrolls students
randomly into courses. Run with `python seed.py` after installing
requirements and creating the virtual environment.
"""

import random
from app import create_app, db
from app.models import User, Course, Enrollment
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# -----------------------------
# RESET DATABASE
# -----------------------------
db.drop_all()
db.create_all()
print("Database reset completed.")

# -----------------------------
# CREATE INSTRUCTORS
# -----------------------------
num_instructors = 5
instructors = []

for i in range(1, num_instructors + 1):
    instructor = User(
        username=f"tp{i}",
        email=f"tp{i}@l.com",
        password=generate_password_hash(f"tp{i}"),
        role="instructor"
    )
    db.session.add(instructor)
    instructors.append(instructor)

db.session.commit()
print(f"{num_instructors} instructors created.")

# -----------------------------
# CREATE STUDENTS (3x instructors)
# -----------------------------
num_students = num_instructors * 3
students = []

for i in range(1, num_students + 1):
    student = User(
        username=f"st{i}",
        email=f"st{i}@l.com",
        password=generate_password_hash(f"st{i}"),
        role="student"
    )
    db.session.add(student)
    students.append(student)

db.session.commit()
print(f"{num_students} students created.")

# -----------------------------
# COURSE DATA (Title + Image)
# -----------------------------
course_data = [
    ("Data Structures", "https://images.unsplash.com/photo-1515879218367-8466d910aaa4"),
    ("Algorithms", "https://images.unsplash.com/photo-1555949963-aa79dcee981c"),
    ("Operating Systems", "https://images.unsplash.com/photo-1518770660439-4636190af475"),
    ("Computer Networks", "https://images.unsplash.com/photo-1526378722370-4b6a28c8f8f7"),
    ("Database Systems", "https://images.unsplash.com/photo-1544383835-bda2bc66a55d"),
    ("Machine Learning", "https://images.unsplash.com/photo-1555255707-c07966088b7b"),
    ("Artificial Intelligence", "https://images.unsplash.com/photo-1531746790731-6c087fecd65a"),
    ("Web Development", "https://images.unsplash.com/photo-1498050108023-c5249f4df085"),
    ("Cloud Computing", "https://images.unsplash.com/photo-1544197150-b99a580bb7a8"),
    ("Cyber Security", "https://images.unsplash.com/photo-1563986768609-322da13575f3"),
    ("Software Engineering", "https://images.unsplash.com/photo-1517694712202-14dd9538aa97"),
    ("System Design", "https://images.unsplash.com/photo-1504384308090-c894fdcc538d"),
    ("Python Programming", "https://images.unsplash.com/photo-1526379095098-d400fd0bf935"),
    ("Java Programming", "https://images.unsplash.com/photo-1518773553398-650c184e0bb3"),
    ("C++ Programming", "https://images.unsplash.com/photo-1519389950473-47ba0277781c"),
    ("React Development", "https://images.unsplash.com/photo-1618477388954-7852f32655ec"),
    ("Flask Development", "https://images.unsplash.com/photo-1504639725590-34d0984388bd"),
    ("Django Framework", "https://images.unsplash.com/photo-1521737604893-d14cc237f11d"),
    ("Microservices", "https://images.unsplash.com/photo-1558494949-ef010cbdcc31"),
    ("DevOps", "https://images.unsplash.com/photo-1555066931-4365d14bab8c"),
    ("Docker & Kubernetes", "https://images.unsplash.com/photo-1605745341112-85968b19335b"),
    ("Git & GitHub", "https://images.unsplash.com/photo-1618401479427-c8ef9465bddd"),
    ("REST API Design", "https://images.unsplash.com/photo-1559028012-481c04fa702d"),
    ("Graph Theory", "https://images.unsplash.com/photo-1550751827-4bd374c3f58b"),
    ("Dynamic Programming", "https://images.unsplash.com/photo-1517430816045-df4b7de11d1d"),
    ("Blockchain", "https://images.unsplash.com/photo-1621761191319-c6fb62004040"),
    ("Big Data", "https://images.unsplash.com/photo-1509228627152-72ae9ae6848d"),
    ("Data Science", "https://images.unsplash.com/photo-1551288049-bebda4e38f71"),
    ("Statistics", "https://images.unsplash.com/photo-1581090700227-4c4f50c2f8d5"),
    ("Linear Algebra", "https://images.unsplash.com/photo-1509223197845-458d87318791"),
    ("Discrete Math", "https://images.unsplash.com/photo-1506784983877-45594efa4cbe"),
    ("Computer Arch", "https://images.unsplash.com/photo-1517336714731-489689fd1ca8"),
    ("Linux Admin", "https://images.unsplash.com/photo-1516116216624-53e697fedbea"),
    ("Mobile App Dev", "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c"),
    ("Android Dev", "https://images.unsplash.com/photo-1607252650355-f7fd0460ccdb"),
    ("iOS Dev", "https://images.unsplash.com/photo-1510552776732-01accd7f4b7b"),
    ("Full Stack", "https://images.unsplash.com/photo-1504639725590-34d0984388bd"),
    ("Backend Eng", "https://images.unsplash.com/photo-1504384308090-c894fdcc538d"),
    ("Frontend Eng", "https://images.unsplash.com/photo-1492724441997-5dc865305da7"),
    ("Testing & QA", "https://images.unsplash.com/photo-1518770660439-4636190af475"),
    ("CI/CD Pipelines", "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc"),
    ("AWS Fundamentals", "https://images.unsplash.com/photo-1603695762547-fba8b9e99b23"),
    ("Azure Basics", "https://images.unsplash.com/photo-1593642532973-d31b6557fa68"),
    ("Google Cloud", "https://images.unsplash.com/photo-1504639725590-34d0984388bd"),
    ("Network Security", "https://images.unsplash.com/photo-1550751827-4bd374c3f58b"),
    ("Ethical Hacking", "https://images.unsplash.com/photo-1555949963-aa79dcee981c"),
    ("Cryptography", "https://images.unsplash.com/photo-1563986768609-322da13575f3"),
    ("Parallel Computing", "https://images.unsplash.com/photo-1581091012184-7e0cdfbb6795"),
    ("Distributed Systems", "https://images.unsplash.com/photo-1526378722370-4b6a28c8f8f7"),
    ("Game Development", "https://images.unsplash.com/photo-1605902711622-cfb43c4437d1"),
    ("UI/UX Design", "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8"),
    ("Data Visualization", "https://images.unsplash.com/photo-1551288049-bebda4e38f71"),
    ("Computer Vision", "https://images.unsplash.com/photo-1507149833265-60c372daea22"),
    ("NLP", "https://images.unsplash.com/photo-1555255707-c07966088b7b"),
    ("Reinforcement Learning", "https://images.unsplash.com/photo-1531746790731-6c087fecd65a"),
]

# -----------------------------
# CREATE COURSES
# -----------------------------
courses = []

for title, image_url in course_data:

    instructor = random.choice(instructors)

    course = Course(
        title=title,
        description=f"This course provides comprehensive knowledge of {title}. "
                    f"It includes theory, practical implementation and real-world applications.",
        thumbnail=image_url,
        instructor_id=instructor.id
    )

    db.session.add(course)
    courses.append(course)

db.session.commit()

print(f"{len(courses)} courses created.")

# -----------------------------
# RANDOM ENROLLMENTS
# -----------------------------
for student in students:

    # Each student gets 2 to 6 random courses
    num_courses = random.randint(2, 6)

    selected_courses = random.sample(courses, num_courses)

    for course in selected_courses:
        enrollment = Enrollment(
            student_id=student.id,
            course_id=course.id
        )
        db.session.add(enrollment)

db.session.commit()

print("Students randomly enrolled (2–6 courses each).")
print("Seeding completed successfully!")