import datetime


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
