from konlpy.tag import Kkma
from konlpy.utils import pprint
import re
from ..models import Company
from django.db.models import Q
from ..dto import Product
from ..utils import len_max

# 작성자: 양태영
# 설명: 크롤러를 통해 받은 내용을 재분리하여 spring에 맞는 형식으로 보내기 위한 것.
class DanawaSeparator:
    kkma = Kkma()

    def __init__(self, danawa_crawled):
        # 크롤링을 통해 분리된 dict: json/danawa.json형식
        self.danawas = danawa_crawled
        self.results = list()

    # 작성자: 양태영
    # 작성일: 21.10.27
    # 설명 title에서 모델명 추출하는 함수 추출 실패시 None 도출
    # INPUT: 제목
    # RETURN: 모델명 or None
    def get_model_name(self, title_string: str):
        result_list = list()  # 결과 후보군 생성
        title_list = title_string.split(" ")
        # 모델명 판별 패턴 설정
        pattern = "([A-Z]|[0-9])+([A-Z]|[0-9]|-|_|\/)+([A-Z]|[0-9])"
        prog = re.compile(pattern)

        for title in title_list:
            matches = prog.match(title)
            if prog.match(title) is not None and len(title) >= 6:
                result_list.append(title)

        # 모델명 찾기 실패
        if len(result_list) == 0:
            return None, title_string

        # 모델명에 요소가 있는 경우 유력 후보 탐색
        # 탐색 기준 string속에 -, /, _ 문자가 포함되어 있는가?
        # 있을 경우 모델명일 확률이 높기 때문에 해당 문자열을 바로 리턴함
        for result in result_list:
            if result.find('-') != -1:
                return result, title_string[:title_string.find(result)]
            elif result.find('/') != -1:
                return result, title_string[:title_string.find(result)]
            elif result.find('_') != -1:
                return result, title_string[:title_string.find(result)]
        # 없을 경우 결과 후보군 중 가장 길이가 긴 요소를 리턴함.
        return len_max(result_list), title_string[:title_string.find(len_max(result_list))]

    # 작성자: 양태영
    # 작성일시: 21.10.30
    # 입력: 상품 제목(str)
    # 반환: 회사 번호(int), 제목에서 회사명을 제외한 문자열(str)
    # 회사명을 찾지 못할 경우 회사번호는 -1, 남은 문자열은 상품 제목 전체가 리턴됨.
    def get_company_id(self, title_string: str):
        # 띄어쓰기를 기준으로 회사명 후보군 도출
        candidates = title_string.split(" ")
        for candidate in candidates:
            # 회사 영어명이나 한글 명중 후보군이 있는지 검색
            results = Company.objects.filter(co_eng_name=candidate.lower())
            if len(results) != 0:
                company = results.first()
                candidates.pop(candidates.index(candidate))
                rest_title = " ".join(candidates)
                return company.pk, rest_title
            results = Company.objects.filter(co_kor_name=candidate)
            if len(results) != 0:
                company = results.first()
                candidates.pop(candidates.index(candidate))
                rest_title = " ".join(candidates)
                return company.pk, rest_title
        return -1, title_string

    def get_warranty(self, title, description):
        return 0

    # Spring에 보낼 필요한 요소를 포장하여 내보내는 함수.
    def get_products(self):
        for danawa in self.danawas:
            # 모델명이 없으면 상품파악이 불가능해지므로 쓰지 않음.
            title_string = danawa.title
            co_id, title_string = self.get_company_id(title_string)
            if co_id == -1:
                continue
            mo_name, title_string = self.get_model_name(title_string)
            if mo_name is None:
                continue
            warranty = self.get_warranty(title=title_string, description=danawa.desc)
            if title_string and title_string != "":
                pr_name = title_string
            else:
                pr_name = mo_name
            product = Product(
                co_id=co_id,
                pr_name=pr_name,
                mo_name=mo_name,
                warranty=warranty,
                desc=danawa.desc,
                img_path=danawa.img_path
            )

            self.results.append(product)

        return self.results
