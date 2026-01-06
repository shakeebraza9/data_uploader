import os,re
import csv
import json
import time
import requests
import logging
import urllib3
from datetime import datetime
from ExportRecord.DataFomater import DataFomater 
from ExportRecord.DataPrefix import DataPrefix
from ExportRecord.Action import Action
from config import PUBLIC_PATH,LOG_FILE,auctionNameNormalize


class Main:
    
    API_BASE_URL = os.getenv("API_BASE_URL")
    LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
    LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
    API_ENDPOINT = f"{API_BASE_URL}/api/cruds/auctions"
    API_ENDPOINT_PLATEFROM = f"{API_BASE_URL}/api/cruds/platform"


    @staticmethod
    def getSheetsForUploading(LoginToken):
        result = []

        folder_path = os.path.join(PUBLIC_PATH, "csv")
        folder_path = folder_path.replace("/", "\\")

        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(".csv"):
                continue

            name = os.path.splitext(filename)[0]
            parts = name.split("_")
            auction_date = parts[0]
            auction_house = parts[1]
            sheet_id, center_name = parts[2].split("-", 1)

            platrfrom_id = Action.getPlatefromID(auction_house,LoginToken)

            csv_path = os.path.join(folder_path, filename)
            rows = []

            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dataFeild = DataFomater(row)
                    mapped_row = dataFeild.Render()
                    rows.append(mapped_row)
                    # print(rows)

            result.append({
                "id": sheet_id,
                "name": center_name,
                "auction_date": auction_date,
                "platform_id": platrfrom_id,
                "auction_type": 2,
                "status": "draft",
                "payload": json.dumps(rows, ensure_ascii=False)
            })
        # print(result)
        return result


    
    @staticmethod
    def post_or_update(payload, token):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        sheet_id = payload.get("id")

        try:

            data = Action.getAuctionDetails(sheet_id,token)
            print(data)
            if data:
                auction_db_id = data[0]["id"]
                payload["_method"] = "PUT"

                print(f"🔄 Updating auction sheet {sheet_id}")

                r = requests.post(
                    f"{Main.API_ENDPOINT}/{auction_db_id}",
                    json=payload,
                    headers=headers,
                    verify=False,
                    timeout=60
                )

            else:
                print(f"🆕 Creating auction sheet {sheet_id}")

                r = requests.post(
                    Main.API_ENDPOINT,
                    json=payload,
                    headers=headers,
                    verify=False,
                    timeout=60
                )

            if r.status_code >= 400:
                print(f"❌ API Error {r.status_code} on sheet {sheet_id}")
                logging.error(f"Sheet:{sheet_id} , Status Code:{r.status_code}")
                logging.error(f"${r.json()}")

                return r.status_code, r.text

            print("✅ Success:", r.status_code)
            return r.status_code, r.text

        except Exception as e:
            print("❌ Exception:", sheet_id)
            logging.error(f"Sheet:{sheet_id} , EXCEPTION:{str(e)}")
            return None, None



    @staticmethod
    def Run():

        DataPrefix.GenJSon()

        LoginToken = Action.login_and_get_token() 
        auctions = Main.getSheetsForUploading(LoginToken)

        for auction in auctions:

            Main.post_or_update(auction, LoginToken)
            time.sleep(3)   