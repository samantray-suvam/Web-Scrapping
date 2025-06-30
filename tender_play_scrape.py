# scraper_rnb.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_rnb_tenders():
    with sync_playwright() as p:
        # Launch browser (headless=False during development so you can see it)
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        
        # Go to the target URL
        page.goto("https://rnbtender.nprocure.com/")

        # Wait for the main content to load; adjust selector if needed
        page.wait_for_timeout(5000)  # simple fixed wait; you could wait for a specific element too

        # Get fully rendered page content
        html = page.content()
        
        browser.close()  # close the browser as soon as you grab the page

    # Now parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Example: Find the first table on the page
    table = soup.find("table")

    if not table:
        print("No table found on the page!")
        return

    # Extract rows
    data = []
    for row in table.find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
        if cells:
            data.append(cells)
            # print(cells)  # print for debug

    # Optional: save to Excel
    df = pd.DataFrame(data)
    df.to_excel("rnb_tenders.xlsx", index=False, header=False)
    print("\n✅ Data saved to rnb_tenders.xlsx")

if __name__ == "__main__":
    scrape_rnb_tenders()
