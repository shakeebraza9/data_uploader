import os
import re,json


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


PUBLIC_PATH = os.path.join(PROJECT_ROOT, 'public')

LOG_FILE = "auction_error.log"
GOOGLE_SHEET_LINK = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQY4fogSBMvwerj4JDlULq8UtsznV3Rd6OX5Bh8vimACCCOx93KlnRWAHSPplcKAB_SpK6CoGA7w4bR/pub?output=xlsx"

# AUCTIONS_DIR = r"\\192.168.18.57\Done Auction"
AUCTIONS_DIR = r"E:\Done Auction"
# AUCTIONS_DIR = r"D:\test\12-Dec"

AUCTION_OUTPUT_DIR = PUBLIC_PATH +'\\csv'



def slugify(text: str):
    
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)  
    text = re.sub(r"[\s_-]+", "-", text)   
    return text.strip("-")


def getJSonPrefixFile(name:str):
    json_path = os.path.join(PUBLIC_PATH, "json", name+".json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            response = json.load(f)
        return response
    except Exception:
        return {}


def auctionNameNormalize(text):
        text = text.lower()
        text = re.sub(r"(auction|auctions|car|cars)", "", text)
        return text.strip()