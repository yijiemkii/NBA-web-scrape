# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 12:08:18 2022

@author: lenovo
"""
#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

#%%
df_salary = pd.DataFrame(columns=['Player','Salary','Year'])
browser = webdriver.Chrome("C:/Users/lenovo/Desktop/NBA/chromedriver.exe")

for yr in range(1990, 2020):
    page_num = str(yr) + '-' + str(yr+1) +'/'
    url = 'https://hoopshype.com/salaries/players/' + page_num
    browser.get(url)
    source = browser.page_source

    soup = BeautifulSoup(source, "html.parser")
    salarysoup = soup.find_all('td', "hh-salaries-sorted")
    namesoup = soup.find_all('td', "name")
    namelist = [name.get_text(strip=True) for name in namesoup]
    salarylist = [salary.get_text(strip=True) for salary in salarysoup]

    
    data_tuples = list(zip(namelist[1:],salarylist[1:]))
    temp_df = pd.DataFrame(data_tuples, columns=['Player','Salary'])
    temp_df['Year'] = yr+1
    df_salary = df_salary.append(temp_df)
    #time.sleep(1)
url = "https://hoopshype.com/salaries/players/"
browser.get(url)
source = browser.page_source

soup = BeautifulSoup(source, "html.parser")
salarysoup = soup.find_all('td', "hh-salaries-sorted")
namesoup = soup.find_all('td', "name")
namelist = [name.get_text(strip=True) for name in namesoup]
salarylist = [salary.get_text(strip=True) for salary in salarysoup]


data_tuples = list(zip(namelist[1:],salarylist[1:]))
temp_df = pd.DataFrame(data_tuples, columns=['Player','Salary'])
temp_df['Year'] = 2022
df_salary = df_salary.append(temp_df)
browser.close()

#%%
df_salary.to_excel("C:/Users/lenovo/Desktop/salary91-22.xlsx",
                   sheet_name="1",index=True,header=True)

#%%
browser = webdriver.Chrome("C:/Users/lenovo/Desktop/NBA/chromedriver.exe")
df_per = pd.DataFrame(columns=['Player','PER','Year','regular/post'])
typedict = {
    2: "regular",
    3: "post"}
for year in range(2009, 2023):
    for qualified in [2,3]:
        url = 'http://insider.espn.com/nba/hollinger/statistics/_/page/1/year/{0}/seasontype/{1}/qualified/false'.format(year, qualified)
        browser.get(url)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        npage = int(soup.find_all('div', "page-numbers")[0].text[-2:])
        for i in range(1,npage+1):
            url = 'http://insider.espn.com/nba/hollinger/statistics/_/page/{0}/year/{1}/seasontype/{2}/qualified/false'.format(i, year, qualified)
            browser.get(url)
            source = browser.page_source
            soup = BeautifulSoup(source, 'html.parser')
            infosoup = soup.find_all('tr', re.compile("player"))
        
            namelist = [name.find_all('td')[1].text for name in infosoup]
            perlist = [name.find_all('td')[11].text for name in infosoup]
            #namelist2 = [name.get_text(strip=True) for name in namesoup]
        
            data_tuples = list(zip(namelist, perlist))
            temp_df = pd.DataFrame(data_tuples, columns=['Player','PER'])
            temp_df['Year'] = year
            temp_df['regular/post'] = typedict[qualified]
            df_per = df_per.append(temp_df)
            time.sleep(1)
browser.close()

#%%
df_per.to_excel("C:/Users/lenovo/Desktop/per09-22.xlsx",
                   sheet_name="1",index=True,header=True)

#%%
df_pick = pd.DataFrame(columns=['Player','Overallpick','Year'])
browser = webdriver.Chrome("C:/Users/lenovo/Desktop/NBA/chromedriver.exe")

for yr in range(1990, 2022):
    url = 'https://www.nba.com/stats/draft/history/?Season=' + str(yr)
    browser.get(url)
    time.sleep(1)
    source = browser.page_source

    soup = BeautifulSoup(source, "html.parser")
    infosoup = soup.find_all('tbody')

    namelist = [name.get_text(strip=True) for name in infosoup[1].find_all('tr')]
    picklist = [name.find_all('td')[6].text for name in infosoup[0].find_all('tr')]

    
    data_tuples = list(zip(namelist,picklist))
    temp_df = pd.DataFrame(data_tuples, columns=['Player','Overallpick'])
    temp_df['Year'] = yr
    df_pick = df_pick.append(temp_df)
browser.close()
#%%
df_pick.to_excel("C:/Users/lenovo/Desktop/pick90-21.xlsx",
                   sheet_name="1",index=True,header=True)















