from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from functools import wraps

app = Flask(__name__)
app.secret_key = "smart-study-planner-secret-key"

DATABASE = "database.db"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            course TEXT,
            year TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject_name TEXT NOT NULL,
            subject_code TEXT,
            priority TEXT DEFAULT 'Medium',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject_id INTEGER,
            task_name TEXT NOT NULL,
            description TEXT,
            deadline TEXT NOT NULL,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject_id INTEGER,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            activity TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject_id INTEGER,
            resource_name TEXT NOT NULL,
            resource_link TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------- LOGIN REQUIRED ----------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


# ---------------- SMART PRIORITY ----------------

def calculate_priority(deadline):
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        days_left = (deadline_date - date.today()).days

        if days_left <= 1:
            return "High"
        elif days_left <= 3:
            return "Medium"
        else:
            return "Low"

    except:
        return "Medium"


# ---------------- HOME ----------------

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        course = request.form["course"]
        year = request.form["year"]

        hashed_password = generate_password_hash(password)

        conn = get_db()

        try:
            conn.execute("""
                INSERT INTO users
                (name, email, password, course, year)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, hashed_password, course, year))

            conn.commit()

            flash("Registration successful! Please login.", "success")

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Email already registered.", "danger")

        finally:
            conn.close()

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
@login_required
def dashboard():

    user_id = session["user_id"]

    conn = get_db()

    total_tasks = conn.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    completed_tasks = conn.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE user_id = ? AND status = 'Completed'
    """, (user_id,)).fetchone()[0]

    pending_tasks = conn.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE user_id = ? AND status = 'Pending'
    """, (user_id,)).fetchone()[0]

    total_subjects = conn.execute("""
        SELECT COUNT(*) FROM subjects
        WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    upcoming_tasks = conn.execute("""
        SELECT tasks.*, subjects.subject_name
        FROM tasks
        LEFT JOIN subjects
        ON tasks.subject_id = subjects.id
        WHERE tasks.user_id = ?
        AND tasks.status = 'Pending'
        ORDER BY tasks.deadline ASC
        LIMIT 5
    """, (user_id,)).fetchall()

    conn.close()

    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    return render_template(
        "dashboard.html",
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        total_subjects=total_subjects,
        progress=progress,
        upcoming_tasks=upcoming_tasks
    )


# ---------------- SUBJECTS ----------------

@app.route("/subjects", methods=["GET", "POST"])
@login_required
def subjects():

    user_id = session["user_id"]

    conn = get_db()

    if request.method == "POST":

        name = request.form["subject_name"]
        code = request.form["subject_code"]
        priority = request.form["priority"]

        conn.execute("""
            INSERT INTO subjects
            (user_id, subject_name, subject_code, priority)
            VALUES (?, ?, ?, ?)
        """, (user_id, name, code, priority))

        conn.commit()

        flash("Subject added successfully.", "success")

    subjects_list = conn.execute("""
        SELECT * FROM subjects
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    conn.close()

    return render_template(
        "subjects.html",
        subjects=subjects_list
    )


@app.route("/delete_subject/<int:id>")
@login_required
def delete_subject(id):

    conn = get_db()

    conn.execute("""
        DELETE FROM subjects
        WHERE id = ? AND user_id = ?
    """, (id, session["user_id"]))

    conn.commit()
    conn.close()

    flash("Subject deleted.", "success")

    return redirect(url_for("subjects"))


# ---------------- TASKS ----------------

@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():

    user_id = session["user_id"]

    conn = get_db()

    if request.method == "POST":

        task_name = request.form["task_name"]
        description = request.form["description"]
        subject_id = request.form["subject_id"]
        deadline = request.form["deadline"]

        priority = calculate_priority(deadline)

        conn.execute("""
            INSERT INTO tasks
            (user_id, subject_id, task_name, description, deadline, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            subject_id,
            task_name,
            description,
            deadline,
            priority
        ))

        conn.commit()

        flash("Task added successfully.", "success")

    tasks_list = conn.execute("""
        SELECT tasks.*, subjects.subject_name
        FROM tasks
        LEFT JOIN subjects
        ON tasks.subject_id = subjects.id
        WHERE tasks.user_id = ?
        ORDER BY tasks.deadline ASC
    """, (user_id,)).fetchall()

    subjects_list = conn.execute("""
        SELECT * FROM subjects
        WHERE user_id = ?
    """, (user_id,)).fetchall()

    conn.close()

    return render_template(
        "tasks.html",
        tasks=tasks_list,
        subjects=subjects_list
    )


@app.route("/complete_task/<int:id>")
@login_required
def complete_task(id):

    conn = get_db()

    conn.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = ? AND user_id = ?
    """, (id, session["user_id"]))

    conn.commit()
    conn.close()

    return redirect(url_for("tasks"))


@app.route("/delete_task/<int:id>")
@login_required
def delete_task(id):

    conn = get_db()

    conn.execute("""
        DELETE FROM tasks
        WHERE id = ? AND user_id = ?
    """, (id, session["user_id"]))

    conn.commit()
    conn.close()

    flash("Task deleted.", "success")

    return redirect(url_for("tasks"))


# ---------------- TIMETABLE ----------------

@app.route("/timetable", methods=["GET", "POST"])
@login_required
def timetable():

    user_id = session["user_id"]

    conn = get_db()

    if request.method == "POST":

        subject_id = request.form["subject_id"]
        day = request.form["day"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        activity = request.form["activity"]

        conn.execute("""
            INSERT INTO timetable
            (user_id, subject_id, day, start_time, end_time, activity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            subject_id,
            day,
            start_time,
            end_time,
            activity
        ))

        conn.commit()

        flash("Study schedule added.", "success")

    timetable_list = conn.execute("""
        SELECT timetable.*, subjects.subject_name
        FROM timetable
        LEFT JOIN subjects
        ON timetable.subject_id = subjects.id
        WHERE timetable.user_id = ?
        ORDER BY
            CASE day
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
            END,
            start_time
    """, (user_id,)).fetchall()

    subjects_list = conn.execute("""
        SELECT * FROM subjects
        WHERE user_id = ?
    """, (user_id,)).fetchall()

    conn.close()

    return render_template(
        "timetable.html",
        timetable=timetable_list,
        subjects=subjects_list
    )


@app.route("/delete_timetable/<int:id>")
@login_required
def delete_timetable(id):

    conn = get_db()

    conn.execute("""
        DELETE FROM timetable
        WHERE id = ? AND user_id = ?
    """, (id, session["user_id"]))

    conn.commit()
    conn.close()

    return redirect(url_for("timetable"))


# ---------------- RESOURCES ----------------

@app.route("/resources", methods=["GET", "POST"])
@login_required
def resources():

    user_id = session["user_id"]

    conn = get_db()

    if request.method == "POST":

        subject_id = request.form["subject_id"]
        resource_name = request.form["resource_name"]
        resource_link = request.form["resource_link"]

        conn.execute("""
            INSERT INTO resources
            (user_id, subject_id, resource_name, resource_link)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            subject_id,
            resource_name,
            resource_link
        ))

        conn.commit()

        flash("Resource added successfully.", "success")

    resources_list = conn.execute("""
        SELECT resources.*, subjects.subject_name
        FROM resources
        LEFT JOIN subjects
        ON resources.subject_id = subjects.id
        WHERE resources.user_id = ?
        ORDER BY resources.id DESC
    """, (user_id,)).fetchall()

    subjects_list = conn.execute("""
        SELECT * FROM subjects
        WHERE user_id = ?
    """, (user_id,)).fetchall()

    conn.close()

    return render_template(
        "resources.html",
        resources=resources_list,
        subjects=subjects_list
    )


@app.route("/delete_resource/<int:id>")
@login_required
def delete_resource(id):

    conn = get_db()

    conn.execute("""
        DELETE FROM resources
        WHERE id = ? AND user_id = ?
    """, (id, session["user_id"]))

    conn.commit()
    conn.close()

    return redirect(url_for("resources"))


# ---------------- PROFILE ----------------

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    user_id = session["user_id"]

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        course = request.form["course"]
        year = request.form["year"]

        conn.execute("""
            UPDATE users
            SET name = ?, course = ?, year = ?
            WHERE id = ?
        """, (name, course, year, user_id))

        conn.commit()

        session["user_name"] = name

        flash("Profile updated successfully.", "success")

    user = conn.execute("""
        SELECT * FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


# ---------------- START APP ----------------

if __name__ == "__main__":
    init_db()

    app.run(debug=True)
