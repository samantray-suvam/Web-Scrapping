# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# from fake_useragent import UserAgent

# url = "https://quotes.toscrape.com/"

# session=requests.session()

# headers = {
    
#     "User-Agent": UserAgent().random,   
#     # this helps us from being banned
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Connection": "keep-alive",
#     "Upgrade-Insecure-Requests": "1",
#     "Referer": "https://www.google.com/",
#     }

# time.sleep(2)
# r=session.get(url, headers=headers)
# soup = BeautifulSoup(r.content, "html.parser")

# with open("file.html", "w", encoding="utf-8") as f:
#     f.write(r.text) 
#     # encoding allows to write special characters correctly, without Python throwing an error 










# from playwright.sync_api import sync_playwright
# import pandas as pd 

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=True)  # headless mode for automation
#     page = browser.new_page()
#     page.goto("https://rnbtender.nprocure.com/")

#     titles = page.query_selector_all(".table > tr")
#     data = []
#     for title in titles:
#         data.append(title.inner_text())

#     df = pd.DataFrame(data, columns=["Tender Titles"])
#     df.to_excel("tender_titles.xlsx", index=False)
#     print("✅ Tender titles scraped and saved to tender_titles.xlsx")

    
#     browser.close()











import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Send an HTTP request to the target URL
url = "https://quotes.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Step 2: Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Find the data you want (e.g., all quotes and authors)
quotes = []
for quote_block in soup.find_all("div", class_="quote"):
    text = quote_block.find("span", class_="text").get_text(strip=True)
    author = quote_block.find("small", class_="author").get_text(strip=True)
    quotes.append([text, author])

# Step 4: Save the data to Excel
df = pd.DataFrame(quotes, columns=["Quote", "Author"])
df.to_excel("quotes.xlsx", index=False)
print("✅ Quotes scraped and saved to quotes.xlsx")