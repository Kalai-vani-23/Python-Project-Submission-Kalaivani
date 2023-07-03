from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random


response = requests.get(
    'https://gist.github.com/tiangechen/b68782efa49a16edaf07dc2cdaa855ea')
soup = BeautifulSoup(response.content, "html.parser")
web_html = soup.find(
    "table", attrs={"class": 'js-csv-data csv-data js-file-line-container'}).text
# print(web_html)
table = soup.table
table_header = table.find_all('th')
headers = []
for header in table_header:
    headers.append(header.text)
table_rows = table.find_all('tr')
rows = {}
i = 0
for tr in table_rows:
    td = tr.find_all('td')
    temp = []
    for data in td:
        if data.text:
            temp.append(data.text.lower())
    rows[i] = temp
    i += 1
rows.pop(0)
data_frame = pd.DataFrame(headers)
data_frame = data_frame.T
# print(data_frame)
try:
    data_frame.to_csv('output.csv', index=False, header=False)
    data_frame = pd.DataFrame(rows)
    data_frame = data_frame.T
    data_frame.to_csv('output.csv', mode='a', index=False, header=False)

    print("Enter any one genre from following:")
    input_sheet = pd.read_csv('output.csv')
    df = pd.DataFrame(input_sheet)
    genre = df['Genre'].unique()
    print(genre)
    input_genre = input()
    if input_genre not in genre:
        print("Kindly enter anyone genre from the above list")
    else:
        df1 = df[df['Genre'] == input_genre]
        list1 = []
        for i in range(0, len(df1)):
            # print(df1['Film'].iloc[i])
            list1.append(df1['Film'].iloc[i])
        print(f"We can watch this {input_genre} movie:{random.choice(list1)}")
except PermissionError:
    print("Kindly close the output.csv file")
