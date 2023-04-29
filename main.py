import undetected_chromedriver as uc
import time
from src.crawler.crawler import *
from src.utils.constants import PathConstants
from src.utils.database import *

def start_crawling():
    CRAWL_INTERVAL = 7
    options = uc.ChromeOptions()
    options.user_data_dir = "profile_1"

    driver = uc.Chrome(headless=False, version_main=112)
    driver.get("https://sahibinden.com")
    time.sleep(25)

    # cities = ["istanbul"]
    # iterate_categories(cities)
    # all_links = get_links()

    #all_links = pd.read_csv(r"E:\~Folders\Coding env\sahibinden_house\data\unified_links.csv")
    #last_ad = 1083838204
    #last_index = all_links.loc[all_links["ad_id"] == last_ad].index[0]
    #all_links = all_links.to_numpy().tolist()[last_index:]

    dt = get_all_ilan_data(all_links)
    print("Done")

manager = DBManager("data/database.sqlite")
print(PathConstants.database_path)
iterate_categories(["istanbul"], manager)
# get_all_ilan_data(manager)