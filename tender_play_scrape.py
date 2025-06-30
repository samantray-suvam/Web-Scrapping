# scraper_rnb.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_rnb_tenders():
    all_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://rnbtender.nprocure.com/")
        page.wait_for_timeout(5000)

        while True:
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table")
            if not table:
                print("No table found on the page!")
                break

            # Extract rows
            for row in table.find_all("tr"):
                cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                if cells:
                    all_data.append(cells)

            # Try to find and click the "Next" button
            try:
                # Adjust selector as needed for your site
                next_button = page.query_selector('a[aria-label="Next"]') or page.query_selector('a:has-text("Next")')
                if next_button and next_button.is_enabled():
                    next_button.click()
                    page.wait_for_timeout(3000)  # Wait for next page to load
                else:
                    break  # No more pages
            except Exception as e:
                print("No more pages or error:", e)
                break

        browser.close()

    # Save all data to Excel
    df = pd.DataFrame(all_data)
    df.to_excel("tenders_list.xlsx", index=False, header=False)
    print("\nData from all pages saved to tenders_list.xlsx")

if __name__ == "__main__":
    scrape_rnb_tenders()
