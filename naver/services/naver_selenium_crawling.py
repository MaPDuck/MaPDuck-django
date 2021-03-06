import selenium.common.exceptions

from ..dto import Naver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip
import time
import platform


# 작성자: 강동연
# 설명: Selenium 패키지를 사용해, 네이버 로그인 후 네이버 페이 내역 크롤링

# 수정일: 2021.11.05
# 수정사항: purchased_at(구매날짜) 추가
class NaverCrawler:

    def __init__(self):
        self.products = list()

    def get_prooduct_list_Naver(self, id, password):

        # 크롬 드라이버 옵션
        options = webdriver.ChromeOptions()
        
        # headless 옵션 설정
        # options.add_argument('headless')
        # options.add_argument("no-sandbox")

        # 사람처럼 보이게 하는 옵션들
        options.add_argument("disable-gpu")  # 가속 사용 x
        options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
        options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정
        
        # 크롬드라이버 위치 check
        # driver = webdriver.Chrome("/Users/taeyoung/chromedriver", chrome_options=options)
        driver = webdriver.Chrome("C:/chromedriver.exe", chrome_options=options)
        
        # 네이버 loginURL
        url = 'https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'
        id = id
        pw = password
        
        # 드라이버 접속
        driver.get(url)

        time.sleep(2)

        tag_id = driver.find_element(By.ID,"id")
        tag_pw = driver.find_element(By.ID, "pw")

        tag_id.click()
        pyperclip.copy(id)

        # 운영체제에 따른 복사 키 지정
        copy_key = Keys.LEFT_CONTROL
        if platform.system().lower() == "windows":
            copy_key = Keys.CONTROL
        elif platform.system().lower() == "darwin":
            copy_key = Keys.COMMAND

        tag_id.send_keys(copy_key, 'v')
        tag_pw.click()
        pyperclip.copy(pw)
        tag_pw.send_keys(copy_key, 'v')
        login_btn = driver.find_element(By.ID, "log.login")
        login_btn.click()

        # 거래 내역 접속
        driver.get("https://order.pay.naver.com/home")



        # 5번 더보기 클릭
        for i in range(5):
            try:
                more_btn = driver.find_element(By.XPATH, "//*[@id='_moreButton']/button")
                more_btn.click()
                time.sleep(0.5)
            except selenium.common.exceptions.ElementNotInteractableException:
                pass

        src = driver.page_source
        soup = BeautifulSoup(src, "html.parser")
        
        # 크롬 드라이버 닫기
        driver.close()
        

        # title: 주문 내역
        # company_name: 회사 이름
        # img_path: 이미지 주소

        # month 수
        month_len = len(soup.select("#_listContentArea > div.goods_pay_section"))
        for months in range(month_len):

            # 주문내역 수
            order_list_len = len(
                soup.select("#_listContentArea > div.goods_pay_section")[months].select("div.goods_group"))

            for order_num in range(order_list_len):
                # 주문 내역 고유번호
                key_id = soup.select("#_listContentArea > div.goods_pay_section")[months].select("div.goods_group > ul > li")[
                    order_num]["id"]

                # 주문 내역
                title = soup.select_one("#{} > div.goods_item > div > a > p".format(key_id)).text.strip()

                # 주문 내역 회사 이름
                company_name = soup.select_one("#{} > div.seller_item > div > span.seller".format(key_id)).text

                # 이미지 주소
                img_path = soup.select_one("#{} > div.goods_item > a > img".format(key_id))["src"]

                _, purchase_at_str = soup.select_one(
                    "#{} > div.goods_item > div > a > ul > li.date".format(key_id)).text.split(" ")
                purchase_at = purchase_at_str

                self.products.append(Naver(title,company_name,img_path, purchase_at))


