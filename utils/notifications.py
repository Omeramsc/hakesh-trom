from flask_login import current_user
from db import db
from models import Notification


def update_notification_readtime():
    notifications_query = Notification.query
    notifications_query = notifications_query.filter(Notification.recipient_id == current_user.id)
    notifications_query = notifications_query.all()
    for notification in notifications_query:
        notification.was_read = True
        db.session.commit()
