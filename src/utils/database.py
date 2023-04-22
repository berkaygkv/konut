import pandas as pd
import glob

def _read_links_data():
    links = glob.glob(pathname="*csv", root_dir="/Users/berkayg/Codes/sahibinden-project/data/links")
    return links

def unify_ad_links():
    df = pd.DataFrame()
    for file_name in _read_links_data():
        df_file = pd.read_csv("/Users/berkayg/Codes/sahibinden-project/data/links" + "/" + file_name)
        df = pd.concat([df, df_file])
    return df.drop_duplicates(subset=["link"]).drop(columns=["Unnamed: 0"])

def save_links():
    df = unify_ad_links()
    print(df.head())
    df.to_csv("/Users/berkayg/Codes/sahibinden-project/data/unified_links.csv", index=False)

if __name__ == "__main__":
    save_links()