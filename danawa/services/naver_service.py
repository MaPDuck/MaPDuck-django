import requests

# 작성자: 양태영
# 작성일: 21.11.03
# 입력: query: 검색어
# 반환: naver api결과 리스트 객체
# 설명: 검색어(query)를 통해 네이버 쇼핑리스트를 조회하고 반환하는 것.
def get_naver_shopping(query):
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": "9JWI6ruL74CEVqgkzXzE",
        "X-Naver-Client-Secret": "FJYLc07Kas"
    }
    return requests.get(url=url, headers=headers, params={"query": query}).json().get("items")

