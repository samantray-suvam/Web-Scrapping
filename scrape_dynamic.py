# code with playwright for dynamic content scraping:



from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

url = "https://rnbtender.nprocure.com/view-nit-home"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(10000)  # Wait 10 seconds for JS to load

    # Print all frame URLs
    print("All frames on the page:")
    for frame in page.frames:
        print(frame.url)

    # Try to find a table in the main page
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    # If not found, try in iframes
    if not table:
        for frame in page.frames:
            if frame.url != page.url:
                frame_html = frame.content()
                frame_soup = BeautifulSoup(frame_html, "html.parser")
                table = frame_soup.find("table")
                if table:
                    print(f"Table found in iframe: {frame.url}")
                    soup = frame_soup
                    break

    if not table:
        print("❌ No table found on the page or in iframes.")
    else:
        # Extract headers
        headers = [cell.get_text(strip=True) for cell in table.find('tr').find_all(['th', 'td'])]
        # Extract rows
        data = []
        for row in table.find_all('tr')[1:]:
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            if row_data:
                data.append(row_data)
        # Save to Excel
        df = pd.DataFrame(data, columns=headers)
        df.to_excel("scraped_table.xlsx", index=False)
        print("✅ Table scraped and saved to scraped_table.xlsx")

    browser.close()







# code with selenium for dynamic content scraping:
    
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import openpyxl

# # Path to ChromeDriver 
# chromedriver_path = webdriver.Chrome(service=ChromeDriverManager().install())

# # Setup Chrome with Selenium
# service = Service(chromedriver_path)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=service, options=options)

# # Target URL of the tender detail page (example, replace with actual)
# url = "https://rnbtender.nprocure.com/view-nit-home"  # change this if needed
# driver.get(url)

# # Wait for full page load (increase delay if needed)
# time.sleep(5)

# # Find all table rows
# table_rows = driver.find_elements(By.XPATH, "//table//tr")

# # Extract key-value pairs from table
# tender_data = []
# for row in table_rows:
#     cols = row.find_elements(By.TAG_NAME, "td")
#     if len(cols) == 2:
#         key = cols[0].text.strip()
#         value = cols[1].text.strip()
#         tender_data.append((key, value))

# # Save to Excel using openpyxl
# import openpyxl
# workbook = openpyxl.Workbook()
# sheet = workbook.active
# sheet.title = "Tender Details"

# # Write headers
# sheet.cell(row=1, column=1, value="Field")
# sheet.cell(row=1, column=2, value="Value")

# # Write data
# for i, (key, value) in enumerate(tender_data, start=2):
#     sheet.cell(row=i, column=1, value=key)
#     sheet.cell(row=i, column=2, value=value)

# # Save Excel file
# workbook.save("tender_data.xlsx")
# print("✅ Data saved to 'tender_data.xlsx'")

# # Close browser
# driver.quit()