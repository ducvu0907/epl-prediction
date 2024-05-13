import requests

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats" # entry url
data = requests.get(standings_url)
# print(data.text)

from bs4 import BeautifulSoup
soup = BeautifulSoup(data.text, "html.parser") # initiate bs4 html parser

standings_table = soup.select("table.stats_table")[0] # parse html table
# print(standings_table)
 
# filter team url
links = standings_table.find_all("a")
links = [link.get("href") for link in links]
links = [link for link in links if "/squad" in link]

team_urls = [f"https://fbref.com{link}" for link in links]
# print(team_urls)

team_url = team_urls[0]
data = requests.get(team_url)

import pandas as pd
from io import StringIO
matches = pd.read_html(StringIO(data.text), match="Scores & Fixtures") # extract matches table

# print(matches[0])