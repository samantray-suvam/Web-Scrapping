import pandas as pd
from bs4 import BeautifulSoup
import requests

url = "https://www.amazon.in/s?k=adventure+book&crid=1JADR5B88B73J&sprefix=adventure+%2Caps%2C204&ref=nb_sb_ss_mvt-t11-ranker_1_10"

Headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive"
}

webpage = requests.get(url, headers=Headers)
soup = BeautifulSoup(webpage.content, "html.parser")

links = soup.find_all("a", attrs={"class": "a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal"})
print("Length of Parameter = " , len(links))

book_data_list = []

for i in range(3):  # For the first three books
    product_url = "https://www.amazon.in" + links[i].get("href")
    new_webpage = requests.get(product_url, headers=Headers)
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")

    # Extract Product title
    title_tag = new_soup.find("span", attrs={"id": "productTitle"})
    book_title = title_tag.get_text(strip=True) if title_tag else "N/A"

    # Extract Product Price
    price_tag = new_soup.find("span", attrs={"class": "a-price-whole"})
    book_price = price_tag.get_text(strip=True) if price_tag else "N/A"

    # Extract Product Rating
    rating_tag = new_soup.find("span", attrs={"class": "a-icon-alt"})
    book_rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

    # Extract Product Author
    byline = new_soup.find("div", id="bylineInfo")
    if byline:
        author_link = byline.find("a")
        book_auth = author_link.get_text(strip=True) if author_link else "N/A"
    else:
        book_auth = "N/A"

    # Collect all data in a dictionary
    book_data = {
        "Title": book_title,
        "Price": book_price,
        "Rating": book_rating,
        "Author": book_auth
    }
    book_data_list.append(book_data)
    print(f"✅ Book {i+1} details scraped.")

# Create a DataFrame and save to Excel
df = pd.DataFrame(book_data_list)
df.to_excel("amazon_book_details.xlsx", index=False)
print("✅ All book details saved to amazon_book_details.xlsx")
