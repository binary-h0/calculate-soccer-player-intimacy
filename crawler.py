# -*- coding: utf-8 -*-
import requests
import time
import random
import io
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

    # 웹드라이버 종료
    driver.quit()


def getNewsPageData(file_link, save_link):
    urls = []
    driver_path = "../chromedriver"
    driver = webdriver.Chrome(driver_path)
    with open(file_link, "r") as f:
        url = f.readline()
        while url:
            urls.append(url.strip())
            url = f.readline()
        f.close()
    for i in urls:
        print(i)

    with io.open(save_link, "a", encoding='utf-8') as f:
        for url in urls:
            print("REQUEST: %s" % url)
            driver.get(url.strip())
            title = driver.find_elements(
                By.XPATH, '//*[@id="content"]/div/div[1]/div/div[1]/h4')
            f.write(title[0].text+'\n')

            content = driver.find_elements(
                By.XPATH, '//*[@id="newsEndContents"]')
            token = content[0].text.split('\n')
            for i in range(len(token) - 18):
                if len(token[i].rstrip()) != 0:
                    f.write(token[i].rstrip() + '\n')

            time.sleep(1)
        f.close()

    # 웹드라이버 종료
    driver.quit()


# getNewPageLink('./src/news_page_links.txt', 1, 10)
getNewsPageData('./src/news_page_links.txt', './src/page_data.txt')
