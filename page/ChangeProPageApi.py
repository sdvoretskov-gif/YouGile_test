import requests
import os
from dotenv import load_dotenv
load_dotenv()


class ChangeProject:
    def __init__(self, url) -> None:
        self.url = url

    def project_list(self, project_id: str):
        headers = {'Authorization': f'Bearer {os.getenv("API_TOKEN")}'}
        body = {
            "title": "River-Volga"
        }
        resp = requests.put(
            self.url + '/projects/' + str(project_id), json=body,
            headers=headers)

        print(f"Status: {resp.status_code}")
        print(f"Response body: {resp.text}")
        return resp.json()
