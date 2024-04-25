import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import re

def clean_price_string(price_str):
    parts = price_str.split(".", 1)
    if len(parts) == 2:
        cleaned_price = f"{parts[0]}.{parts[1][:2]}"
    else:
        cleaned_price = price_str.replace(".", "")
    cleaned_price = re.sub(r"[^\d.]", "", cleaned_price)
    return cleaned_price

def get_minimum_buy_number(soup):
    min_must_text_element = soup.find("p", {"class": "min-must-text"})
    if min_must_text_element:
        minimum_buy_number = re.search(r"\d+", min_must_text_element.text)
        if minimum_buy_number:
            return int(minimum_buy_number.group())
    return None

def parser_solo(url):
    response = requests.get(url)
    stock = "Out"
    price = "0"

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        svg_element = soup.find("svg", {"class": "block mx-auto align-middle"})
        phrase_unavailable = "This Product is no longer available"
        phrase_unavailable_2 = "This product is no longer available"
        phrase_out_of_stock = "Notify me when this product is back in stock"
        phrase_works_with = 'Works With'
        product_from_line = 'Other Products from this Line'
        selector_for_sale = '#priceBox > div.pricing > p.sale-price > span.text-black.font-bold.bg-yellow-400.rounded-sm.antialiased.mr-1.mt-0\.5.px-3\/4.py-0\.5.text-sm'

        if svg_element or (phrase_unavailable in soup.get_text()) or (phrase_out_of_stock in soup.get_text()) or (phrase_unavailable_2 in soup.get_text()):
            stock = "Out"
        else:
            stock = "In"

        min_must_text_element = soup.find("p", {"class": "min-must-text"})
        minimum_buy = get_minimum_buy_number(soup)

        table_element = soup.select_one("#priceBox")

            # else:
            #     return 'Price element not found'
            
        # if product_from_line in soup.get_text():
        #     price_element = soup.select_one('#priceBox > div.pricing > p > span')

        p_r_error_text = 'Contact us or '
        if p_r_error_text in soup.get_text():
            price_element = soup.select_one('#priceBox > div.pricing > div > p.leading-none.mb-0')
            if price_element:
                price = price_element.text.strip().replace("$", "").replace(",", "")
                filtered_price = re.sub(r'[^\d.]', '', price)
                price = clean_price_string(filtered_price)
            # else:
            #     return 'Price element not found'
     
        was_price_element = soup.select_one("p.was-price")
        if was_price_element:
            price = was_price_element.text.strip().replace("$", "").replace(",", "")
            filtered_price = re.sub(r'[^\d.]', '', price)
            price = clean_price_string(filtered_price)

        if minimum_buy:
            price = str(float(price) * minimum_buy)

    return [table_element]

# df = pd.read_csv('SHELF_KIT_PARTS.csv')

# # Create empty lists to store scraped data
# scraped_prices = []
# scraped_stocks = []

# # Iterate through each row in the DataFrame
# for index, row in df.iterrows():
#     # Extract the URL from the appropriate column in the row
#     url = row['web']
    
#     # Scrape data from the URL using the scrape_data function
#     price, stock = parser_solo(url)
    
#     # Append scraped data to the lists
#     scraped_prices.append(price)
#     scraped_stocks.append(stock)

# # Add scraped data to the DataFrame as new columns
# df['scraped_price'] = scraped_prices
# df['scraped_stock'] = scraped_stocks

# # Write the updated DataFrame to a new CSV file
# df.to_csv('output_shelf_kit_parts.csv', index=False)

print(parser_solo('https://www.webstaurantstore.com/regency-12-x-24-nsf-black-epoxy-wire-shelf/460EB1224.html'))
