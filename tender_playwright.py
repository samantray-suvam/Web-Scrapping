from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

def scrape_rnb_tenders():
    all_data = []
    headers = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://rnbtender.nprocure.com/", timeout=60000)
        page.wait_for_timeout(5000)

        first_page = True
        while True:
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table")
            if not table:
                print("No table found on the page!")
                break

            # Extract headers only from the first page
            if first_page:
                header_row = table.find("tr")
                if header_row:
                    headers = [cell.get_text(strip=True) for cell in header_row.find_all("th")]
                first_page = False

            # Extract data rows (skip header row)
            for row in table.find_all("tr")[1:]:
                cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
                if cells:
                    all_data.append(cells)

            # Try to find and click the "Next" button
            try:
                next_button = page.query_selector('a[aria-label="Next"]') or page.query_selector('a:has-text("Next")')
                if next_button and next_button.is_enabled():
                    next_button.click()
                    page.wait_for_timeout(3000)
                else:
                    break
            except Exception as e:
                print("No more pages or error:", e)
                break

        browser.close()

    # Save all data to Excel
    df = pd.DataFrame(all_data, columns=headers if headers else None)
    df.to_excel("tenders_list.xlsx", index=False)
    print("\nData from all pages saved to tenders_list.xlsx")

if __name__ == "__main__":

    scrape_rnb_tenders()