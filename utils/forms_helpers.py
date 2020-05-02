import datetime
import json

report_categories = ["", "אין גישה", "בניין נעול", "הצפה", "כלב משוחרר", "מפגע", "רחוב חסום", "תקלה באפליקציה",
                     "אחר"]


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


def memoize_dropdown(func):
    """Checks if the dropdown list has already been created.
    If it did, it returns the cached list. otherwise, it creates one.
    """

    dropdown_cache = []

    def wrapper():
        if not dropdown_cache:
            for city in func():
                dropdown_cache.append((city, city))
        return dropdown_cache

    return wrapper


@memoize_dropdown
def read_cities():
    """Reads the city-list files, while putting 'Tel-Aviv' first and ignoring tribes & settlement."""
    with open('static/israel-cities.json', 'r', encoding="utf8") as data:
        data = json.load(data)
    yield 'תל - אביב - יפו'
    for line in data:
        if ")" not in line.get('name'):
            yield line.get('name')
