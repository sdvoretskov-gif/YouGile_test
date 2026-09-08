import os
import requests
from dotenv import load_dotenv
load_dotenv()


class GetCompany:
    def __init__(self, url) -> None:
        self.url = url

    def get_company_list(self):
        headers = {'Authorization': f'Bearer {os.getenv("API_TOKEN")}'}
        creds = {
            "login": "sdvoretskov@inbox.ru",
            "password": "nug-dBP-5DM-D23",
            "name": "Сергей Д"
        }
        resp = requests.post(
            self.url + 'auth/companies/', json=creds, headers=headers)
        return resp.json()
