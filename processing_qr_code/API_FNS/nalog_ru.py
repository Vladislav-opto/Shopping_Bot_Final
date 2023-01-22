"""
This module take from https://github.com/valiotti/get-receipts.git
"""
import requests
from settings_box.settings import CLIENT_SECRET, HEADERS, NALOG_URL

class NalogRuPython:

    def __init__(self, phone_number, code = 0):
        self.session_id = None
        self.phone = phone_number
        self.code = code

    def sends_sms_to_the_user(self):
        """Sends a phone number, receives a code."""
        url = f'https://{NALOG_URL}/auth/phone/request'
        payload = {
            'phone': self.phone,
            'client_secret': CLIENT_SECRET,
            'os': 'Android',
        }

        response = requests.post(url, json=payload, headers=HEADERS)


    def sends_code_to_nalog(self):
        """sends the code to the server, opens the session."""

        url = f'https://{NALOG_URL}/auth/phone/verify'
        payload = {
            'phone': self.phone,
            'client_secret': CLIENT_SECRET,
            'code': self.code,
            'os': 'Android',
        }
        response = requests.post(url, json=payload, headers=HEADERS)
        code_response = str(response.status_code)
        if code_response[0] == '2':
            self.session_id = response.json()['sessionId']
            self.refresh_token = response.json()['refresh_token']
            return True
        else:
            return False


    def refresh_token_function(self) -> None:
        """Refresh token."""
        url = f'https://{NALOG_URL}/mobile/users/refresh'
        payload = {
            'refresh_token': self.refresh_token,
            'client_secret': CLIENT_SECRET,
        }

        response = requests.post(url, json=payload, headers=HEADERS)

        self.session_id = response.json()['sessionId']
        self.refresh_token = response.json()['refresh_token']

    def _get_ticket_id(self, qr: str) -> str:
        """
        Get ticker id by info from qr code
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: Ticket id. Example "5f3bc6b953d5cb4f4e43a06c"
        """
        url = f'https://{NALOG_URL}/ticket'
        payload = {'qr': qr}

        HEADERS['sessionId'] = self.session_id

        response = requests.post(url, json=payload, headers=HEADERS)

        return response.json()['id']

    def get_ticket(self, qr: str) -> dict:
        """
        Get JSON ticket
        :param qr: text from qr code. Example "t=20200727T174700&s=746.00&fn=9285000100206366&i=34929&fp=3951774668&n=1"
        :return: JSON ticket
        """
        ticket_id = self._get_ticket_id(qr)
        url = f'https://{NALOG_URL}/tickets/{ticket_id}'

        HEADERS['Content-Type'] = 'application/json'

        response = requests.get(url, headers=HEADERS)

        return response.json()
