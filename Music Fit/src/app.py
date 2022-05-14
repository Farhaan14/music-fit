from flask import Flask, render_template, request, redirect, url_for
from fitbit import *
import pandas as pd

from songId import *

app = Flask(__name__)

@app.route('/song', methods=['POST'])
def song():
    output = request.get_json()
    result = json.loads(output)
    songId = getSongId(result['songName'])
    return songId

@app.route('/')
def hello_world():
    data = pd.DataFrame()
    prevMood = -1
    running = pd.DataFrame()
    prevRunning = -1
    restless = pd.DataFrame()
    prevRestless = -1
    i = 0
    while i < 5:
        data, prevMood, running, prevRunning, restless, prevRestless, heartRate, distance, sleepEfficiency = fitbitAndMusicRecommendation(data, prevMood, running, prevRunning, restless, prevRestless)
        time.sleep(5)
        i += 1

    values = data.values.tolist()[:5]
    running = running.values.tolist()[:5]
    restless = restless.values.tolist()[:5]
 
    
    if prevMood == 0:
        stateHeart = "Normal"
    elif prevMood == 1:
        stateHeart = "Calm"
    else:
        stateHeart = "Energetic"

    if prevRunning == 0:
        stateRunning = "Sedentary"
    else:
        stateRunning = "Active"

    if prevRestless == 0:
        stateRestless = "Effective"
    else:
        stateRestless = "Restless"

    distance = round(distance / 60, 2)

    return render_template('index.html', values = values, running = running, restless = restless, heartRate = heartRate, distance = distance, sleepEfficiency = sleepEfficiency, stateHeart = stateHeart, stateRunning = stateRunning, stateRestless = stateRestless)

if __name__ == '__main__':
	app.run(debug=True)
