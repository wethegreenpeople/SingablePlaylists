import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import tree
from sklearn import preprocessing
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import neighbors
from sklearn import neural_network
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
import spotipy
import spotipy.util as util
import random
import csv
import private
import lyricsgenius
import textstat
import graphviz

def Train():
    columnNames = ['Name', 'Duration', 'Popularity', 'Key', 'Time Sig', 'Energy', 'Instrumentalness', 'Loudness', 'Tempo', 'LyricSimplicity', 'Singable']
    songs = pd.read_csv(r"Resources\TrainingData.csv")
    trainingDataframe = DataFrame(songs, columns=columnNames)
    #scatterPlot(trainingDataframe)

    X = trainingDataframe[['Duration', 'Popularity', 'Key', 'Energy', 'Instrumentalness', 'Loudness', 'Tempo', 'LyricSimplicity']]
    Y = trainingDataframe['Singable']

    regression = RandomForestRegressor(n_estimators=400, max_features=8, max_depth=None, min_samples_split=2)
    regression = regression.fit(X,Y)
    return regression

def Predict(regression):
    scope = 'user-library-read playlist-modify-public'
    token = util.prompt_for_user_token(private.spotifyUsername, scope, private.spotifyClientId, private.spotifyClientSecret, "http://localhost")
    spot = spotipy.Spotify(auth=token)

    if token:
        songUris = []
        playlist = spot.user_playlist_create(private.spotifyUserId, "Singable")
        while len(songUris) < 10:
            track = spot.current_user_saved_tracks(1, random.randint(0, 1268))
            song = track['items'][0]['track']
            
            # Don't want duplicate songs in this playlist
            if (song["uri"] not in songUris):
                trackAnalysis = spot.audio_features(song["uri"])[0]
                name = song["name"]
                artist = song["artists"][0]["name"]
                print(name)
                simplicity = LyricDifficulty(GetLyrics(name, artist))
                duration = song["duration_ms"]
                popularity = song["popularity"]
                key = trackAnalysis["key"]
                energy = trackAnalysis["energy"]
                instrumentalness = trackAnalysis["instrumentalness"]
                loudness = trackAnalysis["loudness"]
                tempo = trackAnalysis["tempo"]

                prediction = regression.predict([[duration, popularity, key, energy, instrumentalness, loudness, tempo, simplicity]])
                # Checking for prediction confidence. > 60% and we'll add it to the playlist 
                if (float(prediction[0]) > 0.60):
                    songUris.append(song["uri"])
                print(name + " Prediction: " + str(prediction))
        spot.user_playlist_add_tracks(private.spotifyUserId, playlist["id"], songUris)

def scatterPlot(dataFrame):
    plt.scatter(dataFrame['Simplicity'], dataFrame['Singable'], color='red')
    plt.title("Simple VS Singable", fontsize=14)
    plt.xlabel("Simple", fontsize=14)
    plt.ylabel("Singable")
    plt.grid(True)
    plt.show()

def ScrapeSongs():
    scope = 'user-library-read'
    token = util.prompt_for_user_token(private.spotifyUsername, scope, private.spotifyClientId, private.spotifyClientSecret, "http://localhost")

    if token:
        spot = spotipy.Spotify(auth=token)
        
        songUris = []
        # We're grabbing 50 songs total, in batches of 5
        for i in range(0, 10):
            results = spot.current_user_saved_tracks(5, random.randint(0, 1268)) # 1268 is the total amount of songs I have, need to find a way to get this number dynamically

            for item in results['items']:
                if (item["track"]["uri"] not in songUris):
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
                trackInfo.append(LyricDifficulty(GetLyrics(tracks[i]["name"], tracks[i]["artists"][0]["name"])))
                writer = csv.writer(file, delimiter=",")
                writer.writerow(trackInfo)

def GetLyrics(songName, songArtist):
    try:
        genius = lyricsgenius.Genius(private.geniusAccessToken)
        song = genius.search_song(songName, songArtist)
        if (song is not None):
            return song.lyrics
        return None
    except:
        return None

def LyricDifficulty(lyrics):
    if (lyrics is not None):
        return textstat.flesch_reading_ease(lyrics)
    return 0


regression = Train()
Predict(regression)
#ScrapeSongs()
#print(LyricDifficulty(GetLyrics("Hunter", "Tonedeff")))