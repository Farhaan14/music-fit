import requests
import time
import oauth2 as oauth2
from pprint import pprint
import json
import csv

from songRecommender import *


access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzg4M0IiLCJzdWIiOiI3WVg0UFYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNjUxNjgxMDU5LCJpYXQiOjE2NDkwODk0NDF9.hCDHb2NlQkqTYOGkVFTwzDy7mKsqaDO1KvXbCkMokuA'
user_id = '7YX4PV'

prevMood = -1
running = False

while True:
    ### Heart Rate
    activity_request = requests.get('https://api.fitbit.com/1/user/'+user_id+'/activities/heart/date/today/1d/1min.json', 
    headers={'Authorization': 'Bearer ' + access_token})
    # heartRate = activity_request.json()['activities-heart-intraday']['dataset'][-1]['value']
    # print(activity_request.json()['activities-heart-intraday']['dataset'][-1]['value'])

    ### Walk
    activity_request = requests.get('https://api.fitbit.com/1/user/'+user_id+'/activities/distance/date/today/1d.json',
    headers={'Authorization': 'Bearer ' + access_token})
    l = activity_request.json()['activities-distance-intraday']['dataset'][-1]['value']
    sl = activity_request.json()['activities-distance-intraday']['dataset'][-10]['value']

    print(l)


    ### Sleep
    activity_request= requests.get('https://api.fitbit.com/1/user/'+user_id+'/sleep/date/today.json',
    headers={'Authorization': 'Bearer ' + access_token})
    sleepEfficiency = activity_request.json()['sleep']['efficiency']

    ## Testing
    heartRate = 10
    # l = 400
    # sl = 50

    # if l - sl > 300:
    #     running = True

    print("Heart Rate: " + str(heartRate) + "\tMood: ", end="")
    if heartRate>0 and heartRate<60:
        mood = 1
        print("Energetic")    
    elif heartRate>60 and heartRate<100:
        mood = 0
        print("Normal")
    else:
        mood = 2
        print("Calm")   

    

    
# https://open.spotify.com/playlist/3EWU8qJI98pa4rCOuatMoE?si=0sY8yQTJQbajX1ypOqNSyg&utm_source=native-share-menu
# https://open.spotify.com/playlist/4EzpYy3zyvefGdwj3rUgCZ?si=IvnDB-IzQdObkrud6kVB9A&utm_source=whatsapp

# https://open.spotify.com/playlist/2tLMUKxKJXjYV79iPhQzon?si=GBHiOISiSDmn6lXgGfa4Ww&utm_source=whatsapp

    # if prevMood != mood:

    #     playlist_creator = "Dimish"
    #     playlist_id = "2tLMUKxKJXjYV79iPhQzon"

    #     playlist_df = getRecommendations(playlist_creator, playlist_id)

    #     recommended_df = playlist_df[playlist_df['mood']==mood]
    #     print(recommended_df)
    #     prevMood = mood

    time.sleep(60)