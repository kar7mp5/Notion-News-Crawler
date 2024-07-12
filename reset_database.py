# reset_database.py
import requests

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
            "Notion-Version": "2022-06-28"
        }


    def get_all_pages(self):
        """Get all pages from the database.
        
        Returns:
            list: List of page objects from the database.
        """
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        response = requests.post(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            print(f'Failed to retrieve pages. Error: {response.json()}')
            return []


    def delete_page(self, page_id):
        """Delete a page from the database.
        
        Args:
            page_id (str): ID of the page to delete.
        """
        url = f"https://api.notion.com/v1/blocks/{page_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 200:
            print(f'Successfully deleted page: {page_id}')
        else:
            print(f'Failed to delete page: {page_id}, Error: {response.json()}')


    def delete_all_pages(self):
        """Delete all pages from the database."""
        
        pages = self.get_all_pages()
        for page in pages:
            self.delete_page(page["id"])


if __name__=='__main__':
    reset_database = ResetDatabase()
    reset_database.delete_all_pages()
