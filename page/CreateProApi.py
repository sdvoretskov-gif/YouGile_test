import requests
import os
from dotenv import load_dotenv
load_dotenv()


class CreateProject:
    def __init__(self, url) -> None:
        self.url = url

    def post_project(self):
        headers = {'Authorization': f'Bearer {os.getenv("API_TOKEN")}'}
        user_id = str(os.getenv("USER_ID"))
        body = {
         "title": "New test project",
         "users": {
              user_id: "admin"}
        }
        resp = requests.post(
            self.url + '/projects/', json=body, headers=headers)
        return resp.json()
