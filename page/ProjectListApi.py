import requests
import os
from dotenv import load_dotenv
load_dotenv()


class GetProjectList:
    def __init__(self, url) -> None:
        self.url = url

    def project_list(self):
        headers = {'Authorization': f'Bearer {os.getenv("API_TOKEN")}'}
        resp = requests.get(
            self.url + '/projects/', headers=headers)
        return resp.json()
