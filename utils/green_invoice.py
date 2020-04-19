import http.client
from datetime import date
from utils.consts import ORGANIZATION_NAME, PAYMENT_TYPES
import os
import json


def get_bearer_token():
    """
    Creates the bearer key in order to perform requests from the Green Invoice API.
    Since a new key has to be generated at least every 30 mim, this function will be used many times.
    :return: request's bearer login token.
    """

    conn = http.client.HTTPSConnection("sandbox.d.greeninvoice.co.il")
    payload = f"{{\"id\":\"cf4eb537-6eec-4900-affe-e49be73112d3\",\"secret\":\"{os.environ['GREEN_INV_TOKEN']}\"}}"
    headers = {
        'Authorization': f'Basic OWNkMTEyYzItYjRkNi00OTYwLTk2OTQtY2NiMDkyODBjM2Q0OlgyczhXcW5za2JFaVNtbnhvQkUtb0E=',
        'Content-Type': 'application/json',
        'Content-Type': 'text/plain'
    }
    conn.request("POST", "/api/v1/account/token", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    if data.get('errorCode'):
        raise ConnectionError  # unexpected login error
        return False
    return data.get('token')


def get_client_information(token, client_id):
    """
    gets a client's id and returns his information from the Green Invoice DB.
    :param token: request's bearer login token.
    :param client_id: id of the client in the Green Invoice db.
    :return: a dict object containing all the client's information from the Green Invoice DB.
    """

    conn = http.client.HTTPSConnection("sandbox.d.greeninvoice.co.il")
    payload = None
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'text/plain'
    }
    conn.request("GET", f"/api/v1/clients/{client_id}", payload, headers)
    res = conn.getresponse()
    return json.loads(res.read().decode("utf-8"))


def create_new_client(token, name, email, tax_id, address='רחוב סוקולוב 15', city='תל אביב-יפו'):
    """
    Creates a new client for the firm, in order to send him an invoice.
    Note that the sandbox version of green invoice does not allow for two users to have the same name, nor does it allow
    space modifications in the name, therefor if the tax_id is the same, the existing user id will be returned.
    otherwise, a dot ('.') will be added to the client's name.
    :param token: request's bearer login token.
    :param name: name of the client.
    :param email: mail to send future invoices to.
    :param tax_id: personal ID number of the client.
    :param address: client's address.
    :param city: client's city.
    :return: client's user id.
    """

    conn = http.client.HTTPSConnection("sandbox.d.greeninvoice.co.il")
    payload = f"{{\"name\":\"{name}\",\"emails\":[\"{email}\"],\"paymentTerms\": 0,\"taxId\":\"{tax_id}\"," \
              f"\"address\":\"{address}\",\"city\":\"{city}\",\"zip\":\"6291790\",\"country\":\"IL\"," \
              f"\"accountingKey\":\"10202\",\"category\":5,\"subCategory\":501}}".encode('utf-8')
    # Add address when possible

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Content-Type': 'text/plain'
    }
    conn.request("POST", "/api/v1/clients", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    if data.get('errorCode'):
        if data['errorCode'] == 1010:  # Client with this name already exist in the system.
            client_id = data['errorMessage']
            if get_client_information(token, client_id)['taxId'] == tax_id:
                return client_id  # If the existing client has the same ID number, return it's user id.
            else:
                return create_new_client(token, name + '.', email, tax_id)
                # If it has a different ID number, recourse to create a new client, adding a dot to the requested name.
        elif data['errorCode'] == 1111:  # Invalid ID
            raise ValueError()
        else:  # unexpected error
            raise RuntimeError
    return data.get('id')


def payment_type_to_code(payment_type):
    """Gets the method of payment in text, and returns the code numbers necessary for the invoice"""
    app_type = 0
    if payment_type == PAYMENT_TYPES['Cash']:
        p_code = 1
    elif payment_type == PAYMENT_TYPES['PayPal']:
        p_code = 5
    else:  # bit
        p_code = 10
        app_type = 1
    return app_type, p_code


def send_invoice(token, email, client_id, amount, payment_type, org=ORGANIZATION_NAME, to_date=date.today()):
    """
    Gets the client id and payment details, then creates and send an invoice to the email address.
    :param token: request's bearer login token.
    :param email: mail to send the invoice to.
    :param client_id: id of the client in the Green Invoice db.
    :param amount: amount of money donated by the client.
    :param payment_type: method of payment used by the donor.
    :param org: name of the organization the campaign is for.
    :param to_date: date of the donation.
    :return:
    """

    app_type, p_code = payment_type_to_code(payment_type)
    conn = http.client.HTTPSConnection("sandbox.d.greeninvoice.co.il")
    payload = f"{{\"type\": 400,\"date\":\"{to_date}\",\"vatType\":1,\"lang\":\"he\"," \
              f"\"currency\":\"ILS\",\"description\":\"קבלה עבור תרומה ל{org}\",\"remarks\":\"קבלה זו " \
              f"מוכרת לצרכי זיכוי  מס , על פי סעיף 46  לפקודת מס הכנסה\",\"footer\":\"תודה על תרומתך!\"," \
              f"\"client\":{{\"self\": false,\"emails\":[\"{email}\"]," \
              f"\"id\":\"{client_id}\"}},\"rounding\": false,\"signed\":" \
              f"true,\"income\": [{{\"catalogNum\": \"\",\"price\": {amount}," \
              f"\"currency\":\"ILS\",\"currencyRate\": 1,\"quantity\": 1,\"vatType\":1,\"vatRate\": 0}}]," \
              f"\"payment\":[{{\"type\":{p_code},\"appType\":{app_type},\"price\": {amount},\"currency\":" \
              f"\"ILS\",\"currencyRate\": 1,\"date\":\"{to_date}\"}}]}}".encode('utf-8')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/v1/documents", payload, headers)
    data = conn.getresponse().read().decode('utf-8')
    return json.loads(data)['number']  # return ID of the invoice
