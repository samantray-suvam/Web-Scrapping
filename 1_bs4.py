from bs4 import BeautifulSoup

with open(file="file.html", mode="r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# print(soup.prettify()) 
print(soup.title.text)
print(soup.title)