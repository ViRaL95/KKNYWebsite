from SECRETS.secrets import PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY
import requests
from datetime import datetime

def retrieve_donors():
    authorization_request = \
        requests.post("https://api.paypal.com/v1/oauth2/token", headers={"Accept": "application/json",
                                                                        "Accept-Language": "en_US"},
                     auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY),
                     data={"grant_type": "client_credentials"})

    print(PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY)
    token = authorization_request.json()['access_token']
    ia_header = {"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"}

    start_date = datetime(2020, 5, 17)
    current_date  = datetime.now().date()
    start_date_str = datetime.strftime(start_date, '%Y-%m-%dT%H:%M:%SZ')
    current_date_str = datetime.strftime(current_date, '%Y-%m-%dT%H:%M:%SZ')

    answer = requests.get("https://api.paypal.com/v1/reporting/transactions", headers=ia_header,
                          params={"start_date": start_date_str, "end_date": current_date_str,
                                  "transaction_type": "T0013",
                                  "fields": "payer_info"})

    payment_info = {payer['payer_info']['payer_name']['alternate_full_name']: payer['transaction_info']['transaction_amount']['value']
                    for payer in answer.json()['transaction_details']}


    payment_info_sorted = []
    for user, amount in sorted(payment_info.items(), key=lambda item: float(item[1]), reverse=True):
        payment_info_sorted.append(user)
    return payment_info_sorted
