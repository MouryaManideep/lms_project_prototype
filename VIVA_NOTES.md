# VIVA Notes — LMS Project Prototype

## 1. One-line Elevator Pitch

A minimal Learning Management System prototype allowing instructors to create courses and students to register and enroll, demonstrating role-based views and server-rendered Flask pages.

## 2. Purpose & Audience

- Purpose: Demo an MVP LMS with core flows (auth, course CRUD, enrollment).
- Audience: Instructors, demo reviewers, or as a class project showcase.

## 3. Key Features to Highlight

- Registration, login, and role-based dashboards (instructor vs student).
- Course creation, editing, and listing.
- Student enrollment and viewing enrolled courses.
- Instructor view of enrolled students.
- Server-rendered templates using Jinja2; small, easy-to-extend codebase.

## 4. Tech Stack

- Python 3.14
- Flask (app framework)
- SQLAlchemy (ORM)
- Flask-WTF (forms)
- Jinja2 (templating)
- Virtualenv in `lmsReq` for environment

## 5. Architecture & Important Files

- `run.py` — application entrypoint.
- `config.py` — configuration (DB URI, secret key).
- `app/__init__.py` — app factory and extension init.
- `app/routes.py` — main routes (home, courses, dashboards).
- `app/auth.py` — registration and login logic.
- `app/models.py` — `User`, `Course`, and enrollment relations.
- `app/decorators.py` — role-restriction helpers.
- `templates/` — Jinja2 templates (views referenced by routes).

## 6. Data Model Summary

- User: id, name/email, password_hash, role (student/instructor).
- Course: id, title, description, instructor_id.
- Enrollment: many-to-many association between users (students) and courses.
  (See `app/models.py` for exact fields and relationships.)

## 7. Authentication & Authorization Flow

- Registration: validate form → hash password → create `User`.
- Login: validate credentials → create session (Flask-Login or session cookie).
- Authorization: decorator-based checks in `app/decorators.py` to guard instructor routes.
- Security notes: passwords are hashed; secret key in `config.py` secures sessions.

## 8. Routes & What to Demo

- Home (`/`) — landing.
- Register (`/register`) / Login (`/login`) — auth flows.
- Create Course (`/create_course`) — instructor-only.
- Edit Course (`/edit_course/<id>`) — instructor-only.
- Course Students (`/course_students/<id>`) — list enrolled students.
- Dashboard(s) — instructor sees courses; student sees enrollments.
  (Exact route names: check `app/routes.py`.)

## 9. Setup & Run (Windows)

PowerShell:

```powershell
python -m venv lmsReq
.\lmsReq\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

CMD:

```cmd
python -m venv lmsReq
lmsReq\Scripts\activate.bat
pip install -r requirements.txt
python run.py
```

Optional: `python seed.py` to populate demo data.

## 10. Short Demo Script (3–6 minutes)

1. Start app and open browser to home.
2. Register as an instructor and create a course.
3. Register as a student, enroll in the course, show student dashboard.
4. Switch back to instructor view and open the enrolled students list.
5. Explain code layout and how to extend features (API, migrations).

## 11. FAQs / Expected Questions

- How is data persisted? — SQLAlchemy models + configured DB in `config.py`.
- How to add roles? — extend `User.role` and update `decorators.py` checks.
- How to test? — add pytest unit tests for routes and models; use a test DB.
- How to migrate DB? — integrate Flask-Migrate (Alembic).

## 12. Future Improvements (talking points)

- Add REST API + SPA frontend or mobile client.
- Add DB migrations and CI tests.
- Introduce OAuth / multi-factor auth.
- Add role-based permissions (TA/admin) and audit logs.
- Improve UI/UX and accessibility.

---

If you want a PDF or slide-ready one-page version, tell me the format and I will export it.
