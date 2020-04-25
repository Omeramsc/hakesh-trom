import paypalrestsdk
import os
from utils.consts import ORGANIZATION_NAME

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": os.environ['PAYPAL_CLIENT'],
    "client_secret": os.environ['PAYPAL_TOKEN']})


def create_payment(amount, return_url, cancel_url, org=ORGANIZATION_NAME):
    try:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "experience_profile_id": "XP-3YAL-A7TU-M7ZW-AMTU",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "תרומה",
                        "price": amount,
                        "currency": "ILS",
                        "quantity": 1}]},
                "amount": {
                    "total": amount,
                    "currency": "ILS"},
                "description": f"תרומה ל{org}"}]})
        if payment.create():
            return payment
        else:
            raise RuntimeError
    except paypalrestsdk.exceptions.UnauthorizedAccess:
        raise ConnectionError


def authorize_payment(payment):
    for link in payment.links:
        if link.rel == "approval_url":
            # Convert to str to avoid Google App Engine Unicode issue
            approval_url = str(link.href)
            return approval_url


def execute_payment(pp_req):
    payment = paypalrestsdk.Payment.find(pp_req['paymentId'])
    if payment.execute({"payer_id": pp_req['PayerID']}):
        return True
    return False
