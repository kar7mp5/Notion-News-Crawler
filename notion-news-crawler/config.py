# config.py
from dotenv import load_dotenv
import os

class Config:
    def __init__(self):    
        # Load the api token and database id (Notion, Naver)
        load_dotenv()
        # Notion APIs
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = os.getenv('NOTION_DATABASE_ID')
        # Naver APIs
        self.x_naver_client_id = os.getenv('X_NAVER_CLIENT_ID')
        self.x_naver_secret = os.getenv('X_NAVER_SECRET')