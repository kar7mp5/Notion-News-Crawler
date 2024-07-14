from notion_news_crawler import NaverAPI, UploadToDataBase, ResetDatabase


if __name__=='__main__':
    reset_database = ResetDatabase()
    reset_database.delete_all_pages()
    
    for subject in ['Economy', 'Science', 'Society', 'Politics', 'Stock']:
        naver_api = NaverAPI(subject, 100)
        news_data = naver_api.parse_data(naver_api.get_news())

        upload_to_database = UploadToDataBase(news_data)
        upload_to_database.add_to_notion()