import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time

# Set up retry mechanism
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

class SMSApiClient:
    def __init__(self, base_url: str, sms_api_key: str = None, transaction_api_key: str = None):
        self.base_url = base_url.rstrip('/') 
        self.sms_api_key = sms_api_key
        self.transaction_api_key = transaction_api_key

        self.sms_headers = {
            "Content-Type": "application/json",
        }

        if self.sms_api_key:
            self.sms_headers["X-API-Key"] = self.sms_api_key

    def send_sms(self, phone_number: str, message: str):
        if not self.base_url or not self.sms_api_key:
            raise ValueError("base URL and SMS API key must be provided to use this feature.")
        
        url = f"{self.base_url}/sms/send/"
        payload = {
            "phone_number": phone_number,
            "message": message
        }
        response = session.post(url, json=payload, headers=self.sms_headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def check_sms_report(self, message_id: str):
        
        if not self.base_url or not self.sms_api_key:
            raise ValueError("base URL and SMS API key must be provided to use this feature.")
        
        url = f"{self.base_url}/sms/report/"
        payload = {
            "message_id": message_id
        }
        time.sleep(5)
        response = session.post(url, json=payload, headers=self.sms_headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def bkash_transaction_status(self, code: str):
        if not self.base_url or not self.transaction_api_key:
            raise ValueError("base URL and Transaction API key must be provided to use this feature.")

        url = f"{self.base_url}/webhook/read/{code}/?api_key={self.transaction_api_key}"
        headers = {
            "Accept": "application/json"
        }
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
