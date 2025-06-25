import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from fake_useragent import UserAgent

url = "https://etenders.kerala.gov.in/nicgep/app"

session=requests.session()

headers = {
    
    "User-Agent": UserAgent().random,   
    # this helps us from being banned
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
    }

time.sleep(2)
r=session.get(url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

with open("file.html", "w", encoding="utf-8") as f:
    f.write(r.text) 
    # encoding allows to write special characters correctly, without Python throwing an error 