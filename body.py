import json

class ActivityBody:
    def __init__(self, rpa_bnb_data, journey, journey_daily, itinerary_highlight, dynamicContents) -> list:
        self.rpa_bnb_data = rpa_bnb_data
        self.journey = journey
        self.journey_daily = journey_daily
        self.itinerary_highlight = itinerary_highlight
        self.dynamicContents = dynamicContents
        self.default_photo = "desc_Ec2CX0l68TIqDg.webp"

    def create_daily(self) -> list:
        daily_array = [
            {
                "photoFileName": self.default_photo,
                "image_url": daily["raw_data"].get("image_url", ""),
                "description": daily["raw_data"].get("description", ""),
                "summary": daily["raw_data"].get("summary", ""),
                "breakfast": daily["raw_data"].get("breakfast", ""),
                "lunch": daily["raw_data"].get("lunch", ""),
                "dinner": daily["raw_data"].get("dinner", ""),
                "accommodation": daily["raw_data"].get("accommodation", "")
            }
            for daily in self.journey_daily
        ]
        return daily_array

    def create_itinerary_highlight(self) -> list:
        return [
            {
                "content": highlight["raw_data"]["content"],
                "photos": [
                    {
                        "photoFileName": self.default_photo,
                        "description": highlight["raw_data"].get("content", "")
                    }
                ]
            }
            for highlight in self.itinerary_highlight
        ]

    def generate_contacts(self) -> list:
        return {
            "tels": [
                {
                    "region": self.rpa_bnb_data["tel_area"],
                    "value": self.rpa_bnb_data["phone"]
                }
            ]
        }

    def generate_photos(self) -> list:
        num_photos = max(6, len(self.journey[0]["raw_data"]["image_urls"].split(",")))
        
        return [{"photoFileName": self.default_photo, "description": "","image_url": ""} for _ in range(num_photos)]

    def activity_body(self) -> list:
        daily = self.create_daily()
        highlight = self.create_itinerary_highlight()
        
        body = {
            "type": self.rpa_bnb_data["activity_type"],
            "hostId": self.rpa_bnb_data["host_id"],
            "partner": {
                "id": self.rpa_bnb_data["partner_id"],
                "activityId": self.rpa_bnb_data["mapping_group_id"]
            },
            "names": {
                "zh-tw": self.rpa_bnb_data["activity_name"],
                "en-us": self.rpa_bnb_data["activity_name"]
            },
            "countryId": int(self.rpa_bnb_data["country_id"]),
            "poiIds": json.loads(self.rpa_bnb_data["poi_ids"]),
            "days": int(self.rpa_bnb_data["activity_length"]),
            "houseRule": {
                "ageProhibited": self.rpa_bnb_data["age_restrictions"]
            },
            "journey": {
                "overview": self.journey[0]["raw_data"]["journey"]["overview"],
                "daily": {"zh-tw": daily}
            },
            "contacts": self.generate_contacts(),
            "showMemberPricing": {
                "asiayo": True,
                "gha": False
            },
            "refundPolicyId": self.rpa_bnb_data["refund_policy_id"],
            "contracts": {"zh-tw": self.rpa_bnb_data["contract"]},
            "photos": self.generate_photos(),
            "dynamicContents": {
                "zh-tw": self.dynamicContents
            },
            "summaryContents": self.journey[0]["raw_data"]["summaryContents"],
            "departure": self.journey[0]["raw_data"]["departure"],
            "highlightContents": {"zh-tw": highlight}
        }

        return json.dumps(body)