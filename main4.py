from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import datetime
import os
import time 
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
date_list = pd.date_range(start = "2000-02-01", end=datetime.date.today(), freq='1d') #get the dates


chrome_options = Options()  
chrome_options.add_argument("--headless") # Opens the browser up in background
# driver = webdriver.Chrome()

def get_batsmen(date):
    url = f'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting?at={date}'
    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        
        browser.implicitly_wait(10) #waiting for the browser to load
        html = browser.page_source
        
    
    doc = BeautifulSoup(html, "html.parser")
    find_class = doc.find_all("td", class_ = 'table-body__cell rankings-table__name name') #Parsing the webpage for the player names using class
    player_list = []
    find_top = doc.find('div', class_='rankings-block__banner--name-large') #Finding the top ranked player name
    player_list.append(find_top.text)
    for item in find_class:
        player_name = item.find("a") #Finding the player name using link anchor tag
       
        try:    #Using a try except block to catch any exceptions
            player_list.append(player_name.text)
        except AttributeError:
            continue
    df = pd.DataFrame(player_list, columns = ['Player Name'])
    browser.delete_all_cookies() #removing the cookies
    browser.quit() #Closing the web driver 
    return df

def get_bowler(date):
    url = f'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling?at={date}'
    
    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        html = browser.page_source
    doc = BeautifulSoup(html, "html.parser")
    find_class = doc.find_all("td", class_ = 'table-body__cell rankings-table__name name')
    player_list = []
    find_top = doc.find('div', class_='rankings-block__banner--name-large')
    player_list.append(find_top.text)
    for item in find_class:
        player_name = item.find("a")
       
        try:
            player_list.append(player_name.text)
        except AttributeError:
            continue
    df = pd.DataFrame(player_list, columns = ['Player Name'])
    browser.delete_all_cookies() #removing the cookies
    browser.quit() #Closing the web driver 
    return df

def get_allrounder(date):
    url = f'https://www.icc-cricket.com/rankings/mens/player-rankings/odi/all-rounder?at={date}'
    
    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        html = browser.page_source
    doc = BeautifulSoup(html, "html.parser")
    find_class = doc.find_all("td", class_ = 'table-body__cell rankings-table__name name')
    player_list = []
    find_top = doc.find('div', class_='rankings-block__banner--name-large')
    player_list.append(find_top.text)
    for item in find_class:
        player_name = item.find("a")
        # print(player_name.text)
        try:
            player_list.append(player_name.text)
        except AttributeError:
            continue
    df = pd.DataFrame(player_list, columns = ['Player Name'])
    browser.delete_all_cookies() #removing the cookies
    browser.quit() #Closing the web driver 
    return df

#Storing the data into multiple csvs

for date in date_list:
    year = date.year
    month = date.month
    day = date.day
    date = date.strftime("%Y-%m-%d") #Converting to date format
    newpath = rf'C:\Users\divya\OneDrive\Desktop\8th Sem\ISB assignment\{year}' #Making folder named year
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    newpath1 = rf'C:\Users\divya\OneDrive\Desktop\8th Sem\ISB assignment\{year}\{month}' #Making second folder
    if not os.path.exists(newpath1):
        os.makedirs(newpath1)
    newpath2 = rf'C:\Users\divya\OneDrive\Desktop\8th Sem\ISB assignment\{year}\{month}\{day}'
    if not os.path.exists(newpath2):
        os.makedirs(newpath2)
    get_batsmen(date).to_csv(newpath2+'/batsmen.csv')
    
    get_bowler(date).to_csv(newpath2+'/bowler.csv')
    
    get_allrounder(date).to_csv(newpath2+'/allrounder.csv')
    
    
