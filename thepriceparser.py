import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

def price_scrap():
    df = pd.read_csv('file_for_proj_1.csv') # read 

    for index,row in df.iterrows():
        thr_link = row['THR']                    # extract data for scrap 3 links and multiplier for shelves, need to rememeber that ther is always 4 and ONLY 4 posts
        thr_post = row ['posts THR']
        thr_shelv = row['shelves THR']
        shelves_number = row['shelves x']

        response = requests.get(thr_link)
        with open('status_code.txt', 'w') as f:
            f.write(str(response.status_code))
        time.sleep(5)

        

price_scrap()