from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .services.crawling import DanawaCrawler
from .services.danawa_separator import DanawaSeparator
from .serializer import ProductSerializer
from rest_framework.response import Response
# Create your views here.

class Danawa(APIView):

    @swagger_auto_schema()
    def get(self, request):
        keyword = request.GET.get("keyword")
        danawa = DanawaCrawler()
        danawa.get_product_list_danawa(keyword, 2)
        danawa_separator = DanawaSeparator(danawa.products)
        products = danawa_separator.get_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
