import datetime


def get_campaign_icon(d1):
    d2 = datetime.date.today()
    if d1 > d2:
        return "static/didnt_begin.png"
    elif d2 > d1:
        return "static/done.png"
    return "static/in_progress.png"
