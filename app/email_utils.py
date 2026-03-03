import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_task_email(to_email, subject, body):
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    if not smtp_user or not smtp_password:
        print("Email not sent: SMTP_USER or SMTP_PASSWORD not configured.")
        return

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if smtp_port != 1025:
                server.starttls()
                server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def send_task_assigned_email(task):
    if not task.assignee_email:
        return

    subject = f"[Altus] Task Assigned: {task.title}"
    body = (
        f"Hello,\n\n"
        f"A new task has been assigned to you.\n\n"
        f"Title:       {task.title}\n"
        f"Description: {task.description or 'N/A'}\n"
        f"Priority:    {task.priority}\n"
        f"Status:      {task.status}\n"
        f"Created:     {task.created_date}\n\n"
        f"Please log in to Altus Task Manager to view or update the task.\n\n"
        f"— Altus Task Manager"
    )
    send_task_email(task.assignee_email, subject, body)


def send_task_updated_email(task):
    if not task.assignee_email:
        return

    subject = f"[Altus] Task Updated: {task.title}"
    body = (
        f"Hello,\n\n"
        f"A task assigned to you has been updated.\n\n"
        f"Title:       {task.title}\n"
        f"Description: {task.description or 'N/A'}\n"
        f"Assignee:    {task.assignee_email}\n"
        f"Priority:    {task.priority}\n"
        f"Status:      {task.status}\n\n"
        f"Please log in to Altus Task Manager to view the task.\n\n"
        f"— Altus Task Manager"
    )
    send_task_email(task.assignee_email, subject, body)


def send_task_deleted_email(task):
    if not task.assignee_email:
        return

    subject = f"[Altus] Task Deleted: {task.title}"
    body = (
        f"Hello,\n\n"
        f"The following task assigned to you has been deleted.\n\n"
        f"Title:       {task.title}\n"
        f"Description: {task.description or 'N/A'}\n"
        f"Priority:    {task.priority}\n"
        f"Status:      {task.status}\n\n"
        f"— Altus Task Manager"
    )
    send_task_email(task.assignee_email, subject, body)


def send_task_completed_email(task):
    if not task.assignee_email:
        return

    subject = f"[Altus] Task Completed: {task.title}"
    body = (
        f"Hello,\n\n"
        f"The following task has been marked as completed.\n\n"
        f"Title:          {task.title}\n"
        f"Description:    {task.description or 'N/A'}\n"
        f"Priority:       {task.priority}\n"
        f"Completed Date: {task.completed_date}\n\n"
        f"— Altus Task Manager"
    )
    send_task_email(task.assignee_email, subject, body)
