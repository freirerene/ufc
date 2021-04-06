import requests
from bs4 import BeautifulSoup
import string
import datetime
import pandas as pd

urlheader = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}

ab = list(string.ascii_lowercase)
soup = []
for l in ab:
    markup = requests.get('http://ufcstats.com/statistics/fighters?char=' + l + '&page=all', headers=urlheader).text
    soup.append(BeautifulSoup(markup, 'html.parser'))
    
df = pd.DataFrame(columns=['first_name', 'last_name', 'nickname', 'height', 'weight',
       'reach', 'stance', 'win', 'loss', 'draw', 'belt', 'SLpM', 'StrAcc',
       'SApM', 'StrDef', 'nan', 'TD Avg', 'TD Acc', 'TD Def.', 'Sub. Avg.'])

for s in soup:
    rows = s.find_all("tr", {"class": "b-statistics__table-row"})
    for r in rows[2:]:
        url = r.find('a', {'class':'b-link b-link_style_black'})['href']
        markup_details = requests.get(url, headers=urlheader).text
        soup_details = BeautifulSoup(markup_details, 'html.parser')
    
        details = soup_details.find("div", {"class": "b-list__info-box-left clearfix"}).find_all("li", {"class": "b-list__box-list-item b-list__box-list-item_type_block"})
        data = []
        for i in r.find_all("td", {"class": "b-statistics__table-col"}):
            data.append(i.text)
        for i in details:
            data.append(i.text)

        df.loc[-1] = data
        df.index = df.index + 1
        df = df.sort_index()

df.to_csv('ufc.csv', index=False)
