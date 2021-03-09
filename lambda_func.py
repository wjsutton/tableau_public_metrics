import json
import boto3
import os
import sys
import uuid
from datetime import datetime
import pandas as pd
import urllib3
from urllib.parse import unquote_plus

http = urllib3.PoolManager()

s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

bucket = s3.Bucket('MY-AWS-BUCKET') 
key = 'FILE-NAME.csv'

# lambda function
def lambda_handler(event,context):
    # download s3 csv file to lambda tmp folder
    # local_file_name = '/tmp/FILE-NAME.csv' #
    # s3.Bucket(MY-AWS-BUCKET).download_file(key,local_file_name)
    # s3_data = pd.read_csv(local_file_name)
    
    response = s3_client.get_object(Bucket='MY-AWS-BUCKET', Key=key)
    content = response['Body']
    s3_data = pd.read_csv(content)
    print('file read')

    profile = json.loads(http.request('GET',"https://public.tableau.com/profile/api/wjsutton").data)
    workbooks = json.loads(http.request('GET',"https://public.tableau.com/profile/api/wjsutton/workbooks?count=300&index=0").data)
    now = datetime.now()
    print('calls made')
    
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
    row = [profile['profileName'],now,profile['totalNumberOfFollowing'],profile['totalNumberOfFollowers'],profile['visibleWorkbookCount'],total_favs,total_views]
    entry = pd.DataFrame(columns=[headers], data=[row])
    
    existing_rows = len(s3_data['profile'])
    
    for i in range(existing_rows):
        exist = [s3_data['profile'][i]
        ,s3_data['datetime'][i]
        ,s3_data['following'][i]
        ,s3_data['followers'][i]
        ,s3_data['published_workbooks'][i]
        ,s3_data['total_favourites'][i]
        ,s3_data['total_views'][i]]
        
        exist = pd.DataFrame(columns=[headers], data=[exist])
        entry = entry.append(exist, ignore_index=True)
    
    print('entry appended')

    entry.to_csv('/tmp/FILE-NAME.csv', index=False, mode='w+')
    print('file written locally')
    
    # upload file from tmp to s3 key
    bucket.upload_file('/tmp/FILE-NAME.csv', key)
    print('file uploaded to s3')
    
    return {
        'message': 'success!!'
    }



