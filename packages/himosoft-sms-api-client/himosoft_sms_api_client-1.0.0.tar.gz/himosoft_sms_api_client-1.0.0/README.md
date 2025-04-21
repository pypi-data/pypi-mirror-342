
# Himosoft SMS API Client

The **Himosoft SMS API Client** is a Python client that interacts with the Himosoft SMS API, enabling you to send SMS messages, check the status of sent messages, and retrieve transaction details. This client supports automatic retries in case of transient errors, making it reliable for production environments.

## Installation

```bash
pip install himosoft-sms-api-client

```

# Initialize

```python
from sms_api_client import SMSApiClient

client = SMSApiClient(
    base_url="http://localhost:8000",  # Replace with your API base URL
    sms_api_key="your-api-key",  # Replace with your SMS API key
    transaction_api_key="your-transaction-api-key"  # Replace with your transaction API key (Optional)
)
```
# Send SMS
```python
send_response = client.send_sms("8801xxxxxxx", "Your message")
print(send_response)  # The response from the API will be printed
```

# Example Send SMS response
```json
{
    "status": "success",
    "message_id": "message-id"
}
```

# Check SMS status report
```python
report_response = client.check_sms_report("your-message-id")
print(report_response)  # The delivery report will be printed
```

# BKash Payment Transaction status
```python
status_response = client.bkash_transaction_status("your-transaction-code")
print(status_response)
```
