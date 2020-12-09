"""
Airbnb Listing Search Page Fetch DEMO
25-NOV-2020
"""

"""
import requests
url = 'https://www.airbnb.cn/rooms/45697759?adults=1&children=0&infants=0&translate_ugc=false&source_impression_id=p3_1605804054_WdIg1II96GFT8rRB'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
response = requests.get(url=url, headers=headers,)
response.encoding = 'utf-8'
print(response.content)
"""

"""
Prerequisites:
1. Selenium - 安装第三方包
2. Chrome WebDriver
   - https://chromedriver.chromium.org/downloads 找到对应版本下载
   - 将chromedriver.exe放在Python.exe目录中的Scripts文件夹中
   
"""

import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pickle
import pandas as pd
import numpy as np
import random


def get_page_source(url):
    os.system('taskkill /f /im chromedriver.exe')
    # browser = webdriver.Chrome()
    q_option = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images': 2}  # 不加载图片
    q_option.add_experimental_option('prefs', prefs)
    q_option.add_argument('--headless')                 # 无头浏览器
    q_option.add_argument('--disable-gpu')              # 禁用窗口打开
    browser = webdriver.Chrome(chrome_options=q_option)
    browser.get(url)
    #time.sleep(random.randint(1, 6))
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.close()
    return soup


def get_json(soup):
    """
    :param soup:
    :return content_js:
    """
    content_js = json.loads(soup.find('script', id="data-state").text)  # retrieve content json
    return content_js


def get_info(js):
    """
    :param js:
    :return listing_dataframe:
     - Retrieve detail listing information from search page json content.
     - Use value returned from get_json()
    """
    # pd.set_option('display.max_columns', None)
    # json_pickle = open('jsontemp.bin', 'rb')
    # js = pickle.load(json_pickle)
    # json_pickle.close()
    js_sections = js['niobeClientDataLegacy']['__niobe_denormalized']['queries'][0][1]['dora']['exploreV3']['sections']
    listings = js_sections[len(js_sections)-1]['items']
    listing_df = pd.DataFrame(columns=['id', 'name', 'city', 'neighborhood', 'lat', 'lng', 'avgRating', 'reviewsCount',
                                       'bathrooms', 'bathroomLabel', 'bedrooms', 'bedroomLabel', 'beds', 'guestLabel',
                                       'personCapacity', 'roomType', 'isNewListing', 'isSuperhost',
                                       'previewAmenityNames',
                                       'priceString', 'rateType'])
    # listing_df.set_index(['id'], inplace=True)
    for i, listing in enumerate(listings):
        listing_df.loc[i] = [listing['listing']['id'],
                          listing['listing']['name'],
                          listing['listing']['city'],
                          listing['listing']['neighborhood'],
                          listing['listing']['lat'],
                          listing['listing']['lng'],
                          listing['listing']['avgRating'],
                          listing['listing']['reviewsCount'],
                          listing['listing']['bathrooms'],
                          listing['listing']['bathroomLabel'],
                          listing['listing']['bedrooms'],
                          listing['listing']['bedroomLabel'],
                          listing['listing']['beds'],
                          listing['listing']['guestLabel'],
                          listing['listing']['personCapacity'],
                          listing['listing']['roomType'],
                          listing['listing']['isNewListing'],
                          listing['listing']['isSuperhost'],
                          listing['listing']['previewAmenityNames'],
                          listing['pricingQuote']['priceString'],
                          listing['pricingQuote']['rateType']]
    return listing_df


def get_nextpageurl(soup):
    # print(soup)
    url = soup.find('a', {'aria-label': 'Next'})
    # print(url['href'])
    if url is not None:
        return url['href']
    else:
        return None


def get_neighborhood(js):
    js = json.loads(js)
    nbhs = \
    js['niobeClientDataLegacy']['__niobe_denormalized']['queries'][0][1]['dora']['exploreV3']['filters']['sections'][
        17]['items']
    nbh_df = pd.DataFrame(columns=['id', 'name'])
    for i, nbh in enumerate(nbhs):
        nbh_df.loc[i] = [nbh['params'][0]['value']['longValue'],
                         nbh['title']]
    nbh_df.to_csv('neighborhood_id.csv')


def get_progress():
    if 'neighborhood_id.csv' in os.listdir():
        progress = pd.read_csv(open('neighborhood_id.csv'), index_col='index')
        finished = 1
        for i in progress.index:
            if progress.loc[i]['status'] != 'Done':
                finished = 0
                if progress.loc[i]['status'] == 'In Progress':
                    start_url = 'https://www.airbnb.com' + progress.loc[i]['current_url'] + '&locale=en'
                    return [start_url, i]
                if np.isnan(progress.loc[i]['status']):
                    start_url = 'https://www.airbnb.com/s/New-York--NY--United-States/homes?locale=en&tab_id=home_tab&search_type=filter_change&neighborhood_ids%5B%5D=' + str(
                        progress.loc[i]['id'])
                    return [start_url, i]
        if finished == 1:
            return ['1', 0]
    else:
        return ['0', 0]


def main():
    prog = get_progress()
    if prog[0] != '1' and prog[0] != '0':
        url = prog[0]
        i = prog[1]
        prog_sheet = pd.read_csv('neighborhood_id.csv', index_col='index', encoding='gb2312')
        while url is not None and i <= len(prog_sheet):
            source_soup = get_page_source(url)
            json_content = get_json(source_soup)
            listing_df = get_info(json_content)
            url = get_nextpageurl(source_soup)
            if 'listings.csv' not in os.listdir():
                listing_df.to_csv('listings.csv')
            else:
                listings = pd.read_csv('listings.csv', index_col=0, header=0)
                listings = pd.concat([listings, listing_df], axis=0, ignore_index=True)
                listings.to_csv('listings.csv')
            if url is not None:
                prog_sheet.loc[i, 'status'] = 'In Progress'
                prog_sheet.loc[i, 'current_url'] = url
                prog_sheet.to_csv('neighborhood_id.csv')
                url = 'https://www.airbnb.com' + url + '&locale=en'
                print('1 page get!')
            else:
                prog_sheet.loc[i, 'status'] = 'Done'
                prog_sheet.loc[i, 'current_url'] = ''
                prog_sheet.to_csv('neighborhood_id.csv')
                i += 1
                if i > len(prog_sheet):
                    url = None
                    print('All Done!')
                else:
                    url = 'https://www.airbnb.com/s/New-York--NY--United-States/homes?locale=en&tab_id=home_tab&search_type=filter_change&neighborhood_ids%5B%5D=' + str(prog_sheet.loc[i, 'id'])
                    print('1 page get!')
                    print(prog_sheet.loc[i - 1, 'name'] + ' Finished!')


if __name__ == '__main__':
    # print(get_nextpageurl(get_page_source('https://www.airbnb.com/s/New-York--NY--United-States/homes?locale=en&search_type=pagination&tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&neighborhood_ids%5B%5D=2751&place_id=ChIJOwg_06VPwokRYv534QaPC8g&federated_search_session_id=cd48c92e-da30-4037-b7b0-df30e07f2e17&items_offset=80&section_offset=3'))==None)
    # content = get_json('https://www.airbnb.com/s/New-York--NY--United-States/homes?&query=New%20York&locale=en')
    # json_ = open('jsontemp.bin', 'wb')
    # pickle.dupicklemp(content, json_pickle)
    # json_pickle.close()
    # get_info(content)
    main()

