import os

DEFAULT_TEAM_USER_PASSWORD = 'Aa123456'
INVOICE_REF_LENGTH = 7
INVOICE_TYPES = {"PAPER": "Paper", "DIGITAL": "Digital"}
BIT_ACCOUNT_NUM = "0529999999"
ORGANIZATION_NAME = "האגודה למלחמה בסרטן"
PAYMENT_TYPES = {"Cash": "Cash", "PayPal": "PayPal", "bit": "bit"}
HOST_URL = os.environ.get("HOST_URL", "http://localhost:5000/")
ESTIMATE_MINUTES_PER_FLOOR = 5
