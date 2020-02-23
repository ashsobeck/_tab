#!/usr/bin/env python3

#just returns the top 10 songs in the daily 200
import requests
from bs4 import BeautifulSoup 
from datetime import date
from time import time
from time import sleep
import pandas as pd

def getTop10():
  #url needed for getting the daily 200
  url = 'https://spotifycharts.com/regional/us/daily/'

  spotifyList = requests.get(url)
  #sleep after request to make sure it goes through
  sleep(1)

  soup = BeautifulSoup(spotifyList.text, 'html.parser')

  chart = soup.find('table', {'class': 'chart-table'})
  tbody = chart.find('tbody')

  bigTable = []

  for songs in tbody.find_all('tr'):
    rank = songs.find('td', {'class': 'chart-table-position'}).text
    songname = songs.find('td', {'class': 'chart-table-track'}).find('strong').text
    artist = songs.find('td', {'class': 'chart-table-track'}).find('span').text

    bigTable.append( [rank, songname, artist] )
  
  data = pd.DataFrame(bigTable, columns =['Rank', 'Title', 'Artist'])
  print(data)

  with open('top10' + date.strftime('%Y-%m-%d') + '.csv', 'w') as file:
    data.to_csv(file, header=False, index=False)


