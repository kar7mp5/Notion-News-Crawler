# naver_api.py
import requests
import html, re
from datetime import datetime
import pytz

from config import Config


class NaverAPI(Config):
    def __init__(self, subject, news_num):
        """NaverAPI
        
        Args:
            subject (str): The subject of the article
            news_num (int): Number of news articles to retrieve
        """
        super().__init__()
        
        self.subject = subject
        self.news_num = news_num
        
        # Define the headers
        self.headers = {
            "X-Naver-Client-Id": self.x_naver_client_id,
            "X-Naver-Client-Secret": self.x_naver_secret
        }

        self.tags = {
            'Economy': '경제',
            'Science': '과학',
            'Society': '사회',
            'Politics': '정치',
            'Stock': '주식'
        }


    def clean_text(self, text):
        """Delete HTML tags from the text
        
        Args:
            text (str): The text of the article
            
        Returns:
            str: The text without HTML tags
        """
        clean = re.compile('<.*?>')
        text_without_tags = re.sub(clean, '', text)

        return html.unescape(text_without_tags)


    def get_news(self):
        """Get news articles from Naver API

        Returns:
            dict: The result containing a list of news articles with keys ['title', 'originallink', 'link', 'description', 'pubDate'], and the subject
        """
        # Define the URL and query parameters
        url = "https://openapi.naver.com/v1/search/news.json"
        params = {
            "query": self.tags[self.subject],
            "display": self.news_num,
            "start": 1,
            "sort": "sim"
        }

        try:
            # Make the request
            response = requests.get(url, headers=self.headers, params=params)
            response = response.json()
        except requests.exceptions.RequestException as e:
                print(f'Failed to add: {item["name"]}, Error: {e}')

        
        for item in response['items']:
            item['title'] = self.clean_text(item['title'])
            item['description'] = self.clean_text(item['description'])
            
            # Input date and time string
            input_datetime_str = item['pubDate']

            # Define the input format for parsing
            input_format = "%a, %d %b %Y %H:%M:%S %z"
            input_datetime = datetime.strptime(input_datetime_str, input_format)

            # Convert to UTC timezone
            input_datetime_utc = input_datetime.astimezone(pytz.utc)

            # Convert to ISO 8601 format
            item['pubDate'] = input_datetime_utc.isoformat()
            
        return {
            'contents': response['items'], 
            'tags': self.subject
        }


    def parse_data(self, data):
        """Parse the news data

        Args:
            data (dict): The data containing news articles and tags

        Returns:
            list: A list of parsed news articles with keys ['name', 'description', 'tag']
        """
        result = []
        tag = data['tags']

        for item in data['contents']:

            result.append({
                            'name': item['title'], 
                            'description': item['description'],
                            'link': item['link'],
                            'pubDate': item['pubDate'],
                            'tag': tag
                        })
        
        return result


if __name__=='__main__':
    naver_api = NaverAPI('Economy', 10)
    print(naver_api.parse_data(naver_api.get_news()))