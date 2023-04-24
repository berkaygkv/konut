import requests
import pandas as pd
import json
import time
import random

from bs4 import BeautifulSoup
import jmespath
from tqdm import tqdm

CRAWL_INTERVAL = 6

payload={}

headers = {
    'Cookie': 'cdid=VZFsEyNHwy424tYQ6445969d; csid=fG2IFsGTjWQAwh+uWC8fPk3H+whrRLUi0u5qMNkvNtNSMINkytgKFOgG4DFNf8T2rvMYBpGJlMRcPJzjZQFYrKwEfrrE93Bv+UbTvKFmlBNRd2vBG4luifrklUTBmtz3IpskFwF/tbzJ7Tk70hUIN/su+//SzR3FsekzqJRaY5Dz1EwjlD9hKvRg+0oR7gqd; st=aac7ac9d59d7646cf9e04d966812266b565d2634780f78ad21b33267ea155a20fd6ded04993c7027b9450e77591953c7d4172a122b4bd34f9; vid=332',
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}

#$end

all_links = pd.read_csv(r"E:\~Folders\Coding env\sahibinden_house\data\unified_links.csv")
last_ad = 1087177100
last_index = all_links.loc[all_links["ad_id"] == last_ad].index[0]
all_links = all_links.to_numpy().tolist()[last_index + 32:]

def get_ilan_details(url):
    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'html.parser') 

    ilan_json = json.loads(soup.find(id="gaPageViewTrackingJson")["data-json"])

    if ilan_json.get("route") == "error":
        return {}

    # combine ilan keys and values
    ilan_keys = jmespath.search('dmpData[*].name', ilan_json)
    ilan_values = jmespath.search('dmpData[*].value', ilan_json)
    ilan_data_json = dict(zip(ilan_keys, ilan_values))

    lat = soup.find(id="gmap")["data-lat"]
    lon = soup.find(id="gmap")["data-lon"]
    ilan_data_json.update({"lat": lat, "lon": lon})

    properties_keys = [k.get_text().strip() for k in soup.find(id="classifiedProperties").find_all("li")]
    properties_values = [k["class"] for k in soup.find(id="classifiedProperties").find_all("li")]
    properties = dict((key, len(val) > 0) for key, val in zip(properties_keys, properties_values))
    ilan_data_json.update(properties)

    interval = random.randint((CRAWL_INTERVAL -  0.5) * 1000, (CRAWL_INTERVAL +  0.5) * 1000) / 1000
    time.sleep(interval)
    return ilan_data_json

def get_all_ilan_data(links):
    final_data = []
    for ad_id, link, _ in tqdm(links):
        data = get_ilan_details(link)
        data.update({"ad_id": ad_id})
        final_data.append(data)
    return final_data

data = get_all_ilan_data(all_links)