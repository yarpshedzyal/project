import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

def web_scrape_price(url):
    price = '0'
    response = requests.get(url)

    if response.status_code == 200:
    # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        print(response.text)
        price_in_table_element = soup.select('#item-page > div > div:nth-child(2) > div > div.product-page > div > div:nth-child(3) > div:nth-child(1) > div > div')
        if price_in_table_element:
            print("Selected element text:", price_in_table_element[0].get_text())
        else:
            print("No element found with the specified selector.")


def price_scrap():
    df = pd.read_csv('SHELF_KIT_PARTS.csv') # read 

    def calculate_prices(row):
        # You can implement your logic here to calculate prices based on the 'web' and 'the' fields
        # For demonstration purposes, let's assume the price for 'web' and 'the' is twice the value in those fields
        price_web = row['web'] * 2
        price_the = row['the'] * 2
        return price_web, price_the

    # Apply the function to each row in the DataFrame
    df['price_web'], df['price_the'] = zip(*df.apply(calculate_prices, axis=1))

    # Write the updated DataFrame back to the CSV file
    df.to_csv('output_shelf_kit_parts.csv', index=False)

        

print(web_scrape_price('https://www.webstaurantstore.com/regency-12-x-24-nsf-black-epoxy-wire-shelf/460EB1224.html'))