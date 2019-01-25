import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn import linear_model
import statsmodels.api as sm
import spotipy
import spotipy.util as util
import random
import csv
import private

def Train():
    columnNames = ['Name', 'Duration', 'Popularity', 'Key', 'Time Sig', 'Energy', 'Instrumentalness', 'Loudness', 'Tempo', 'Singable']
    songs = pd.read_csv(r"Resources\TrainingData.csv")
    trainingDataframe = DataFrame(songs, columns=columnNames)

    X = trainingDataframe[['Duration', 'Popularity', 'Key', 'Energy', 'Instrumentalness', 'Loudness', 'Tempo' ]]
    Y = trainingDataframe['Singable']

    regression = linear_model.LinearRegression()
    return regression.fit(X,Y)

def Predict(regression):
    scope = 'user-library-read playlist-modify-public'
    token = util.prompt_for_user_token(private.spotifyUsername, scope, private.spotifyClientId, private.spotifyClientSecret, "http://localhost")
    spot = spotipy.Spotify(auth=token)

    if token:
        songUris = []
        playlist = spot.user_playlist_create(private.spotifyUserId, "Singable")
        while len(songUris) < 11:
            track = spot.current_user_saved_tracks(1, random.randint(0, 1268))
            song = track['items'][0]['track']

            trackAnalysis = spot.audio_features(song["uri"])[0]
            name = song["name"]
            print(name)
            duration = song["duration_ms"]
            popularity = song["popularity"]
            key = trackAnalysis["key"]
            energy = trackAnalysis["energy"]
            instrumentalness = trackAnalysis["instrumentalness"]
            loudness = trackAnalysis["loudness"]
            tempo = trackAnalysis["tempo"]

            prediction = regression.predict([[duration, popularity, key, energy, instrumentalness, loudness, tempo]])
            if (float(prediction[0]) > 0.60):
                print(name + " Prediction: " + str(prediction))
                songUris.append(song["uri"])
        spot.user_playlist_add_tracks(private.spotifyUserId, playlist["id"], songUris)

def scatterPlot(dataFrame):
    plt.scatter(dataFrame['Popularity'], dataFrame['Singable'], color='red')
    plt.title("Singable Rating VS. Song Popularity", fontsize=14)
    plt.xlabel("Popularity", fontsize=14)
    plt.ylabel("Singable")
    plt.grid(True)
    plt.show()

    plt.scatter(dataFrame['Energy'], dataFrame['Singable'], color='green')
    plt.title("Singable Rating VS. Song Energy", fontsize=14)
    plt.xlabel("Energy", fontsize=14)
    plt.ylabel("Singable")
    plt.grid(True)
    plt.show()

def ScrapeSongs():
    scope = 'user-library-read'
    token = util.prompt_for_user_token(private.spotifyUsername, scope, private.spotifyClientId, private.spotifyClientSecret, "http://localhost")

    if token:
        spot = spotipy.Spotify(auth=token)
        
        songUris = []
        for i in range(0, 5):
            results = spot.current_user_saved_tracks(10, random.randint(0, 1268))

            for item in results['items']:
                songUris.append(item['track']['uri'])
        print(len(songUris))

        tracks = spot.tracks(songUris)['tracks']
        trackAnalysis = spot.audio_features(songUris)
        with open("TrainingData.csv", "w+", newline='') as file:
            for i in range(0, len(tracks)):
                trackInfo = []
                trackInfo.append(tracks[i]["name"])
                trackInfo.append(tracks[i]["duration_ms"])
                trackInfo.append(tracks[i]["popularity"])
                trackInfo.append(trackAnalysis[i]["key"])
                trackInfo.append(trackAnalysis[i]["time_signature"])
                trackInfo.append(trackAnalysis[i]["energy"])
                trackInfo.append(trackAnalysis[i]["instrumentalness"])
                trackInfo.append(trackAnalysis[i]["loudness"])
                trackInfo.append(trackAnalysis[i]["tempo"])
                writer = csv.writer(file, delimiter=",")
                writer.writerow(trackInfo)

regression = Train()
Predict(regression)

