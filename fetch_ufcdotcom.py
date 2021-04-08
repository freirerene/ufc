import requests
from bs4 import BeautifulSoup
import string
import datetime
import pandas as pd

urlheader = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}

soup = {}

for i in range(0,88):
    markup_links = requests.get('https://www.ufc.com.br/athletes/all?gender=All&search=&page='+str(i), headers=urlheader).text
    soup_links = BeautifulSoup(markup_links, 'html.parser')
    for j in range(0,len(soup_links.find_all("li", {"class":"l-flex__item"})) - 1):
        try:
            url = 'https://www.ufc.com.br' + soup_links.find_all("li", {"class":"l-flex__item"})[j].find("a")['href']
            markup = requests.get(url, headers=urlheader).text
            soup[url] = BeautifulSoup(markup, 'html.parser')
        except Exception as e:
            pass

# we save what we get
with open('soup.data', 'wb') as filehandle:
    pickle.dump(soup, filehandle)

name, active, country, team, age, height, weight, started_on, reach, reach_legs, wld, sig_strikes, sig_strikes_connected, sig_strikes_pm, absorbed_strikes_pm, strikes_standing, strikes_clinch, strikes_ground, strikes_head, strikes_body, strikes_legs, take_down, take_down_attempts, takedown_p15min, fin_p15min, strike_defense_pct, takedown_defense_pct, knockdown_mean, mean_fighttime, ko_tko, dec, fin = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

for so in list(soup.values()):
    
    name.append(list(soup.keys())[list(soup.values()).index(so)])
    
    wld.append(so.find("div", {"class":"c-hero__headline-suffix tz-change-inner"}).text)
    stats = so.find_all("div", {"class":"c-stats-group-2col__item"})
    stats_2 = so.find_all("div", {"class":"c-stats-group-3col__item"})
    bio = so.find("div", {"class":"c-bio__content"})
    
    # bio
    bio_1 = bio.find_all("div", {"class":"c-bio__row--1col"})
    bio_2 = bio.find_all("div", {"class":"c-bio__row--2col"})
    bio_3 = bio.find_all("div", {"class":"c-bio__row--3col"})
    
    try:
        active.append(bio_1[0].find("div", {"class":"c-bio__text"}).text)
    except:
        active.append(np.nan)
    try:
        country.append(bio_1[1].find("div", {"class":"c-bio__text"}).text)
    except:
        country.append(np.nan)
    try:
        team.append(bio_2[0].find("div", {"class":"c-bio__text"}).text)
    except:
        team.append(np.nan)
    try:
        age.append(bio_3[0].find("div", {"class":"field field--name-age field--type-integer field--label-hidden field__item"}).text)
    except:
        age.append(np.nan)
    try:
        height.append(bio_3[0].find_all("div", {"class":"c-bio__text"})[1].text)
    except:
        height.append(np.nan)
    try:
        weight.append(bio_3[0].find_all("div", {"class":"c-bio__text"})[2].text)
    except:
        weight.append(np.nan)
    try:
        started_on.append(bio_3[1].find_all("div", {"class":"c-bio__text"})[0].text)
    except:
        started_on.append(np.nan)
    try:
        reach.append(bio_3[1].find_all("div", {"class":"c-bio__text"})[1].text)
    except:
        reach.append(np.nan)
    try:
        reach_legs.append(bio_3[1].find_all("div", {"class":"c-bio__text"})[2].text)
    except:
        reach_legs.append(np.nan)

    # strikes
    strikes = so.find("div", {"class":"l-overlap-group__item--odd"})
    try:
        sig_strikes_connected.append(strikes.find_all("dd", {"class":"c-overlap__stats-value"})[0].text)
    except:
        sig_strikes_connected.append(np.nan)
    try:
        sig_strikes.append(strikes.find_all("dd", {"class":"c-overlap__stats-value"})[1].text)
    except:
        sig_strikes.append(np.nan)
        

    try:
        strikes_perminute = stats[0]
        try:
            sig_strikes_pm.append(strikes_perminute.find_all("div", {"class":"c-stat-compare__number"})[0].text)
        except:
            sig_strikes_pm.append(np.nan)
        try:
            absorbed_strikes_pm.append(strikes_perminute.find_all("div", {"class":"c-stat-compare__number"})[1].text)
        except:
            absorbed_strikes_pm.append(np.nan)
    except:
        sig_strikes_pm.append(np.nan)
        absorbed_strikes_pm.append(np.nan)

    try:
        strikes_standing.append(stats_2[0].find_all("div", {"class":"c-stat-3bar__value"})[0].text)
    except:
        strikes_standing.append(np.nan)
    try:
        strikes_clinch.append(stats_2[0].find_all("div", {"class":"c-stat-3bar__value"})[1].text)
    except:
        strikes_clinch.append(np.nan)
    try:
        strikes_ground.append(stats_2[0].find_all("div", {"class":"c-stat-3bar__value"})[2].text)
    except:
        strikes_ground.append(np.nan)
    try:
        strikes_head.append(stats_2[1].find("text", {"id":"e-stat-body_x5F__x5F_head_percent"}).text)
    except:
        strikes_head.append(np.nan)
    try:
        strikes_body.append(stats_2[1].find("text", {"id":"e-stat-body_x5F__x5F_body_percent"}).text)
    except:
        strikes_body.append(np.nan)
    try:
        strikes_legs.append(stats_2[1].find("text", {"id":"e-stat-body_x5F__x5F_leg_percent"}).text)
    except:
        strikes_legs.append(np.nan)

    # grappling
    grappling = so.find("div", {"class":"l-overlap-group__item--even"})
    try:
        take_down.append(grappling.find_all("dd", {"class":"c-overlap__stats-value"})[0].text)
    except:
        take_down.append(np.nan)
    try:
        take_down_attempts.append(grappling.find_all("dd", {"class":"c-overlap__stats-value"})[1].text)
    except:
        take_down_attempts.append(np.nan)
        

    try:
        grappling_per15min = stats[1]
        try:
            takedown_p15min.append(grappling_per15min.find_all("div", {"class":"c-stat-compare__number"})[0].text)
        except:
            takedown_p15min.append(np.nan)
        try:
            fin_p15min.append(grappling_per15min.find_all("div", {"class":"c-stat-compare__number"})[1].text)
        except:
            fin_p15min.append(np.nan)
    except:
        takedown_p15min.append(np.nan)
        fin_p15min.append(np.nan)
    

    # defense
    try:
        defense = stats[2]
        try:
            strike_defense_pct.append(defense.find_all("div", {"class":"c-stat-compare__number"})[0].text)
        except:
            strike_defense_pct.append(np.nan)
        try:
            takedown_defense_pct.append(defense.find_all("div", {"class":"c-stat-compare__number"})[1].text)
        except:
            takedown_defense_pct.append(np.nan)
    except:
        strike_defense_pct.append(np.nan)
        takedown_defense_pct.append(np.nan)


    # means
    try:
        means = stats[3]
        try:
            knockdown_mean.append(means.find_all("div", {"class":"c-stat-compare__number"})[0].text)
        except:
            knockdown_mean.append(np.nan)
        try:
            mean_fighttime.append(means.find_all("div", {"class":"c-stat-compare__number"})[1].text)
        except:
            mean_fighttime.append(np.nan)
    except:
        knockdown_mean.append(np.nan)
        mean_fighttime.append(np.nan)

    # victories
    try:
        ko_tko.append(stats_2[2].find_all("div", {"class":"c-stat-3bar__value"})[0].text)
    except:
        ko_tko.append(np.nan)
    try:
        dec.append(stats_2[2].find_all("div", {"class":"c-stat-3bar__value"})[1].text)
    except:
        dec.append(np.nan)
    try:
        fin.append(stats_2[2].find_all("div", {"class":"c-stat-3bar__value"})[2].text)
    except:
        fin.append(np.nan)


data = {'name': name, 'active': active, 'country': country, 'team': team, 'age': age, 'height': height, 'weight': weight, 'started_on': started_on, 'reach': reach, 'reach_legs': reach_legs, 'wld': wld, 'sig_strikes': sig_strikes, 'sig_strikes_connected': sig_strikes_connected, 'sig_strikes_pm': sig_strikes_pm, 'absorbed_strikes_pm': absorbed_strikes_pm, 'strikes_standing': strikes_standing, 'strikes_clinch': strikes_clinch, 'strikes_ground': strikes_ground, 'strikes_head': strikes_head, 'strikes_body': strikes_body, 'strikes_legs': strikes_legs, 'take_down': take_down, 'take_down_attempts': take_down_attempts, 'takedown_p15min': takedown_p15min, 'fin_p15min': fin_p15min, 'strike_defense_pct': strike_defense_pct, 'takedown_defense_pct': takedown_defense_pct, 'knockdown_mean': knockdown_mean, 'mean_fighttime': mean_fighttime, 'ko_tko': ko_tko, 'dec': dec, 'fin': fin}

df = pd.DataFrame(data)
df.to_csv('ufc.csv', index=False)