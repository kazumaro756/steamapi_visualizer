#!/usr/bin/env python
# coding: utf-8

# ## API情報を取得
# 

import requests
import json
import pandas as pd
import boto3
import datetime
import os
from io import StringIO


# APIのひな型
api_key = os.environ['steamapikey']
user_key = os.environ['steamuserkey']
url= "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json&include_appinfo=1".format(api_key,user_key)


# S3のクレデンシャル情報は環境設定で指定。
S3_accesskey = os.environ['s3accesskey']
S3_secretkey = os.environ['s3secretkey']


# S3のバケットを指定
Bucket_profile = 'buc-steamapi'




r = requests.get(url)
# 結果はJSON形式なのでデコードする
data = json.loads(r.text) 


df = pd.DataFrame(data['response']['games'])  

df = df[["appid","name","playtime_forever"]]

df["day"] = datetime.date.today()



def  upload_df_to_s3_as_csv(df):
    s3 = boto3.resource('s3',
                      aws_access_key_id=S3_accesskey,
                      aws_secret_access_key=S3_secretkey,
                      region_name='ap-northeast-1')

    
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3.Object(Bucket_profile, 'dailydata/df_{}.csv'.format(datetime.date.today())).put(Body=csv_buffer.getvalue())
    


upload_df_to_s3_as_csv(df)
