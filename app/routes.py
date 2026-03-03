from flask import Blueprint, render_template, request, redirect, url_for
from .extensions import db
from .models import Task
from .email_utils import send_task_assigned_email, send_task_completed_email, send_task_updated_email, send_task_deleted_email
from datetime import datetime, timezone

main = Blueprint('main', __name__)

# INDEX
@main.route('/')
def index():

    priority_filter = request.args.get('priority', '')
    status_filter = request.args.get('status', '')

    query = Task.query

    if priority_filter:
        query = query.filter_by(priority=priority_filter)

    if status_filter:
        query = query.filter_by(status=status_filter)

    tasks = query.all()

    return render_template('index.html', tasks=tasks,
                           priority_filter=priority_filter,
                           status_filter=status_filter)

# CREATE TASK
@main.route('/create', methods=['GET', 'POST'])
def create_task():

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        assignee_email = request.form.get('assignee_email')
        priority = request.form.get('priority', 'Medium')

        task = Task(
            title=title,
            description=description,
            assignee_email=assignee_email,
            priority=priority
        )

        db.session.add(task)
        db.session.commit()

        send_task_assigned_email(task)

        return redirect(url_for('main.index'))

    return render_template('create_task.html')


# COMPLETE TASK
@main.route('/complete/<int:id>')
def complete_task(id):

    task = Task.query.get(id)

    task.status = "Completed"
    task.completed_date = datetime.now(timezone.utc)

    db.session.commit()

    send_task_completed_email(task)

    return redirect(url_for('main.index'))

# EDIT TASK
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):

    task = Task.query.get_or_404(id)

    if request.method == 'POST':

        task.title = request.form['title']
        task.description = request.form['description']
        task.assignee_email = request.form.get('assignee_email')
        task.status = request.form['status']
        task.priority = request.form.get('priority', 'Medium')

        if task.status == "Completed" and task.completed_date is None:
            task.completed_date = datetime.now(timezone.utc)

        db.session.commit()

        send_task_updated_email(task)

        return redirect(url_for('main.index'))

    return render_template('edit_task.html', task=task)


# DELETE TASK
@main.route('/delete/<int:id>')
def delete_task(id):

    task = Task.query.get_or_404(id)

    send_task_deleted_email(task)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('main.index'))