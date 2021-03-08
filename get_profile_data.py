import requests
import json
import datetime
import pandas as pd

profile = json.loads(requests.get("https://public.tableau.com/profile/api/wjsutton").text)
workbooks = json.loads(requests.get("https://public.tableau.com/profile/api/wjsutton/workbooks?count=300&index=0").text)
datetime = datetime.datetime.now()

all_favs = []
all_views = []
all_workbooks = len(workbooks)
for book in range(all_workbooks -1):
    favs = workbooks[book]['numberOfFavorites']
    views = workbooks[book]['viewCount']
    all_favs.append(favs)
    all_views.append(views)

total_favs = sum(all_favs)
total_views = sum(all_views)

headers = ['profile','datetime','following','followers','published_workbooks','total_favourites','total_views']
row = [profile['profileName'],datetime,profile['totalNumberOfFollowing'],profile['totalNumberOfFollowers'],profile['visibleWorkbookCount'],total_favs,total_views]

df = pd.DataFrame(columns=[headers], data=[row])
df.to_csv('tableau_public_stats.csv', index=False)

#print(df)