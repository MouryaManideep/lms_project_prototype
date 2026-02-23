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
    ("Data Structures", "https://loremflickr.com/640/360/datastructure,coding"),
    ("Algorithms", "https://loremflickr.com/640/360/algorithm,math"),
    ("Operating Systems", "https://loremflickr.com/640/360/operatingsystem,linux"),
    ("Computer Networks", "https://loremflickr.com/640/360/network,server"),
    ("Database Systems", "https://loremflickr.com/640/360/database,sql"),
    ("Machine Learning", "https://loremflickr.com/640/360/machinelearning,neural"),
    ("Artificial Intelligence", "https://loremflickr.com/640/360/ai,robot"),
    ("Web Development", "https://loremflickr.com/640/360/webdesign,html"),
    ("Cloud Computing", "https://loremflickr.com/640/360/cloud,server"),
    ("Cyber Security", "https://loremflickr.com/640/360/cybersecurity,hacker"),
    ("Software Engineering", "https://loremflickr.com/640/360/software,coding"),
    ("System Design", "https://loremflickr.com/640/360/architecture,system"),
    ("Python Programming", "https://loremflickr.com/640/360/python,code"),
    ("Java Programming", "https://loremflickr.com/640/360/java,programming"),
    ("C++ Programming", "https://loremflickr.com/640/360/cpp,programming"),
    ("React Development", "https://loremflickr.com/640/360/reactjs,javascript"),
    ("Flask Development", "https://loremflickr.com/640/360/flask,python"),
    ("Django Framework", "https://loremflickr.com/640/360/django,backend"),
    ("Microservices", "https://loremflickr.com/640/360/microservices,cloud"),
    ("DevOps", "https://loremflickr.com/640/360/devops,automation"),
    ("Docker & Kubernetes", "https://loremflickr.com/640/360/docker,container"),
    ("Git & GitHub", "https://loremflickr.com/640/360/git,github"),
    ("REST API Design", "https://loremflickr.com/640/360/api,web"),
    ("Graph Theory", "https://loremflickr.com/640/360/graph,nodes"),
    ("Dynamic Programming", "https://loremflickr.com/640/360/math,recursion"),
    ("Blockchain", "https://loremflickr.com/640/360/blockchain,crypto"),
    ("Big Data", "https://loremflickr.com/640/360/bigdata,analytics"),
    ("Data Science", "https://loremflickr.com/640/360/datascience,analysis"),
    ("Statistics", "https://loremflickr.com/640/360/statistics,chart"),
    ("Linear Algebra", "https://loremflickr.com/640/360/mathematics,matrix"),
    ("Discrete Math", "https://loremflickr.com/640/360/logic,math"),
    ("Computer Arch", "https://loremflickr.com/640/360/cpu,motherboard"),
    ("Linux Admin", "https://loremflickr.com/640/360/linux,terminal"),
    ("Mobile App Dev", "https://loremflickr.com/640/360/mobile,app"),
    ("Android Dev", "https://loremflickr.com/640/360/android,phone"),
    ("iOS Dev", "https://loremflickr.com/640/360/iphone,swift"),
    ("Full Stack", "https://loremflickr.com/640/360/fullstack,coding"),
    ("Backend Eng", "https://loremflickr.com/640/360/backend,server"),
    ("Frontend Eng", "https://loremflickr.com/640/360/frontend,ui"),
    ("Testing & QA", "https://loremflickr.com/640/360/testing,software"),
    ("CI/CD Pipelines", "https://loremflickr.com/640/360/automation,pipeline"),
    ("AWS Fundamentals", "https://loremflickr.com/640/360/aws,cloud"),
    ("Azure Basics", "https://loremflickr.com/640/360/azure,cloud"),
    ("Google Cloud", "https://loremflickr.com/640/360/gcp,google"),
    ("Network Security", "https://loremflickr.com/640/360/firewall,security"),
    ("Ethical Hacking", "https://loremflickr.com/640/360/hacking,code"),
    ("Cryptography", "https://loremflickr.com/640/360/encryption,key"),
    ("Parallel Computing", "https://loremflickr.com/640/360/parallel,supercomputer"),
    ("Distributed Systems", "https://loremflickr.com/640/360/nodes,distributed"),
    ("Game Development", "https://loremflickr.com/640/360/gamedev,unity"),
    ("UI/UX Design", "https://loremflickr.com/640/360/uiux,design"),
    ("Data Visualization", "https://loremflickr.com/640/360/dataviz,charts"),
    ("Computer Vision", "https://loremflickr.com/640/360/computervision,face"),
    ("NLP", "https://loremflickr.com/640/360/nlp,text"),
    ("Reinforcement Learning", "https://loremflickr.com/640/360/robotics,learning"),
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