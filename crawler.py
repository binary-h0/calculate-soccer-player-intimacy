# -*- coding: utf-8 -*-
import requests
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def getNewPageLink(savePath, start, end):
    # 크롬 드라이버 경로 설정
    driver_path = "../chromedriver"

    # 웹드라이버 실행
    driver = webdriver.Chrome(driver_path)
    stack = []
    for i in range(start, end+1):
        # 크롤링할 웹페이지 주소
        url = "https://sports.news.naver.com/kfootball/news/index?isphoto=N&type=latest&page=%d" % i
        print("REQUEST: %s" % url)

        # 웹페이지 열기
        driver.get(url)

        # 각 뉴스 기사의 링크 추출
        links = driver.find_elements(
            By.XPATH, '//*[@id="_newsList"]/ul/li/div/a')

        for link in links:
            href = link.get_attribute("href")
            print("ELEM:", link)
            print("HREF:", href)
            stack.append(href)
            # print("GET PAGE LINK: %s" % link)
        r = random.randrange(5, 10)
        time.sleep(1)
    # 저장
    with open(savePath, "a") as f:
        for link in stack:
            f.write(link+'\n')
        f.close()


getNewPageLink('./src/news_page_links.txt', 1, 10)

# 웹드라이버 종료
driver.quit()


# # 뉴스 기사 HTML 소스코드 가져오기
# res = requests.get(news_url)
# html = res.text

# # BeautifulSoup 객체 생성
# soup = BeautifulSoup(html, "html.parser")

# # 뉴스 기사 제목 추출
# title = soup.select_one('div.title > h4').get_text()

# # 뉴스 기사 본문 추출
# content = soup.select_one('div._article_body_contents').get_text().replace(
#     '\n', '').replace('\t', '').strip()

# # 추출한 제목과 본문 출력
# print(title)
# print(content)
