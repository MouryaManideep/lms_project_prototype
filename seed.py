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
# COURSE LIST
# -----------------------------
course_titles = [
    "Data Structures", "Algorithms", "Operating Systems",
    "Computer Networks", "Database Systems",
    "Machine Learning", "Artificial Intelligence",
    "Web Development", "Cloud Computing",
    "Cyber Security", "Software Engineering",
    "System Design", "Python Programming",
    "Java Programming", "C++ Programming",
    "React Development", "Flask Development",
    "Django Framework", "Microservices Architecture",
    "DevOps Fundamentals", "Docker & Kubernetes",
    "Git & GitHub", "REST API Design",
    "Graph Theory", "Dynamic Programming",
    "Blockchain Basics", "Big Data Analytics",
    "Data Science Fundamentals",
    "Statistics for Engineers",
    "Linear Algebra", "Discrete Mathematics",
    "Computer Architecture", "Linux Administration",
    "Mobile App Development",
    "Android Development",
    "iOS Development",
    "Full Stack Development",
    "Backend Engineering",
    "Frontend Engineering",
    "Testing & QA",
    "CI/CD Pipelines",
    "AWS Fundamentals",
    "Azure Basics",
    "Google Cloud Platform",
    "Network Security",
    "Ethical Hacking",
    "Cryptography",
    "Parallel Computing",
    "Distributed Systems",
    "Game Development",
    "UI/UX Design",
    "Data Visualization",
    "Computer Vision",
    "Natural Language Processing",
    "Reinforcement Learning"
]

# -----------------------------
# CREATE COURSES
# -----------------------------
courses = []

for title in course_titles:
    instructor = random.choice(instructors)

    course = Course(
    title=title,
    description=f"This course provides in-depth knowledge of {title}. "
                f"It includes theory, implementation, and real-world case studies.",
    thumbnail=f"https://picsum.photos/seed/{title.replace(' ', '')}/400/200",
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