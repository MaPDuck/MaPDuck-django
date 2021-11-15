from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from naver.services.naver_selenium_crawling import NaverCrawler
from naver.services.naver_service import get_my_products, get_naver_shopping
from naver.serializer import MyProductSerializer
from rest_framework.response import Response
import base64
# Create your views here.

# 작성자: 양태영
# 작성일: 21.11.15
# 설명: 내가 산 제품을 네이버에서 크롤링을 통해 얻는 함수 id, pw는 base64로 인코딩 되어 헤더에서 수신.
class MyProductView(APIView):
    @swagger_auto_schema()
    def get(self, request):
        id = base64.b64decode(request.META.get("HTTP_NAVER_ID")).decode('utf-8')
        pw = base64.b64decode(request.META.get("HTTP_NAVER_PW")).decode('utf-8')
        naver_crawler = NaverCrawler()
        naver_crawler.get_prooduct_list_Naver(id, pw)
        my_product_list = get_my_products(naver_crawler.products)
        serializer = MyProductSerializer(my_product_list, many=True)
        return Response(serializer.data)

class NaverSearchView(APIView):
    @swagger_auto_schema()
    def get(self, request):
        keyword = request.GET.get("keyword")
        return get_naver_shopping(keyword)



