from typing import Any
import requests
import os
from dotenv import load_dotenv
load_dotenv()


class AuthPage:
    def __init__(self, url) -> None:
        self.url = url

    def get_token(self) -> Any:
        company_id = str(os.getenv("COMPANYID"))
        creds = {
            "login": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD"),
            "companyId": company_id}
        resp = requests.post(self.url + "/auth/keys", json=creds)
        return resp.json()
