import requests 
import json

class Activity():
    def __init__(self):
        # self.body = body
        self.header = {"content-type":"application/json",
                       "x-channel-name":"infra",
                       "x-user":"RPA"
                       }

    def create_activity(self, body):
        try:
            response = requests.post(url = "https://doraemon.beta.asiayo.com/api/v2/activity" , headers = self.header , data = body)
            response.raise_for_status()
            return json.loads(response.text)["data"]["id"]
        except requests.HTTPError as http_e:
            print(f"HTTP error: {http_e}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def update_activity(self, bnb_id, body):
        header = {"content-type":"application/json",
                       "x-channel-name":"infra",
                       "x-user":"RPA",
                       "activityId" : bnb_id
                       }
        try:
            response = requests.put(url = f"https://doraemon.beta.asiayo.com/api/v2/activity/{bnb_id}" , headers = header , data = body)
            response.raise_for_status()
            return json.loads(response.text)["data"]["id"]
        except requests.HTTPError as http_e:
            print(f"HTTP error: {http_e}")

        except Exception as e:
            print(f"An error occurred: {e}")