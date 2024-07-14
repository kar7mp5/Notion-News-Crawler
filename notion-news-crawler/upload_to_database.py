# upload_to_database.py
import requests
import json
import concurrent.futures
from tqdm import tqdm

# Load the api
from config import Config


class UploadToDataBase(Config):
    def __init__(self, data):
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
        self.data = data


    def add_item_to_notion(self, item):
        """Helper function to add a single item to Notion."""
        url = "https://api.notion.com/v1/pages"
        new_page = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": item["name"]
                            }
                        }
                    ]
                },
                "Description": {
                    "rich_text": [
                        {
                            "text": {
                                "content": item["description"]
                            }
                        }
                    ]
                },
                "URL": {
                    "url": item["link"]
                },
                "Date": {
                    "date": {
                        "start": item["pubDate"]
                    }
                },
                "Tags": {
                    "multi_select": [{"name": item["tag"]}]
                }
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(new_page))
        if response.status_code == 200:
            pass
            # print(f'Successfully added: {item["name"]}')
        else:
            print(f'Failed to add: {item["name"]}, Error: {response.json()}')




    def add_to_notion(self):
        """Upload the data to Notion database using multithreading."""
        
        total_items = len(self.data)

        # Adjusting tqdm settings
        tqdm_settings = {
            'desc': 'Progress',
            'total': total_items,
            'unit': 'item',
            'unit_scale': True,
            'leave': True,
            'dynamic_ncols': True  # Adjusts the bar dynamically to fit the terminal width
        }

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Use tqdm to display progress
            with tqdm(**tqdm_settings) as pbar:
                futures = []
                for item in self.data:
                    future = executor.submit(self.add_item_to_notion, item)
                    future.add_done_callback(lambda _: pbar.update(1))  # Update progress bar when each future completes
                    futures.append(future)

                # Wait for all futures to complete
                for future in concurrent.futures.as_completed(futures):
                    future.result()  # Ensure any exceptions raised in the threads are propagated
