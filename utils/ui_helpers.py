import datetime
import math


def get_campaign_icon(d1):
    d2 = datetime.date.today()
    if d1 > d2:
        return "static/didnt_begin.png"
    elif d2 > d1:
        return "static/done.png"
    return "static/in_progress.png"


def get_report_status_icon(is_open):
    if is_open:
        return "static/report_open.png"
    return "static/report_closed.png"


def pretty_time(minutes):
    if minutes < 60:
        return "{} דקות".format(minutes)

    parsed_hours = math.floor(minutes / 60)
    if parsed_hours == 1:
        parsed_hours = "שעה"
    elif parsed_hours == 2:
        parsed_hours = "שעתיים"
    else:
        parsed_hours = "{} שעות".format(parsed_hours)

    parsed_minutes = minutes % 60
    if parsed_minutes == 0:
        parsed_minutes = ""
    elif parsed_minutes == 1:
        parsed_minutes = "ודקה"
    else:
        parsed_minutes = "ו-{} דקות".format(parsed_minutes)

    return "{parsed_hours} {parsed_minutes}".format(parsed_hours=parsed_hours, parsed_minutes=parsed_minutes).strip()
