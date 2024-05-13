import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time

# standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats" # entry url
# data = requests.get(standings_url)
# # print(data.text)

# soup = BeautifulSoup(data.text, "html.parser") # initiate bs4 html parser

# standings_table = soup.select("table.stats_table")[0] # parse html table
# # print(standings_table)
 
# # filter team url
# links = standings_table.find_all("a")
# links = [link.get("href") for link in links]
# links = [link for link in links if "/squad" in link]

# team_urls = [f"https://fbref.com{link}" for link in links]
# # print(team_urls)

# team_url = team_urls[0]
# data = requests.get(team_url)

# matches = pd.read_html(StringIO(data.text), match="Scores & Fixtures") # extract matches table

# # print(matches[0])

# # scrape shooting stats
# soup = BeautifulSoup(data.text, "html.parser")
# links = soup.find_all("a")
# links = [link.get("href") for link in links]
# links = [link for link in links if link and "all_comps/shooting/" in link]
# # print(links)

# data = requests.get(f"https://fbref.com{links[0]}")
# shooting = pd.read_html(StringIO(data.text), match="Shooting")[0]
# # print(data.text)
# # print(shooting.head())
# shooting.columns = shooting.columns.droplevel() # remove multi-level index

# team_data = matches[0].merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date") # merge columns
# print(shooting.shape)

# scraping
years = list(range(2024, 2018, -1))
all_matches = []
url = "https://fbref.com/en/comps/9/Premier-League-Stats"

for year in years:
  data = requests.get(url)
  soup = BeautifulSoup(data.text, "html.parser")
  table = soup.select("table.stats_table")[0]
  links = [l.get("href") for l in table.find_all("a")]
  links = [l for l in links if "/squads/" in l]
  teams_url = [f"https://fbref.com{l}" for l in links]

  previous_season = soup.select("a.prev")[0].get("href")
  url = f"https://fbref.com{previous_season}"

  for team_url in teams_url:
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
    data = requests.get(team_url)
    matches = pd.read_html(StringIO(data.text), match="Scores & Fixtures")[0]
    soup = BeautifulSoup(data.text, "html.parser")
    links = [l.get("href") for l in soup.find_all("a")]
    links = [l for l in links if l and "all_comps/shooting" in l]
    data = requests.get(f"https://fbref.com{links[0]}")
    shooting = pd.read_html(StringIO(data.text), match="Shooting")[0]
    shooting.columns = shooting.columns.droplevel()
    try: 
      team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
    except ValueError:
      continue
    team_data = team_data[team_data["Comp"] == "Premier League"]
    team_data["Season"] = year
    team_data["Team"] = team_name
    all_matches.append(team_data)
    time.sleep(1) # interval between scrapes
  
# convert to csv file
match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
match_df.to_csv("matches.csv")