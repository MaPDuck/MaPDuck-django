from django.test import TestCase
from .services.danawa_separator import DanawaSeparator
from .services.naver_service import get_naver_shopping
# Create your tests here.
class DanawaSeparatorTest(TestCase):
    def test_get_model_name(self):
        ds = DanawaSeparator(dict())
        self.assertIsNotNone(ds.get_model_name())
        print(ds.get_model_name())

class NaverServiceTest(TestCase):
    def test_get_naver_api(self):
        res = get_naver_shopping("노트북")
        print(res)
