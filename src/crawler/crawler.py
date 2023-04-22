import json
import time
from itertools import chain, product
import random
import os

import jmespath
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

options = uc.ChromeOptions()

# setting profile
# options.user_data_dir = "profile_1"

CRAWL_INTERVAL = 5
driver = uc.Chrome(options=options, user_data_dir="profile_1")
driver.get("https://sahibinden.com")
time.sleep(25)
driver.find_element(By.XPATH, "/html/body/div[3]/div/ul/li[3]/a").text
#$end


def get_ilan_details(url):
    driver.get(url)

    time.sleep(0.1)
    
    try:
        WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="classifiedStatusWarning classifiedExpired"]')))
        return {}
    except:
        pass

    # ilan detail json
    ilan_json_text = driver.find_element(By.XPATH,
        '//div[@id="gaPageViewTrackingJson"]').get_attribute('data-json')
    ilan_json = json.loads(ilan_json_text)

    # combine ilan keys and values
    ilan_keys = jmespath.search('dmpData[*].name', ilan_json)
    ilan_values = jmespath.search('dmpData[*].value', ilan_json)
    ilan_data_json = dict(zip(ilan_keys, ilan_values))

    # geolocation info
    gmap_ele = driver.find_element(By.XPATH, "//div[@id='gmap']")
    lat = gmap_ele.get_attribute("data-lat")
    lon = gmap_ele.get_attribute("data-lon")
    ilan_data_json.update({"lat": lat, "lon": lon})

    # properties
    properties = get_ilan_properties()
    ilan_data_json.update(properties)

    return ilan_data_json

def get_ilan_properties():
    properties_table_element = driver.find_element(By.XPATH, "//div[@id='classifiedProperties']")
    properties_element = properties_table_element.find_elements(By.XPATH, "..//li")
    property_values = dict((k.text, k.get_attribute("class")) for k in properties_element)
    return property_values


def get_links(category_url):
    links_page = category_url
    driver.get(links_page)
    time.sleep(1)

    total_ilan_number = driver.find_element(By.XPATH, 
        '//div[@class="result-text"]').find_element(By.XPATH, './/span').text
    total_ilan_number = int(total_ilan_number.replace('.', '').replace(" ilan", ''))-10

    navi_buttons = driver.find_element(By.XPATH, 
        '//ul[@class="pageNaviButtons"]')

    last_page_element = navi_buttons.find_element(By.XPATH, 
        './/li//input[@id="currentPageValue"]')
    current_page = last_page_element.get_attribute('value')

    categories = driver.find_elements(By.XPATH, '//li[@class="cl2"]')
    category_links = [cat.find_element(By.XPATH, 
        './/a').get_attribute('href') for cat in categories]

    navi_buttons = driver.find_element(By.XPATH, 
        '//ul[@class="pageNaviButtons"]')
    last_page_element = navi_buttons.find_elements(By.XPATH, './/li')[-2]
    last_page = last_page_element.find_element(By.XPATH, 
        '//a').get_attribute('title')

    all_links = []
    while True:
        table_xp = '//table[@id="searchResultsTable"]'
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, table_xp)))
        except TimeoutException:
            print(
                f"Presence of all elements Timeout Error")
            raise
        time.sleep(2)
        table = driver.find_element(By.XPATH,table_xp)
        hrefs = table.find_elements(By.XPATH,
            './/td[@class="searchResultsTitleValue leafContent"]')

        listings = []
        for href in hrefs:
            ad_id = href.find_element(By.XPATH,
                './/following-sibling::div[@class="action-wrapper"]').get_attribute("data-classified-id")
            link = href.find_element(By.XPATH,
                './/following-sibling::a[contains(@href, "/ilan/")]').get_attribute('href')
            listings.append([int(ad_id), link, None])
        all_links.append(listings)
        # print(f"{current_page} / {last_page} --- # of new ads: {number_of_new_ads} ---- # of Total unchecked URLs: {total_new_ads}")
        next_button_obj = driver.find_elements(By.XPATH,
            '//a[(@class="prevNextBut") and (@title="Sonraki")]')
        if not next_button_obj:
            break


        next_button = next_button_obj[0]
        loc_nxt = next_button.location_once_scrolled_into_view
        loc_y = loc_nxt['y'] - 70
        driver.execute_script(f"window.scrollBy(0, {loc_y})")
        driver.find_element(By.XPATH,'//a[@title="Sonraki"]').click()
        loading_element = driver.find_element(By.XPATH,
            '//div[@class="opening"]')

        try:
            WebDriverWait(driver, 25).until(
                EC.invisibility_of_element_located((By.XPATH, '//div[@class="opening"]')))
        except TimeoutException:
            print(f"Loading element Timeout Error")
    ls = list(chain(*all_links))
    links_df = pd.DataFrame(ls, columns=["ad_id", "link", "checked"]).drop_duplicates(subset=["link"])
    return links_df

def get_all_ilan_data(links):
    final_data = []
    for ad_id, link, _ in links:
        data = get_ilan_details(link)
        data.update({"ad_id": ad_id})
        final_data.append(data)
        interval = random.randint((CRAWL_INTERVAL -  0.5) * 1000, (CRAWL_INTERVAL +  0.5) * 1000) / 1000
        time.sleep(interval)
    return final_data


def iterate_categories(city_list: list):
    base_1 = ["kiralik", "satilik",]
    base_2 = ["daire", "mustakil-ev", "residence", "villa"]
    base_3 = ["sahibinden", "emlak-ofisinden"]
    category_combionations = list(product(city_list, base_1, base_2, base_3))

    for city, sale_type, konut_type, ad_owner in category_combionations:
        category_url = f"https://www.sahibinden.com/{sale_type}-{konut_type}/{city}/{ad_owner}?pagingSize=50"
        print(category_url)
        link_path = f"/Users/berkayg/Codes/sahibinden-project/data/links/{city}_{sale_type}_{konut_type}_{ad_owner}.csv"
        if not os.path.exists(link_path):
            all_links = get_links(category_url)
            all_links.to_csv(link_path, index=False)

# cities = ["istanbul"]
# iterate_categories(cities)
# all_links = get_links()
# import pickle
# with open("links_list.pkl", "rb") as rd:
#     all_links = pickle.load(rd)
all_links = pd.read_csv("/Users/berkayg/Codes/sahibinden-project/data/unified_links.csv")
all_links = all_links.to_numpy().tolist()
dt  = get_all_ilan_data(all_links)
dt.to_csv("/Users/berkayg/Codes/sahibinden-project/data/21_april_23.csv", index=False)
print("Done")