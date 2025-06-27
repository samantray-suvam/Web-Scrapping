import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

url = "https://www.amazon.in/s?k=adventure+book&crid=1JADR5B88B73J&sprefix=adventure+%2Caps%2C204&ref=nb_sb_ss_mvt-t11-ranker_1_10"

#headers for request
Headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

#HTTP requests
webpage = requests.get(url, headers=Headers)
print("Status code:", webpage.status_code)

#proof of successful request
print(type(webpage.content))

#soup object containig all data
soup = BeautifulSoup(webpage.content, "html.parser")

#fetch links of list of tag objects
links = soup.find_all("a", attrs={"class": "a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal"})

#check the length of the links
print("Length of Parameter = " , len(links))


#automate the extraction of links
book_data_list = []

for i in range(3):
    product_list = "https://www.amazon.in/s?k=adventure+book&crid=1JADR5B88B73J&sprefix=adventure+%2Caps%2C204&ref=nb_sb_ss_mvt-t11-ranker_1_10" + links[i].get("href")


    #Extracting other lists
    new_webpage = requests.get(product_list, headers=Headers)
    print("Status code:", new_webpage.status_code)

    print("Length of full webpage:", len(new_webpage.content))


    # Create a BeautifulSoup object for the new webpage containing all the data
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")
    # print("Length of new_soup:", len(new_soup))


    #Extract Product title
    book_title_tag = new_soup.find("a", attrs={"class": "a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal"})
    book_title = book_title_tag.get_text(strip=True)
    print("Book Title: ", book_title)


    #Extract Product Price
    book_price = new_soup.find("span", attrs={"class": "a-price-whole"}).get_text(strip=True)
    book_price_num = float(book_price.replace(",", ""))
    print("Price: ", book_price_num)


    #Extract product rating
    book_rating = new_soup.find("span", attrs={"class": "a-icon-alt"}).get_text(strip=True)
    print("Rating:", book_rating)


    # Extract product author (get text, not just the tag)
    book_auth = new_soup.find("a", attrs={"class": "a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style"}).get_text(strip=True)
    print("Author: ", book_auth)


    # Collect all data in a dictionary
    book_data = {
        "Title": book_title,
        "Price": book_price,
        "Rating": book_rating,
        "Author": book_auth
    }
    book_data_list.append(book_data)
    print(f"Book {i+1} data collected")
    time.sleep(5)

# Create a DataFrame and save to Excel
df = pd.DataFrame(book_data_list)
df.to_excel("amazon_book_details.xlsx", index=False)
print("✅ Book details saved to amazon_book_details.xlsx")
