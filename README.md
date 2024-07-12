# Notion-News-Crawler

Notion news crawler

## Table of contents

[**1. APIs**](#1-apis)  
[1-1. Environment parameters (`config.py`)](#1-1-environment-parameters-configpy)  
[1-2. Notion API](#1-2-notion-api)  
[1-3. Naver API](#1-3-naver-api)

---

## 1. APIs

### 1-1. Environment parameters (`config.py`)

**`.env` file**

```
# Notion
NOTION_TOKEN
NOTION_DATABASE_ID

# Naver
X_NAVER_CLIENT_ID
X_NAVER_SECRET
```

### 1-2. Notion API

```python
self.headers = {
    "Authorization": f"Bearer {self.notion_token}", # notion application token
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"                  # latest version of the notion
}
```

### 1-3. Naver API

**Naver news api**  
[Naver API Application](https://developers.naver.com/apps/#/myapps/tXBrP5xIcu61FHzmj15v/overview)  
[About NAVER API](https://developers.naver.com/docs/serviceapi/search/news/news.md#%EB%89%B4%EC%8A%A4)

The result of the Naver API

```json
{
    "title": "article title",
    "originallink": "original news link",
    "link": "naver news link",
    "description": "article description",
    "pubDate": "published date"
}
```

---
