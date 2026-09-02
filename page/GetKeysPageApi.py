from typing import Any
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class KeysPage:
    def __init__(self, url) -> None:
        self.url = url

    def get_keys(self) -> Any:
        company_id = str(os.getenv("COMPANYID"))
        creds = {
            "login": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD"),
            "companyId": company_id}
        resp = requests.post(self.url + "/auth/keys/get", json=creds)
        return resp.json()
