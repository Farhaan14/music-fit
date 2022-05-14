import requests
import time
import oauth2 as oauth2
from pprint import pprint
import json
import csv

from songRecommender import *


access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzg4M0IiLCJzdWIiOiI3WVg0UFYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNjUxNjgxMDU5LCJpYXQiOjE2NDkwODk0NDF9.hCDHb2NlQkqTYOGkVFTwzDy7mKsqaDO1KvXbCkMokuA'
user_id = '7YX4PV'

playlist_creator = "Dimish"
playlist_id = "2tLMUKxKJXjYV79iPhQzon"

def fitbitAndMusicRecommendation(recommended_df, prevMood, running_df, prevRunning, restless_df, prevRestless):

    ### Heart Rate
    activity_request = requests.get('https://api.fitbit.com/1/user/'+user_id+'/activities/heart/date/today/1d/1min.json', 
    headers={'Authorization': 'Bearer ' + access_token})
    # heartRate = activity_request.json()['activities-heart-intraday']['dataset'][-1]['value']

    ### Walk
    activity_request = requests.get('https://api.fitbit.com/1/user/'+user_id+'/activities/distance/date/today/1d.json',
    headers={'Authorization': 'Bearer ' + access_token})
    # l = activity_request.json()['activities-distance-intraday']['dataset'][-1]['value']
    # sl = activity_request.json()['activities-distance-intraday']['dataset'][-10]['value']

    ### Sleep
    activity_request= requests.get('https://api.fitbit.com/1/user/'+user_id+'/sleep/date/today.json',
    headers={'Authorization': 'Bearer ' + access_token})
    # sleepEfficiency = activity_request.json()['sleep']['efficiency']
 
    ## Testing
    heartRate = 57
    distance = 100
    sleepEfficiency = 70

    if distance > 300:
        running = 1
    else:
        running = 0

    if sleepEfficiency < 85:
        restless = 1
    else: 
        restless = 0

    if heartRate>0 and heartRate<60:
        mood = 1   
    elif heartRate>60 and heartRate<100:
        mood = 0
    else:
        mood = 2

    if prevMood != mood:
        playlist_df = getRecommendations(playlist_creator, playlist_id)

        recommended_df = playlist_df[playlist_df['mood']==mood]
        prevMood = mood

    if prevRunning != running:
        playlist_df = getRecommendations(playlist_creator, playlist_id)

        if running == 1:
            running_df = playlist_df[playlist_df['mood']==1]
            prevRunning = 1
        else:
            df_normal = playlist_df[playlist_df['mood']==0]
            df_calm = playlist_df[playlist_df['mood']==2]
            running_df = pd.concat([df_normal, df_calm])
            prevRunning = 0

    if prevRestless != restless:
        playlist_df = getRecommendations(playlist_creator, playlist_id)
        
        if restless == 1:
            restless_df = playlist_df[playlist_df['mood']==2]
            prevRestless = 1
        else:
            df_normal = playlist_df[playlist_df['mood']==0]
            df_energetic = playlist_df[playlist_df['mood']==1]
            restless_df = pd.concat([df_normal, df_energetic])
            prevRestless = 0

    return recommended_df, prevMood, running_df, prevRunning, restless_df, prevRestless, heartRate, distance, sleepEfficiency

