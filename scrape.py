import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Request the page
url = "https://quotes.toscrape.com/"
response = requests.get(url)

# Step 2: Parse the page
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Find all quote blocks
quotes = soup.find_all('div', class_='quote')

# Step 4: Extract data
data = []
for quote in quotes:
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    data.append([text, author])

# Step 5: Save to CSV
df = pd.DataFrame(data, columns=['Quote', 'Author'])
df.to_excel("quotes.xlsx", index=False)

print("✅ Scraping done! Data saved to quotes.csv")
