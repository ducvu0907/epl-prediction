import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import time

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
match_df.to_csv("matches2.csv")
