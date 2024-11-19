import pygsheets
from  pathlib import Path
import json

class Package_Google_Sheet:
    def __init__(self , sheetId):
        self.sheetId = sheetId
        self.auth = Path(r".\auth\sheet-access-250701-f43fa8915df5.json")
        self.sheet = self.open_GoogleSheet()
    
    def open_GoogleSheet(self):
        author = pygsheets.authorize(service_file = self.auth)
        git_sheet = author.open_by_key(self.sheetId)
        return git_sheet

    def get_rpa_bnb(self):
        rpa_bnb = []
        sheet_data = self.sheet.worksheet_by_title("rpa_bnb").get_all_records()

        for rpa_bnb_data in sheet_data:
            if not rpa_bnb_data["is_created"] and rpa_bnb_data["mapping_group_id"]:

                rpa_bnb.append({
                    "mapping_group_id" : rpa_bnb_data["mapping_group_id"],
                    "host_id" : rpa_bnb_data["host_id"],
                    "activity_type" : rpa_bnb_data["activity_type"],
                    "activity_name" : rpa_bnb_data["activity_name"],
                    "country_id" : rpa_bnb_data["country_id"],
                    "activity_length" : rpa_bnb_data["行程天數"],
                    "age_restrictions" : rpa_bnb_data["age_restrictions"],
                    "tel_area" : rpa_bnb_data["電話地區"],
                    "phone" : int(rpa_bnb_data["市話1"]),
                    "refund_policy_id" : rpa_bnb_data["refund_policy_id"],
                    "contract" : rpa_bnb_data["契約條款"],
                    "poi_ids" : rpa_bnb_data["poi_ids"],
                    "partner_id" : rpa_bnb_data["partner_id"],
                })

        return rpa_bnb
    
    def get_rpa_dynamicContents(self, group_id):
        dynamicContents = []
        sheet_data = self.sheet.worksheet_by_title("rpa_dynamicContents").get_all_records()

        for data in sheet_data:
            if group_id == data["GroupID"]:
                dynamicContents.append({
                    "title": data["title"],
                    "isShowInNavbar": data["is_show_in_navbar"].upper() == "TRUE",
                    "content": data["content"]
                })

        return dynamicContents

    def get_sheet_data(self, group_id, sheet_name):
        sheet_detail = []
        sheet_data = self.sheet.worksheet_by_title(sheet_name).get_all_records()

        for data in sheet_data:
            if group_id == data["GroupID"]:
                sheet_detail.append({
                    "group_id" : data["GroupID"],
                    "raw_data" : json.loads(data["RawData"])
                })

        return sheet_detail

def update_upload_list(group_id , bnb_id):
    author = pygsheets.authorize(service_file = Path(r".\auth\sheet-access-250701-f43fa8915df5.json"))
    upload_list  = author.open_by_key("1yzW1y5THME-G-A1GpKyvgE33lvXgSNOGi0cCvCHb9-U")
    upload_list_detail = upload_list.worksheet_by_title("Upload list").get_all_records()
    for i , detail in enumerate(upload_list_detail):
        if detail["group_id"] == group_id:
            upload_list.worksheet_by_title("Upload list").update_value((i + 2 , 5) , bnb_id)