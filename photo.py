import base64
import requests
import json

class Photo_File_Uploader:
    def __init__(self, photo, daily_photo, bnb_id):
        self.photo = photo
        self.daily_photo = daily_photo
        self.bnb_id = bnb_id
        self.header = {
            "x-prog-user": "RPA",
            "Content-Type": "application/json",
        }

    def fetch_image_as_base64(self, photo_url):
        try:
            response = requests.get(photo_url)
            response.raise_for_status()
            return base64.b64encode(response.content).decode('utf-8')
        
        except requests.HTTPError as http_e:
            print(f"HTTP error when downloading {photo_url}: {http_e}")

        except Exception as e:
            print(f"An error occurred when downloading {photo_url}: {e}")
            
        return None

    def upload_photo(self, base64_photo):
        image_endpoint = f"https://imgsvc.asiayo.com/api/v1/bnb/{self.bnb_id}/image"
        image_body = {
            "photo": base64_photo
        }
        try:
            response = requests.post(url=image_endpoint, headers=self.header, data=json.dumps(image_body))
            print(response.text)
            response.raise_for_status()
            return json.loads(response.text)["data"]["fileName"]
        except requests.HTTPError as http_e:
            print(f"HTTP error during upload: {http_e}")
        except Exception as e:
            print(f"An error occurred during upload: {e}")
        return False

    def upload_photos_to_image_service(self):
        for photo_data in self.photo:
            photo_url = photo_data["image_url"]
            if photo_url:
                base64_photo = self.fetch_image_as_base64(photo_url)
                if base64_photo:
                    photo_file_name = self.upload_photo(base64_photo)
                    print(photo_file_name)
                    if photo_file_name:
                        photo_data["photoFileName"] = photo_file_name

        for photo_data in self.daily_photo:
            photo_url = photo_data["image_url"]
            if photo_url:
                base64_photo = self.fetch_image_as_base64(photo_url)
                if base64_photo:
                    photo_file_name = self.upload_photo(base64_photo)
                    print(photo_file_name)
                    if photo_file_name:
                        photo_data["photoFileName"] = photo_file_name
        
        return json.dumps({
                "hostId": 37582,
                "journey": {
                    "daily": {
                        "zh-tw": self.daily_photo
                    }
                },
                "photos": self.photo
            })