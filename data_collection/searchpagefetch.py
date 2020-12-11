"""
title: searchpagefetch.py
date: 25-NOV-2020
author: Chengyu Wu (chengyu2)
description: This module is used to fetch content from search pages of Airbnb.com for each city.
Using Selenium, BeautifulSoup, and json, this module can return information of each listing shown on a search page.
It would also find the URL of the next page and self-navigate to turn pages. On the highest level,
a progress management CSV file can be used by this module to track and resume collecting progress
in case of functionality or connectivity failures.
"""

"""
Prerequisites:
1. Selenium
   If haven't installed in your environment, use "pip install Selenium" in Python Console to install it.
2. Chrome WebDriver
   - Download corresponding version (OS&Chrome Version) of WebDriver via https://chromedriver.chromium.org/downloads
   - Put chromedriver.exe into the "script" folder at the same directory as your current using Python.exe

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
    """
    Open up a headless, no-window, and no-image browser to load and return page source code.
    """
    os.system('taskkill /f /im chromedriver.exe')                            # Kill existing chromedriver processes to release resource.
    q_option = webdriver.ChromeOptions()                                     # Specify customized options
    prefs = {'profile.managed_default_content_settings.images': 2}           # Don't load images.
    q_option.add_experimental_option('prefs', prefs)
    q_option.add_argument('--headless')                                      # Use headless browser.
    q_option.add_argument('--disable-gpu')                                   # Don't open real window.
    browser = webdriver.Chrome(chrome_options=q_option)                      # Open browser.
    browser.get(url)                                                         # Get source code from the window.
    time.sleep(random.randint(1, 6))                                         # Sleep a random period of time to lower query frequency.
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)") # Scroll to the bottom to ensure everything get loaded
    soup = BeautifulSoup(browser.page_source, 'lxml')
    browser.close()
    return soup


def get_json(soup):
    """
    Normalize json content to dictionary
    """
    content_js = json.loads(soup.find('script', id="data-state").text)  # retrieve json content
    return content_js


def get_info(js):
    """
    :param js:
    :return listing_dataframe:
     - Retrieve detail listing information from search page json content.
     - Use value returned from get_json()
    """
    # pd.set_option('display.max_columns', None)               Temp pickle file for debug, not used in actual scraping.
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
    """
    Find link to the next page, return None if not applicable.
    """
    url = soup.find('a', {'aria-label': 'Next'})
    if url is not None:
        return url['href']
    else:
        return None


def get_neighborhood(js):
    """
    This is a one-time function only used to get the list of all neighborhood.
    """
    js = json.loads(js)
    nbhs = js['niobeClientDataLegacy']['__niobe_denormalized']['queries'][0][1]['dora']['exploreV3']['filters']['sections'][17]['items']
    nbh_df = pd.DataFrame(columns=['id', 'name'])
    for i, nbh in enumerate(nbhs):
        nbh_df.loc[i] = [nbh['params'][0]['value']['longValue'],
                         nbh['title']]
    nbh_df.to_csv('neighborhood_id.csv')


def get_progress():
    """
    Locate the current progress,
    return the URL of the last stop,
    generate new URL if not applicable,
    return 1 if a neighborhood is finished,
    return 0 if all neighborhoods are finished.
    """
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
    """
    Call get_progress() to locate current progress,
    call get_page_source() using the saved or generated url.
    Then call get_json(), get_info() and get_nextpageurl() to decode and extract specific data.
    Loops are controlled by the dataframe from the progress managing CSV file.
    """
    prog = get_progress()
    if prog[0] != '1' and prog[0] != '0':
        url = prog[0]
        i = prog[1]
        prog_sheet = pd.read_csv('../data_collection/neighborhood_id.csv', index_col='index', encoding='gb2312')
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
    # Notice - Enabling one block at a time is recommended, try not to enable them all.

    # Main Function
    main()

    # Unit Test of Opening Browser Window. Enable it if you need to test your package installation & connectivity.
    #browser = webdriver.Chrome()
    #browser.get('https://www.airbnb.com/s/New-York--NY--United-States/homes?adults=1&refinement_paths%5B%5D=%2Fhomes&search_type=autocomplete_click&tab_id=home_tab&query=New%20York%2C%20NY%2C%20United%20States&locale=en')
