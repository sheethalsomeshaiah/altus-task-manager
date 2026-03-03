# Altus Task Manager

A simple Flask web app for managing tasks. Create, edit, complete, and delete tasks. Assignees receive email notifications for every change.

## Features

- **CRUD tasks** — Create, read, update, delete
- **Task fields** — Title, description, assignee email, priority (Low / Medium / High), status (Pending / Completed)
- **Filtering** — Filter tasks by priority and status on the home page
- **Email notifications** — Assignees get an email when a task is:
  - Created (task assigned)
  - Updated
  - Marked complete
  - Deleted
- **Delete confirmation** — Browser confirm dialog before deleting a task

## Tech Stack

- **Backend:** Flask 3.x
- **Database:** SQLite + SQLAlchemy (Flask-SQLAlchemy)
- **Email:** SMTP (e.g. Gmail) via Python `smtplib`
- **Config:** `python-dotenv` for `.env`

## Project Structure

```
Altus Task Manager/
├── app/
│   ├── __init__.py      # App factory, db.create_all()
│   ├── extensions.py    # SQLAlchemy db instance
│   ├── models.py        # Task model
│   ├── routes.py        # Blueprint: index, create, edit, complete, delete
│   ├── email_utils.py   # Send task emails (assigned, updated, completed, deleted)
│   └── templates/
│       ├── index.html       # Task list + filters
│       ├── create_task.html
│       └── edit_task.html
├── instance/
│   └── Altustaskmanagement.db   # SQLite DB (created on first run)
├── run.py               # Entry point
├── requirements.txt
├── .env                 # SMTP and app config (create from below)
└── README.md
```

## Setup

### 1. Clone and enter the project

```bash
cd "Altus Task Manager"
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv myvenv
source myvenv/bin/activate   # On Windows: myvenv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

For **Gmail**, use an [App Password](https://myaccount.google.com/apppasswords) (requires 2-Step Verification). Do not use your normal account password.

**Optional — local debug (no real email):** Use Python’s built-in debug SMTP server so emails are printed in the terminal instead of sent:

```env
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=test@test.com
SMTP_PASSWORD=anything
```

Then in a **separate terminal** run:

```bash
python3 -m smtpd -n -c DebuggingServer localhost:1025
```

Keep that running while you use the app; all “sent” emails will appear in that terminal.

## Run the app

```bash
source myvenv/bin/activate
python3 run.py
```

The app runs at **http://127.0.0.1:5001**.

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Task list with optional `?priority=` and `?status=` filters |
| `/create` | GET, POST | Create a new task |
| `/edit/<id>` | GET, POST | Edit a task |
| `/complete/<id>` | GET | Mark task as completed |
| `/delete/<id>` | GET | Delete task (with confirmation in UI) |

## Email logs

When the app sends (or tries to send) an email, it logs to the **same terminal where Flask is running**:

- `Email sent to <address>` — success
- `Failed to send email: <error>` — SMTP error
- `Email not sent: SMTP_USER or SMTP_PASSWORD not configured.` — missing `.env` credentials

## License

Use as you like.
