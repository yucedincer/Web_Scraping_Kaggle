from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import logging
import pandas as pd
import sys
import timeit
import time
import csv
import re
from random import randint
from time import sleep
#
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

start_time = time.time()

# options = Options()
# options.binary_location = "/Applications/GoogleChrome.app/Contents/MacOS/GoogleChrome"
# options = Options()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("start-maximized")
# options.add_argument("disable-infobars")
# options.add_argument("--disable-extensions")


#driver = webdriver.Chrome(chrome_options=options)

# payload = {'key': 'eb14ef1467a2f3bbc0a376ac44ce01f3', 'url':'https://httpbin.org/ip', 'render': 'true'}

# print("Chrome Browser Initialized in Headless Mode")


driver = webdriver.Chrome()
driver.get("https://www.kaggle.com/kernels?sortBy=voteCount&group=everyone&pageSize=500")
# time.sleep(5)


# Scrolls 20 elements every loop.. So, 50 * 20 = 1000 elements.
for i in range(1,65):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

csv_file = open('k_test_data.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)

url_list = []

counter = 900
while counter < 1500:
    sleep(4)

    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    kaggle_kernels = {}

    # VOTES
    try:
        vote_count = driver.find_elements_by_xpath((
            './/span[@class="vote-button__vote-count"]'))[counter].text
    except:
        vote_count = ""

        # KERNEL NAME
    try:
        kernel_name = driver.find_elements_by_xpath((
            "//div[@class='kernel-list-item__name false']"))[counter].text
    except:
        kernel_name = ""

        # DATA USED
    try:
        data_used = driver.find_elements_by_xpath(
            ('//p[@class="kernel-list-item__details"]/span[2]/span'))[counter].text.split()[1:]
        data_used = ' '.join(data_used)
    except:
        data_used = ""

        # TAGS
    try:
        tags = driver.find_elements_by_xpath((
            "//span[@class='sc-bmyXtO iMVSiV']"))[counter].text
    except:
        tags = ""

        # MEDAL
    try:
        medal = driver.find_elements_by_xpath((
            "//span[@class='kernel-list-item__name']/img"))[counter].get_attribute('title')
    except:
        medal = ""

        # OUTPUT TYPE
    try:
        output_type = driver.find_elements_by_xpath((
            "//div[@class='kernel-list-item__info-blocks']/span[1]"))[counter].get_attribute('data-tooltip')
    except:
        output_type = ""

        # TYPE (SCRIPT OR NOTEBOOK)
    try:
        type_output = driver.find_elements_by_xpath((
            "//div[@class='kernel-list-item__info-blocks']/span[2]"))[counter].get_attribute('data-tooltip').split()[3:]
        type_output = ' '.join(type_output)
    except:
        type_output = ""

        # LANGUAGE
    try:
        language = driver.find_elements_by_xpath((
            "//div[@class='kernel-list-item__info-blocks']/span[3]"))[counter].get_attribute('data-tooltip').split()[5:]
        language = ' '.join(language)
    except:
        language = ""

        # NUMBER OF COMMENTS
    try:
        comment_count = driver.find_elements_by_xpath((
            "//div[@class='kernel-list-item__info-blocks']/span[4]"))[counter].get_attribute('data-tooltip').split()[3: -1]
        comment_count = ' '.join(comment_count)
    except:
        comment_count = ""

        # # URL FOR USERS
    try:
        url = driver.find_elements_by_xpath((
            ".//a[@class='avatar']"))[counter].get_attribute('href')
    except:
        url = ""

    kaggle_kernels['vote_count'] = vote_count
    kaggle_kernels['kernel_name'] = kernel_name
    kaggle_kernels['data_used'] = data_used
    kaggle_kernels['tags'] = tags
    kaggle_kernels['medal'] = medal
    kaggle_kernels['output_type'] = output_type
    kaggle_kernels['type_output'] = type_output
    kaggle_kernels['language'] = language
    kaggle_kernels['comment_count'] = comment_count
    kaggle_kernels['url'] = url

    # Append the list of urls with new url
    url_list.append(url)

    writer.writerow(kaggle_kernels.values())

    counter += 1

    print("-" * 50)
    print(counter)

csv_file.close()

print('\n''\n''\n'"-------------USER SCRAPING STARTING-------------"'\n''\n''\n')


########################################################

#____________USER SCRAPING PART STARTS HERE____________#

########################################################


kaggle_file = pd.read_csv('k_test_data.csv')
csv_file = open('k_test_user_data.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)

for u in url_list:

    print(u)

    driver.get(u)
    sleep(4)

    user_info = {}

    # USER NAME
    try:
        user_name = driver.find_element_by_xpath((
            '//span[@class="profile__head-display-name"]')).text
    except:
        user_name = ""

        # JOIN DATE OF USER
    try:
        join_date = driver.find_element_by_xpath((
            '//p[@class="profile__user-metadata"]/span')).get_attribute('title').\
            split()[1:4]
        join_date = ' '.join(join_date)
    except:
        join_date = ""

        # NUMBER OF FOLLOWERS
    try:
        num_followers = driver.find_element_by_xpath((
            '//div[@class="profile__user-followers-item"]')).text
    except:
        num_followers = ""

        # JOB TITLE
    try:
        job_title = driver.find_element_by_xpath((
            '//p[@class="profile__user-occupation"]')).text
    except:
        job_title = ""

        # USER LOCATION
    try:
        user_location = driver.find_element_by_xpath((
            '//p[@class="profile__user-location"]')).text
    except:
        user_location = ""

        # WHAT KIND OF USER
    try:
        type_user = driver.find_element_by_xpath((
            '//a[@href="/progression"]/p[2]')).text
    except:
        type_user = ""

        # BIO
    try:
        bio_user = driver.find_element_by_xpath((
            '//div[@class="markdown-converter__text--rendered"]')).text
    except:
        bio_user = ""

    user_info['user_name'] = user_name
    user_info['join_date'] = join_date
    user_info['num_followers'] = num_followers
    user_info['job_title'] = job_title
    user_info['user_location'] = user_location
    user_info['type_user'] = type_user
    user_info['bio_user'] = bio_user

    writer.writerow(user_info.values())
    print(user_info)

    counter += 1

    print("-" * 50)

driver.close()

csv_file.close()

end_time = time.time()

# fin
