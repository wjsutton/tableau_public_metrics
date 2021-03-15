import json
import datetime
import pandas as pd
import urllib3
from pandas.io.json import json_normalize
import numpy as np
import re

def flatten_nested_json_df(df):

    df = df.reset_index()

    print(f"original shape: {df.shape}")
    print(f"original columns: {df.columns}")


    # search for columns to explode/flatten
    s = (df.applymap(type) == list).all()
    list_columns = s[s].index.tolist()

    s = (df.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()

    print(f"lists: {list_columns}, dicts: {dict_columns}")
    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            print(f"flattening: {col}")
            # explode dictionaries horizontally, adding new columns
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f'{col}.')
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns) # inplace

        for col in list_columns:
            print(f"exploding: {col}")
            # explode lists vertically, adding new columns
            df = df.drop(columns=[col]).join(df[col].explode().to_frame())
            new_columns.append(col)

        # check if there are still dict o list fields to flatten
        s = (df[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (df[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()

        print(f"lists: {list_columns}, dicts: {dict_columns}")

    print(f"final shape: {df.shape}")
    print(f"final columns: {df.columns}")
    return df

http = urllib3.PoolManager()
votd = json.loads(http.request('GET',"https://public.tableau.com/api/gallery?page=0&count=10000&galleryType=viz-of-the-day&language=en-us").data)
df = pd.json_normalize(votd['items'], max_level=0)

workbook_df =[]

for i in df.index:

    workbook_url = 'https://public.tableau.com/profile/api/single_workbook/' + votd['items'][i]['workbookRepoUrl']
    workbook = json.loads(http.request('GET',workbook_url).data)
    workbook = pd.json_normalize(workbook)
    
    if 'error.message' in workbook.columns:
        source_url = df['sourceUrl'][i]
        retry = re.search('/views/(.+?)/', source_url)
        if retry is not None:
            retry = retry.group(0)[7:-1]
            workbook_url = 'https://public.tableau.com/profile/api/single_workbook/' + retry
            workbook = json.loads(http.request('GET',workbook_url).data)
            workbook = pd.json_normalize(workbook)
            workbook['workbookRepoUrl'] = votd['items'][i]['workbookRepoUrl']

    workbook_df.append(workbook)

# see pd.concat documentation for more info
workbook_df = pd.concat(workbook_df)

df = pd.merge(df,workbook_df, on='workbookRepoUrl',how='left')
del df['workbook']
if 'error.message' in df.columns:
    del df['error.message']
    del df['error.id']

df['types'] = [','.join(map(str, l)) for l in df['types']]
df['topics'] = [','.join(map(str, l)) for l in df['topics']]
df['badges'] = [','.join(map(str, l)) for l in df['badges']]
df['attributions'] = np.where(len(df['attributions'])>0,True,False) #[','.join(map(str, l)) for l in df['attributions']]

df = df.drop_duplicates()
#print(df)
print(len(df))
#workbooks.to_csv('tableau_public_workbooks.csv', index=False)
df.to_csv('tableau_public_votd.csv', index=False)
