import pandas as pd
from bs4 import BeautifulSoup as bs


# Scraping on First Sample
soup = bs(tabScript,"html.parser")

myTable = soup.find('table',{'class':"type 1 table"})
myTable

row_headers = []
for x in myTable.find_all('tr'):
    for y in x.find_all('th'):
        row_headers.append(y.text)
row_headers

tableValues = []
for x in myTable.find_all('tr')[1:]:
    td_tags = x.find_all('td')
    td_val = [y.text for y in td_tags]
    tableValues.append(td_val)
tableValues

pd.DataFrame(tableValues,columns=row_headers)


# Scraping on second sample
# web = rqst.get("https://fastestlaps.com/tracks/adm-miachkovo")

# soup = bs(web.content,"html.parser")


# tableHead = soup.thead
# tableHead


# row_headers = []
# for x in tableHead.find_all('tr'):
#     for y in x.find_all('th'):
#         row_headers.append(y.text)
# row_headers


# tableBody = soup.tbody
# tableBody


# tableValues = []
# for x in tableBody.find_all('tr')[1:]:
#     td_tags = x.find_all('td')
#     td_val = [y.text for y in td_tags]
#     tableValues.append(td_val)
# tableValues


# df = pd.DataFrame(tableValues,columns=row_headers)
# df.to_excel(r"D:\Learnerea\Tables\tabledata.xlsx",index=False)