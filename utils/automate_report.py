from flask_login import current_user
from models import Report, Notification
from db import db


def generate_automate_report(category):
    description = 'ישנה תקלת מערכת לא צפויה'
    if category == 'paypal':
        description = 'תקלת מערכת בשירות PayPal'
    elif category == 'invoice':
        description = 'תקלת מערכת בשירות החשבונית הירוקה'
    # Post the report only if It's there isn't already an open one with the same description:
    is_report_open = Report.query.filter(Report.description == description, Report.is_open == True).first()
    not None
    if not is_report_open:
        report = Report(category='תקלה באפליקציה',
                        description=description)
        if current_user.team_id:
            report.team_id = current_user.team_id
        db.session.add(report)
        db.session.commit()
        notification = Notification(recipient_id=1,
                                    description=f'דיווח אוטומטי חדש מסוג "{report.category}"  התקבל בעקבות {description} ',
                                    report_id=report.id)
        db.session.add(notification)
        db.session.commit()
