from . import db
from datetime import datetime, timezone

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)
    
    assignee_email = db.Column(db.String(100), nullable=True)

    priority = db.Column(db.String(20), default="Medium")

    created_date = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    completed_date = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )