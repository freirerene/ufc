import requests
from bs4 import BeautifulSoup
import string
import pandas as pd
import pickle

urlheader = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}

links = []

for i in range(0,72):
    url = 'https://www.ufc.com.br/events?page='+str(i)
    markup = requests.get(url, headers=urlheader).text
    soup = BeautifulSoup(markup, 'html.parser')
    pages = soup.find("details", {"id":"events-list-past"}).find_all("li", {"class":"l-listing__item"})
    for p in pages:
        links.append(p.find("h3", {"class":"c-card-event--result__headline"}).find("a")['href'])

soup = []
for l in links:
    url = 'https://www.ufc.com.br' + l
    markup = requests.get(url, headers=urlheader).text
    soup.append(BeautifulSoup(markup, 'html.parser'))

results, results_b, results_c = [], [], []

for s in soup:
    try:
        fights = s.find("ul", {"class":"l-listing__group--bordered"}).find_all("li", {"class":"l-listing__item"})
    except:
        pass
    try:
        fights_b = s.find("details", {"class":"fight-card-prelims"}).find_all("li", {"class":"l-listing__item"})
    except:
        pass

    try:
        fights_c = s.find("details", {"class":"fight-card-prelims-early"}).find_all("li", {"class":"l-listing__item"})
    except:
        pass

    for f in fights:      
        red = f.find("div", {"class":"c-listing-fight__corner--red"})
        name_red = red.find("div", {"class":"c-listing-fight__corner-name"}).text
        outcome_red = red.find("div", {"class":"c-listing-fight__outcome-wrapper"}).text
        
        blue = f.find("div", {"class":"c-listing-fight__corner--blue"})
        name_blue = blue.find("div", {"class":"c-listing-fight__corner-name"}).text
        outcome_blue = blue.find("div", {"class":"c-listing-fight__outcome-wrapper"}).text
                          
        results.append((name_red, outcome_red, name_blue, outcome_blue))
        

    for f in fights_b:
        red_b = f.find("div", {"class":"c-listing-fight__corner--red"})
        outcome_red_b = red_b.find("div", {"class":"c-listing-fight__outcome-wrapper"}).text
        name_red_b = red_b.find("div", {"class":"c-listing-fight__corner-name"}).text

        blue_b = f.find("div", {"class":"c-listing-fight__corner--blue"})
        outcome_blue_b = blue_b.find("div", {"class":"c-listing-fight__outcome-wrapper"}).text
        name_blue_b = blue_b.find("div", {"class":"c-listing-fight__corner-name"}).text
        results_b.append((name_red_b, outcome_red_b, name_blue_b, outcome_blue_b))

    for f in fights_c:
        red_c = f.find("div", {"class":"c-listing-fight__corner--red"})
        outcome_red_c = red_c.find("div", {"class":"c-listing-fight__outcome-wrapper"}).text
        name_red_c = red_c.find("div", {"class":"c-listing-fight__corner-name"}).text

        blue_c = f.find("div", {"class":"c-listing-fight__corner--blue"})
        outcome_blue_c = blue_c.find("div", {"class":"c-listing-fight__outcome-wrapper"}).text
        name_blue_c = blue_c.find("div", {"class":"c-listing-fight__corner-name"}).text
        results_c.append((name_red_c, outcome_red_c, name_blue_c, outcome_blue_c))

df1 = pd.DataFrame(results, columns=['name_red', 'outcome_red', 'name_blue', 'outcome_blue'])
df2 = pd.DataFrame(results_b, columns=['name_red', 'outcome_red', 'name_blue', 'outcome_blue'])
df3 = pd.DataFrame(results_c, columns=['name_red', 'outcome_red', 'name_blue', 'outcome_blue'])
df = pd.concat([df1, df2, df3])
df.to_csv('bouts.csv', index=False)