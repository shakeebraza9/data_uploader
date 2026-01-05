import os
# This gets the folder where config.py is (your real project root)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Global paths you can use anywhere
PUBLIC_PATH = os.path.join(PROJECT_ROOT, 'public')

API_BASE_URL = os.getenv("API_BASE_URL")
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD")
LOG_FILE = "auction_error.log"
API_ENDPOINT = f"{API_BASE_URL}/api/cruds/auctions"
API_ENDPOINT_PLATEFROM = f"{API_BASE_URL}/api/cruds/platform"
GOOGLE_SHEET_LINK = os.getenv("GOOGLE_SHEET_LINK")