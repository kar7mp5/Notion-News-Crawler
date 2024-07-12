# naver_api.py
import requests
import html, re

from config import Config


class NaverAPI(Config):
    def __init__(self, subject, news_num):
        """NaverAPI
        
        Arg:
            subject (str): The subject of the article
            news_num (int): News number
        """
        super().__init__()
        
        self.subject = subject
        self.news_num = news_num
        
        # Define the headers
        self.headers = {
            "X-Naver-Client-Id": self.x_naver_client_id,
            "X-Naver-Client-Secret": self.x_naver_secret
        }


    def clean_text(self, text):
        """Delete html tags
        
        Arg:
            text (str): The text of the article
            
        Returns:
            str: The text that don't have html tags
        """

        clean = re.compile('<.*?>')
        text_without_tags = re.sub(clean, '', text)

        return html.unescape(text_without_tags)


    def get_news(self):
        """Get news

        Returns:
            list[dict[str]]: The result of the feature; ['title', 'originallink', 'link', 'description', 'pubDate']
        """
        
        # Define the URL and query parameters
        url = "https://openapi.naver.com/v1/search/news.json"
        params = {
            "query": self.subject,
            "display": self.news_num,
            "start": 1,
            "sort": "sim"
        }
        
        # Make the request
        response = requests.get(url, headers=self.headers, params=params)

        for item in response.json()['items']:
            item['title'] = self.clean_text(item['title'])
            item['description'] = self.clean_text(item['description'])

        return response.json()['items']


if __name__=='__main__':
    naver_api = NaverAPI('뉴스', 10)
    print(naver_api.get_news())