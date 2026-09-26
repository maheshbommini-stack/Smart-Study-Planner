📚 Smart Study Planner

Smart Study Planner is a web-based application designed to help students organize their studies, manage academic tasks, create study schedules, store learning resources, and track their study progress in one place.

🎯 Project Objective

The main objective of Smart Study Planner is to provide students with a simple and user-friendly platform to:

- Manage subjects
- Create and manage study tasks
- Organize a study timetable
- Track completed and pending tasks
- Store useful study resources
- Monitor overall study progress
- Identify task priority based on deadlines

---

✨ Features

🔐 User Authentication

- Student registration
- Student login
- Secure password hashing
- Logout functionality

📊 Dashboard

The dashboard provides an overview of the student's study activities.

It displays:

- Total subjects
- Total tasks
- Completed tasks
- Pending tasks
- Overall study progress
- Upcoming tasks

📚 Subject Management

Students can:

- Add subjects
- Add subject codes
- Set subject priority
- Delete subjects

📝 Task Management

Students can:

- Create study tasks
- Add task descriptions
- Assign tasks to subjects
- Set deadlines
- Mark tasks as completed
- Delete tasks

🧠 Smart Task Priority

The system automatically calculates task priority based on the deadline:

Deadline| Priority
1 day or less| High
2–3 days| Medium
More than 3 days| Low

📅 Study Timetable

Students can create their own study schedule by selecting:

- Subject
- Day
- Start time
- End time
- Study activity

📖 Study Resources

Students can save useful learning resources such as:

- Notes
- Websites
- Videos
- Documentation
- Online learning materials

📈 Progress Tracking

The application automatically calculates study progress based on completed tasks.

Formula:

Progress = (Completed Tasks / Total Tasks) × 100

👤 Profile

Students can manage:

- Name
- Course
- Year
- Email information

---

🛠️ Technologies Used

Frontend

- HTML5
- CSS3
- JavaScript

Backend

- Python
- Flask

Database

- SQLite

Other

- Jinja2 Templates
- Werkzeug Password Hashing

---

📂 Project Structure

Smart-Study-Planner/
│
├── app.py
│
├── database.db
│
├── requirements.txt
│
├── README.md
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── subjects.html
│   ├── tasks.html
│   ├── timetable.html
│   ├── resources.html
│   └── profile.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    └── js/
        └── script.js

«"database.db" is automatically created when the application is started for the first time.»

---

⚙️ Installation

1. Clone the Repository

git clone https://github.com/your-username/Smart-Study-Planner.git

Move into the project directory:

cd Smart-Study-Planner

2. Create a Virtual Environment

Windows

python -m venv venv

Activate it:

venv\Scripts\activate

Linux / macOS

python3 -m venv venv

Activate it:

source venv/bin/activate

---

📦 Install Dependencies

Run:

pip install -r requirements.txt

If you don't have "requirements.txt", install the packages manually:

pip install flask werkzeug

---

▶️ Run the Application

Run:

python app.py

The application will start on:

http://127.0.0.1:5000

Open the address in your web browser.

---

🔑 Application Flow

Register
   ↓
Login
   ↓
Dashboard
   ↓
┌───────────────┐
│   Subjects    │
├───────────────┤
│     Tasks     │
├───────────────┤
│   Timetable   │
├───────────────┤
│   Resources   │
├───────────────┤
│    Profile    │
└───────────────┘
   ↓
Track Study Progress

---

🗄️ Database Structure

The application uses SQLite with the following tables:

Users

Stores student account information.

id
name
email
password
course
year

Subjects

Stores student subjects.

id
user_id
subject_name
subject_code
priority

Tasks

Stores study tasks.

id
user_id
subject_id
task_name
description
deadline
priority
status

Timetable

Stores study schedules.

id
user_id
subject_id
day
start_time
end_time
activity

Resources

Stores study resources.

id
user_id
subject_id
resource_name
resource_link

---

🔒 Security

The project includes basic security features:

- Passwords are hashed using Werkzeug.
- User sessions are used for authentication.
- Users can access only their own subjects, tasks, schedules, and resources.
- Login is required for protected pages.

«For a production application, additional security measures such as CSRF protection, stronger session configuration, input validation, and secure secret management should be added.»

---

🚀 Future Enhancements

The project can be extended with:

- 🔔 Study reminders
- 📧 Email notifications
- 🤖 AI-based study recommendations
- 📅 Calendar integration
- 🌙 Dark mode
- 📊 Detailed study analytics
- 🔥 Daily study streak
- 📱 Mobile application
- 🏆 Achievement system
- 🔐 Two-factor authentication

---

🎓 Academic Information

Project Title: Smart Study Planner

Domain: Web Technology

Frontend: HTML, CSS, JavaScript

Backend: Python Flask

Database: SQLite

Project Type: Web Application

---

👨‍💻 Project Purpose

This project demonstrates the practical implementation of web development concepts including:

- Frontend development
- Backend development
- Database connectivity
- CRUD operations
- User authentication
- Session management
- Dynamic web pages
- Form handling
- Data validation
- Progress calculation

---

📄 License

This project is developed for educational and academic purposes.
