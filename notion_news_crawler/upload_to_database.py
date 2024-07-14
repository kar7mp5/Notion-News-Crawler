import requests
import json
import concurrent.futures
from tqdm import tqdm
import logging
from retrying import retry

# Load the api
from config import Config

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def add_item_to_notion(self, item):
        """Helper function to add a single item to Notion with retry logic."""
        try:
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
            response.raise_for_status()  # raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to add: {item['name']}, Error: {str(e)}")
            raise

    def add_to_notion(self):
        """Upload the data to Notion database using multithreading."""
        
        total_items = len(self.data)
        logger.info(f"Uploading {total_items} items to Notion")

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
                    try:
                        future.result()  # Ensure any exceptions raised in the threads are propagated
                    except Exception as e:
                        logger.error(f"Error in future: {str(e)}")
