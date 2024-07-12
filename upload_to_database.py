# upload_to_database.py
import requests
import json

# Load the api
from config import Config


class UploadToDataBase(Config):
    def __init__(self):
        """Initialize UploadToDataBase instance.
        
        Inherits configuration settings from Config class,
        sets up necessary headers for Notion API requests,
        and initializes data to upload to the database.
        """
        super().__init__()
        
        # Set up the header
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        # Data to be uploaded
        self.data = [
            {"name": "Sample Task 3", "description": "This is the first task"},
            {"name": "Sample Task 2", "description": "This is the second task"}
        ]


    def add_to_notion(self):
        """Upload the data to Notion database."""
        
        url = f"https://api.notion.com/v1/pages"
        for item in self.data:
            new_page = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "이름": {  # Adjusted to match the actual property name in Notion
                        "title": [
                            {
                                "text": {
                                    "content": item["name"]
                                }
                            }
                        ]
                    },
                    "태그": {  # Adjusted to match the actual property name in Notion
                        "multi_select": []
                    }
                }
            }
            
            response = requests.post(url, headers=self.headers, data=json.dumps(new_page))
            if response.status_code == 200:
                print(f'Successfully added: {item["name"]}')
            else:
                print(f'Failed to add: {item["name"]}, Error: {response.json()}')


if __name__=='__main__':
    upload_to_database = UploadToDataBase()
    upload_to_database.add_to_notion()