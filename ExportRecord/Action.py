import os,re
import csv
import json
import time
import requests
import urllib3
from datetime import datetime
from ExportRecord.DataFomater import DataFomater 
from ExportRecord.DataPrefix import DataPrefix
from config import PUBLIC_PATH,LOG_FILE,auctionNameNormalize

class Action:

    API_BASE_URL = os.getenv("API_BASE_URL")
    LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
    LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
    API_ENDPOINT = f"{API_BASE_URL}/api/cruds/auctions"
    API_ENDPOINT_PLATEFROM = f"{API_BASE_URL}/api/cruds/platform"
   


   

    @staticmethod
    def getPlatefromID(auction_house, LoginToken):
        if not auction_house:
            return None
        ALIASES = {
            "protruck": ["protruck", "protruck auction"],
            "cca": ["central car auction", "central car auctions", "cca"],
            "bca": ["bca", "british car auctions"],
            "manheim": ["manheim", "manheim auction"],
            "aston barclay": ["aston barclay", "aston barclay auctions"],
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LoginToken}"
        }

        response = requests.get(
            Action.API_ENDPOINT_PLATEFROM,
            headers=headers,
            verify=False,
            timeout=30
        )

        response.raise_for_status()
        data = response.json().get("data", [])

        auction_norm = auctionNameNormalize(auction_house)

        for item in data:
            item_norm = auctionNameNormalize(item["name"])
            for key, names in ALIASES.items():
                if auction_norm in names and key in item_norm:
                    return item["id"]
            if auction_norm in item_norm or item_norm in auction_norm:
                return item["id"]

        return None
    
    

    @staticmethod
    def login_and_get_token():
        url = f"{Action.API_BASE_URL}/api/auth/login"
        payload = {
            "email": Action.LOGIN_EMAIL,
            "password": Action.LOGIN_PASSWORD
        }

        try:
            r = requests.post(url, json=payload, verify=False, timeout=30)
            r.raise_for_status()
            token = r.json().get("data").get("token")

            if not token:
                raise Exception("Token missing in response")

            print("✅ Login successful")
            return token

        except Exception as e:
            print("❌ Login failed:", e)
            exit()
    


    def log_error(sheet_id, error_type, response=None):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"Time       : {datetime.now()}\n")
            f.write(f"Sheet ID   : {sheet_id}\n")
            f.write(f"Error Type : {error_type}\n")

            if response is not None:
                try:
                    f.write("API Response:\n")
                    f.write(json.dumps(response, indent=2, ensure_ascii=False))
                except Exception:
                    f.write(str(response))

            f.write("\n\n")


   

