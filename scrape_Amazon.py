import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

url = "https://www.amazon.in/s?k=books&rh=p_n_binding_browse-bin%3A1318376031&dc&ds=v1%3AfRgoJ1XEfxJUN6EJhYLeExhhcDyUfmxt936ORK094FU&crid=2403G4FXZOCRS&qid=1750938052&rnid=1318374031&sprefix=book%2Caps%2C352&ref=sr_nr_p_n_binding_browse-bin_2"

Headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

webpage = requests.get(url, headers=Headers)
print("Status code:", webpage.status_code)

soup = BeautifulSoup(webpage.content, "html.parser")

links = soup.find_all("a", attrs={"class": "a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal"})
print("No. of Links found = ", len(links))

book_data_list = []

for i in range(min(5, len(links))):
    product_url = "https://www.amazon.in/" + links[i].get("href")
    new_webpage = requests.get(product_url, headers=Headers)
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    # Extract Product Title
    title_tag = new_soup.find("span", attrs={"id": "productTitle"})
    book_title = title_tag.get_text(strip=True) if title_tag else ""
    # print("Book Title:", book_title)

    # Extract Product Price
    price_tag = new_soup.find("span", attrs={"class": "a-price-whole"})
    book_price = price_tag.get_text(strip=True) if price_tag else ""
    # print("Prices: ", book_price)


    # Extract Product Rating
    rating_tag = new_soup.find("span", attrs={"class": "a-icon-alt"})
    book_rating = rating_tag.get_text(strip=True) if rating_tag else ""
    # print("Rating: ", book_rating)

    # Extract Product Author
    byline = new_soup.find("div", id="bylineInfo")
    if byline:
        author_link = byline.find("a")
        book_auth = author_link.get_text(strip=True) if author_link else ""
    else:
        book_auth = ""
    # print("Author: ", book_auth)

    print()  # Print a blank line between books

    # Collect all data in a dictionary
    book_data = {
        "Title": book_title,
        "Price": book_price,
        "Rating": book_rating,
        "Author": book_auth
    }
    book_data_list.append(book_data)
    time.sleep(2)  # Be polite to the server

# Create a DataFrame and save to Excel
df = pd.DataFrame(book_data_list)
df.to_excel("amazon_book_details.xlsx", index=False)
print("✅ Book details saved to amazon_book_details.xlsx")
