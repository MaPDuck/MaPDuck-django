import requests


def get_naver_shopping(query):
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": "9JWI6ruL74CEVqgkzXzE",
        "X-Naver-Client-Secret": "FJYLc07Kas"
    }
    return requests.get(url=url, headers=headers, params={"query": query}).json().get("items")

