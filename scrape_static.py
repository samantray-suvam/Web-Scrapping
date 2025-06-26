import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace with the actual tender page URL
url = "https://rnbtender.nprocure.com/view-nit-home"

headers = {
    'User-Agent': 'Mozilla/5.0'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Get all table rows
rows = soup.find_all("tr")

data = {}
for row in rows:
    cells = row.find_all("td")
    if len(cells) == 2:
        key = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True)
        data[key] = value

# Convert to DataFrame and Save
df = pd.DataFrame([data])
df.to_excel("tender_details.xlsx", index=False)

print("✅ Scraped tender details saved to tender_details.xlsx")
