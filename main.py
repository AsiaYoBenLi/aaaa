from Google_Sheet import Package_Google_Sheet ,update_upload_list
from body import ActivityBody
from activity import Activity
from photo import Photo_File_Uploader
from datetime import datetime


def main():
    package_Google_Sheet = Package_Google_Sheet("1Cf008hrQgv4pnxaDmatN_Mwx8XLBHrLTwhWfWBpSt7I")
    rpa_bnb = package_Google_Sheet.get_rpa_bnb()
    activity_data = []

    for rpa_bnb_data in rpa_bnb:
        group_id = rpa_bnb_data["mapping_group_id"]
        journey = package_Google_Sheet.get_sheet_data(group_id = group_id , sheet_name = "journey")
        journey_daily = package_Google_Sheet.get_sheet_data(group_id = group_id , sheet_name = "journey_daily")
        itinerary_highlight = package_Google_Sheet.get_sheet_data(group_id = group_id, sheet_name = "itinerary_highlight")
        dynamicContents = package_Google_Sheet.get_rpa_dynamicContents(group_id = group_id)

        create_activity_body = ActivityBody(rpa_bnb_data, journey, journey_daily, itinerary_highlight, dynamicContents)
        body = create_activity_body.activity_body()
        photo = create_activity_body.generate_photos()
        daily_photo = create_activity_body.create_daily()

        activity_data.append({
            group_id : {
                "body" : body,
                "bnb_id" : "",
                "photo" : photo,
                "daily_photo" : daily_photo
            }
        })

    for data in activity_data:
        for group_ids, content in data.items():
            activity = Activity()
            bnb_id = activity.create_activity(content["body"])
            content["bnb_id"] = str(bnb_id)
            photo_uploader = Photo_File_Uploader(photo = content["photo"], daily_photo = content["daily_photo"], bnb_id = content["bnb_id"])
            result = photo_uploader.upload_photos_to_image_service()
            # print(result)
            api_result = activity.update_activity(content["bnb_id"] ,result)
            print(api_result)
            # update_upload_list(group_ids , bnb_id)

if __name__ == "__main__":
    start_time = datetime.now()
    print("開始時間:", start_time)

    main()

    end_time = datetime.now()
    print("結束時間:", end_time)

    duration = end_time - start_time
    print("執行時間:", duration)