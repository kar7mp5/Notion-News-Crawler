# reset_database.py
import requests
import concurrent.futures
from tqdm import tqdm

from config import Config




class ResetDatabase(Config):
    def __init__(self):
        """Initialize ResetDatabase instance.
        
        Inherits configuration settings from Config class,
        sets up necessary headers for Notion API requests.
        """
        super().__init__()
        
        # Set up the header
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }


    def _get_all_pages(self):
        """Get all pages from the database.
        
        Returns:
            list: List of page objects from the database.
        """
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            print(f"Left pages: {len(response.json()['results'])}")
            return response.json()["results"]
        else:
            print(f'Failed to retrieve pages. Error: {response.json()}')
            return []


    def _delete_page(self, page_id):
        """Delete a page from the database.
        
        Args:
            page_id (str): ID of the page to delete.
        """
        url = f"https://api.notion.com/v1/blocks/{page_id}"
        response = requests.delete(url, headers=self.headers)
        
        # Fail to delete the page
        if response.status_code != 200:
            print(f'Failed to delete page: {page_id}, Error: {response.json()}')


    def delete_all_pages(self):
        """Delete all pages from the database."""
        
        pages = self._get_all_pages()
        total_pages = len(pages)
        deleted_pages = 0

        # Use tqdm inside the while loop
        while len(pages) > 0:
            with tqdm(total=total_pages, desc='Deleting pages', unit='page', unit_scale=True) as pbar:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Submit _delete_page tasks and get futures
                    futures = [executor.submit(self._delete_page, page["id"]) for page in pages]

                    # As_completed to iterate over completed futures
                    for future, page in zip(concurrent.futures.as_completed(futures), pages):
                        try:
                            future.result()  # Ensure the task completed without exception
                            deleted_pages += 1
                            pbar.update(1)  # Update progress bar for each completed page
                        except Exception as exc:
                            print(f'Page {page["id"]} generated an exception: {exc}')  # page here is accessed correctly

                # Retrieve pages again after deletion
                pages = self._get_all_pages()
                total_pages = len(pages)  # Update total pages after each iteration
        
        print(f'All pages deleted. Total pages deleted: {deleted_pages}')




if __name__=='__main__':
    reset_database = ResetDatabase()
    reset_database.delete_all_pages()