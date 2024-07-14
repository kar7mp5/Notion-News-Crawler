# Notion-News-Crawler

Notion News Crawler is a Python library that collects news from Notion and uploads it to a database.

News can be collected using Naver Search API, so only Naver and Notion API keys can be used by putting them in environment variables.

## Table of Contents

1. [Install](#install)
2. [Supported Python Version](#supported-python-version)
3. [APIs](#apis)
    - [Environment Parameters](#environment-parameters)
    - [Notion API](#notion-api)
    - [Naver API](#naver-api)
4. [Result](#result)

## Install

```bash
$ pip3 install notion-news-crawler
```

## Supported Python version

|       Library       |     Supported Version      |
| :-----------------: | :------------------------: |
| Notion News Crawler | 3.8, 3.9, 3.10, 3.11, 3.12 |

## APIs

To use this library, Notion and Naver API are required.

Just enter the two API Key values ​​in the environment variables.

### Environment parameters

You can create an environment variable .env file and use it by entering the following.

**.env file format**

```
# Notion
NOTION_TOKEN='YOUR NOTION TOKEN'
NOTION_DATABASE_ID='YOUR NOTION DATABASE ID'

# Naver
X_NAVER_CLIENT_ID='YOUR NAVER CLIENT ID'
X_NAVER_SECRET='YOUR NAVER SECRET KEY'
```

### Notion API

The Notion API can be found at: [**Notion API**](https://developers.notion.com/)  
Enter the Notion application token value in the environment variable.
Create a Notion application, register the Notion application in the database you will use, and then use it.

### Naver API

You can create a [Naver application](https://developers.naver.com/apps/#/list) and obtain the API key value.  
More detail on [NAVER API docs](https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4)

The Naver API result values ​​are as follows, and when uploading to Notion, you can refine and use the data as you wish.

```json
{
    "title": "article title",
    "originallink": "original news link",
    "link": "naver news link",
    "description": "article description",
    "pubDate": "published date"
}
```
