import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np


# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": "productTitle"})
        title_string = title.get_text(strip=True)
    except AttributeError:
        title_string = ""

    return title_string


# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={"class": "a-price-whole"}).get_text(strip=True)
    except AttributeError:
        price = ""

    return price


# Function to extract Product Author
def get_author(soup):
    try:
        author = soup.find("span", class_="author")
        if author:
            author_string = author.get_text(strip=True)
        else:
            byline = soup.find("div", id="bylineInfo")
            if byline:
                author_link = byline.find("a")
                author_string = author_link.get_text(strip=True) if author_link else ""
            else:
                author_string = ""
    except AttributeError:
        author_string = ""

    return author_string


if __name__ == "__main__":

    #adding user agent to headers
    Headers = ({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",})


    # URL of the Amazon page to scrape
    url = "https://www.amazon.in/s?k=adventure+book&crid=1JADR5B88B73J&sprefix=adventure+%2Caps%2C204&ref=nb_sb_ss_mvt-t11-ranker_1_10"


    #HTTP requests
    webpage = requests.get(url, headers=Headers)
    print("Status code:", webpage.status_code)

    # Parsing the webpage content
    soup = BeautifulSoup(webpage.content, "html.parser")


    #Fetching links of list of tag objects
    links = soup.find_all("a", attrs={""})


    # Extracting product details
    product_details = {
        "title": get_title(soup),
        "price": get_price(soup),
        "author": get_author(soup)
    }

    # Displaying the extracted product details
    for key, value in product_details.items():
        print(f"{key.capitalize()}: {value}")