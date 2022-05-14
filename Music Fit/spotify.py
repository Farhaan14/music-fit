import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import numpy as np
import joblib

auth_manager = SpotifyClientCredentials(
    client_id = 'f6343bebebba4e3a84520d2cb79a53e8',
    client_secret = 'ad836bec7b934b94b0b298e70f7f9ec0'
    )

sp = spotipy.Spotify(auth_manager=auth_manager)
# artist_info = 'spotify:artist:2eam0iDomRHGBypaDQLwWI'

# artist = sp.artist(artist_info)
# print(artist)

# https://open.spotify.com/playlist/4EzpYy3zyvefGdwj3rUgCZ?si=IvnDB-IzQdObkrud6kVB9A&utm_source=whatsapp



playlist_creator = "Varan"
playlist_id = "4EzpYy3zyvefGdwj3rUgCZ"

def analyze_playlist(creator, playlist_id):
    
    # Create empty dataframe
    playlist_features_list = ["artist", "album", "track_name", "track_id", 
                             "danceability", "energy", "key", "loudness", "mode", "speechiness","acousticness",
                             "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    # Create empty dict
    playlist_features = {}
    
    # Loop through every track in the playlist, extract features and append the features to the playlist df
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]

    for track in playlist:
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
       
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df

def get_track_features(id):
    meta = sp.track(id)
    # meta

    album_cover = meta['album']['images'][0]['url']
    track_info = [album_cover]
    return track_info

playlist_df = analyze_playlist(playlist_creator, playlist_id)

track_id=[]
# county=0
for i in range(len(playlist_df)) :
  track_id.append(playlist_df.iloc[i, 3])

track_img=[]
for i in range(len(track_id)) :
  track_img.append(get_track_features(track_id[i]))

df2=pd.DataFrame(track_img)
df2.columns=['image']

playlist_df = playlist_df.join(df2)

playlist_df=playlist_df.drop(playlist_df.columns[[1, 3, 6, 8, 11, 14, 15, 16]], axis=1)
playlist_df = playlist_df[["artist","track_name","image" ,"energy",	"danceability",	"loudness",	"liveness",	"valence",	"acousticness",	"speechiness"]]

# playlist_df['danceability'] = playlist_df['danceability'].map(lambda a: a * 100)
# playlist_df['energy'] = playlist_df['energy'].map(lambda a: a * 100)
# playlist_df['liveness'] = playlist_df['liveness'].map(lambda a: a * 100)
# playlist_df['valence'] = playlist_df['valence'].map(lambda a: a * 100)
# # playlist_df['duration_ms']=playlist_df['duration_ms'].map(lambda a: a/1000)
# playlist_df['speechiness'] = playlist_df['speechiness'].map(lambda a: a * 100)
# playlist_df['acousticness'] = playlist_df['acousticness'].map(lambda a: a * 100)

playlist_df.danceability=playlist_df.danceability.astype(int)
playlist_df.energy=playlist_df.energy.astype(int)
playlist_df.liveness=playlist_df.liveness.astype(int)
playlist_df.valence=playlist_df.valence.astype(int)
# playlist_df.duration_ms=playlist_df.duration_ms.astype(int)
playlist_df.loudness=playlist_df.loudness.astype(int)
playlist_df.speechiness=playlist_df.speechiness.astype(int)
playlist_df.acousticness=playlist_df.acousticness.astype(int)

arr=playlist_df.iloc[0].to_numpy()
nar=playlist_df.iloc[0].values

joblib_file = "C:/Users/Admin/Desktop/6th Sem/Project/IoT/Music Fit/randomforestmodel.pkl"  
joblib_model = joblib.load(joblib_file)

# tarr=list(arr)
# X_test=[tarr[3:]]
# y_pred = joblib_model.predict(X_test)
# print(y_pred)

final_song=[]
for n in range(len(playlist_df)):
  arr=playlist_df.iloc[n].to_numpy()
  tarr=list(arr)
  X_test=[tarr[3:]]
  y_pred = joblib_model.predict(X_test)
  final_song.append(list(y_pred))

print(final_song)

# songsCalm = []
# songsEnergetic = []
# songsHappy = []
# for i in range(len(final_song)):
#     if final_song[i][0] == 1:
#         songsCalm.append(i)
#     elif final_song[i][1] == 1:
#         songsEnergetic.append(i)
#     else:
#         songsHappy.append(i)

# print(songsCalm)
# print(songsEnergetic)
# print(songsHappy)
