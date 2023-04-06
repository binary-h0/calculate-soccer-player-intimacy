# -*- coding: utf-8 -*-
import requests
import time
import random
import io
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getNewPageLink(savePath, m):
    # 크롬 드라이버 경로 설정
    driver_path = "../chromedriver"

    # 웹드라이버 실행
    driver = webdriver.Chrome(driver_path)
    stack = []
    month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for day in range(1, month[m-1] + 1):
        page = 1
        headLink = "0"
        while page < 30:
            url = "https://sports.news.naver.com/kfootball/news/index?page=%d&date=202303%02d&isphoto=N&type=latest" % (
                page, day)
            print("REQUEST: %s" % url)
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            links = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="_newsList"]/ul/li/div/a')))

            _headLink = links[0].get_attribute("href")
            _headLink = _headLink[len(_headLink)-10:len(_headLink)]
            if headLink == _headLink:
                break
            headLink = _headLink

            for link in links:
                href = link.get_attribute("href")
                print("HREF:", href)
                stack.append(href)

            page += 1
            print(headLink)
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


getNewPageLink('./src/news_page_links.txt', 1, 10)
# getNewsPageData('./src/news_page_links.txt', './src/page_data.txt')
