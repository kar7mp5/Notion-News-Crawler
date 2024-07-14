# main.py
from naver_api import NaverAPI
from upload_to_database import UploadToDataBase


for subject in ['Economy', 'Science', 'Society', 'Politics', 'Stock']:
    naver_api = NaverAPI(subject, 100)
    news_data = naver_api.parse_data(naver_api.get_news())

    upload_to_database = UploadToDataBase(news_data)
    upload_to_database.add_to_notion()