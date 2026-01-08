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
    API_ENDPOINT_MAKE = f"{API_BASE_URL}/api/cruds/make"
    API_ENDPOINT_MODEL = f"{API_BASE_URL}/api/cruds/model"
    API_ENDPOINT_VARIANT = f"{API_BASE_URL}/api/cruds/variant?length=100000"
    
    token = ""
    
   

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
    def getmake(LoginToken):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LoginToken}"
        }
  
        response = requests.get(
            Action.API_ENDPOINT_MAKE,
            headers=headers,
            verify=False,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json().get("data", [])
        return data
    
    @staticmethod
    def getVariant(LoginToken):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LoginToken}"
        }

        response = requests.get(
            Action.API_ENDPOINT_VARIANT,
            headers=headers,
            verify=False,
            timeout=30
        )

        response.raise_for_status()
        data = response.json().get("data", [])
        json_path = os.path.join(PUBLIC_PATH, "json", "webvariant.json")
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return data
    
    @staticmethod
    def getAuctionDetails(sheet_id,LoginToken):
        Action.token = LoginToken

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LoginToken}"
        }
        check = requests.get(
            f"{Action.API_ENDPOINT}?table_id={sheet_id}",
            headers=headers,
            verify=False,
            timeout=30
        )
        check.raise_for_status()
        data = check.json().get("data", [])
        return data
    

    @staticmethod
    def updateAuction(auction_db_id,payload,LoginToken):
        Action.token = LoginToken

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LoginToken}"
        }

        r = requests.post(
            f"{Action.API_ENDPOINT}/{auction_db_id}",
            json=payload,
            headers=headers,
            verify=False,
            timeout=60
        )
        print(f"🔄 Updating auction sheet {auction_db_id}")
      
        return r

    @staticmethod
    def createAuction(payload,LoginToken):
        Action.token = LoginToken

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LoginToken}"
        }

        r = requests.post(
                Action.API_ENDPOINT,
                json=payload,
                headers=headers,
                verify=False,
                timeout=60
            )
        print(f"🔄 Auction Created")
      
        return r
    
    
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


   

