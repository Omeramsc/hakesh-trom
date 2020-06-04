from flask_login import current_user
from db import db
from models import Notification


def update_notification_status_to_read():
    notifications_query = Notification.query.filter(Notification.recipient_id == current_user.id).filter(
        Notification.was_read == False)
    notifications_query = notifications_query.all()
    for notification in notifications_query:
        notification.was_read = True
    db.session.commit()


def create_new_notification(recipient_id, report, description=None):
    notification = Notification(recipient_id=recipient_id,
                                description=description or f'דיווח חדש מסוג "{report.category}" התקבל מאת צוות {current_user.team_id}',
                                report_id=report.id)
    db.session.add(notification)
    db.session.commit()
