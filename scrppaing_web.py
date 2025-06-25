# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# from fake_useragent import UserAgent

# url = "https://etenders.gov.in/eprocure/app?page=FrontEndLatestActiveTenders"

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










# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import pandas as pd
# import time

# # Set up Selenium WebDriver (make sure you have ChromeDriver installed)
# service = Service(r'C:\WebDrivers\chromedriver.exe')  # Use the actual path to chromedriver.exe
# driver = webdriver.Chrome(service=service)

# url = "https://etenders.gov.in/eprocure/app?page=Home&service=page"
# driver.get(url)
# time.sleep(5)  
# html = driver.page_source

# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html, "html.parser")

# # Parse the table (example for the "Latest Active Tenders" table)
# table = soup.find("table", {"id": "table"})  # Update the id/class as per actual table

# data = []
# columns = []

# if table:
#     # Get headers
#     headers = table.find_all("th")
#     columns = [header.text.strip() for header in headers]

#     # Get rows
#     for row in table.find_all("tr")[1:]:
#         cells = row.find_all("td")
#         if cells:
#             data.append([cell.text.strip() for cell in cells])

#     # Save to Excel
#     df = pd.DataFrame(data, columns=columns)
#     df.to_excel("tenders.xlsx", index=False)
#     print("Data saved to tenders.xlsx")
# else:
#     print("Table not found. Check the table's id or class.")

# driver.quit()







import requests

url = "https://etenders.gov.in/eprocure/app?component=view&page=FrontEndTendersByOrganisation&service=page"

headers = {
    "User-Agent": "Mozilla/5.0",
}

response = requests.get(url, headers=headers)

print(response.text)
