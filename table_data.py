from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1️⃣ Launch browser and go to homepage
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
parent_url = "https://rnbtender.nprocure.com/"
driver.get(parent_url)
print("⏳ Waiting for page to load...")
time.sleep(5)  # Let pop-up auto-close

# 2️⃣ Click the anchor with id="tenderInProgress"
try:
    tender_in_progress = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "tenderInProgress"))
    )
    tender_in_progress.click()
    print("✅ Clicked 'Tender In Progress'")
except Exception as e:
    print(f"❌ Could not click 'Tender In Progress': {e}")
    driver.quit()
    exit()

# 3️⃣ Switch to the new tab
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
driver.switch_to.window(driver.window_handles[-1])
print("🔄 Switched to new tab.")

# 4️⃣ Wait for tables to load
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.TAG_NAME, "table"))
)
child_html = driver.page_source
child_soup = BeautifulSoup(child_html, 'html.parser')
child_tables = child_soup.find_all("table")

# 5️⃣ Save all tables to a single Excel workbook, each in a separate sheet
excel_file = "tenderInProgress_tables.xlsx"
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    for idx, table in enumerate(child_tables):
        rows = []
        for tr in table.find_all("tr"):
            row = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if row:
                rows.append(row)
        df = pd.DataFrame(rows)
        sheet_name = f"Table_{idx+1}"
        df.to_excel(writer, index=False, header=False, sheet_name=sheet_name)
        print(f"✅ Saved {sheet_name} with {len(rows)} rows.")

print(f"🎉 All tables saved to {excel_file}")
driver.quit()