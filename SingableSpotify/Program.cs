﻿using System;
using System.IO;
using Microsoft.ML;
using SingableSpotifyML.Model.DataModels;
using System.Collections.Generic;
using SpotifyAPI.Web.Auth;
using SpotifyAPI.Web.Enums;
using SpotifyAPI.Web; //Base Namespace
using SpotifyAPI.Web.Auth; //All Authentication-related classes
using SpotifyAPI.Web.Enums; //Enums
using SpotifyAPI.Web.Models; //Models for the JSON-responses
using System.Linq;

namespace SingableSpotify
{
    class Program
    {
        static void Main(string[] args)
        {
            // Load the model
            MLContext mlContext = new MLContext();
            ITransformer mlModel = mlContext.Model.Load("MLModel.zip", out var modelInputSchema);
            var predEngine = mlContext.Model.CreatePredictionEngine<ModelInput, ModelOutput>(mlModel);
            var singableSongs = new List<string>();
            var rand = new Random();

            ImplicitGrantAuth auth = new ImplicitGrantAuth("6333b8e3c6de47cdadcd860e8d9a881c", "http://localhost:4002", "http://localhost:4002", Scope.UserReadPrivate)
            {
                ShowDialog = true,
            };
            
            auth.AuthReceived += (sender, payload) =>
            {
                auth.Stop();
                SpotifyWebAPI api = new SpotifyWebAPI() { TokenType = payload.TokenType, AccessToken = payload.AccessToken };

                var savedTracks = api.GetSavedTracks(50, rand.Next(0, 1285)).Items;
                var tracksAudioFeatures = api.GetSeveralAudioFeatures(savedTracks.Select(s => s.Track.Id).ToList()).AudioFeatures;
                for (int i = 0; i < savedTracks.Count; ++i)
                {
                    var track = savedTracks[i].Track;
                    var trackAnalysis = tracksAudioFeatures[i];

                    if (track.Id == trackAnalysis.Id)
                    {
                        var input = new ModelInput()
                        {
                            Name = track.Name,
                            Duration = track.DurationMs,
                            Popularity = track.Popularity,
                            Key = trackAnalysis.Key,
                            TimeSig = trackAnalysis.TimeSignature,
                            Energy = trackAnalysis.Energy,
                            Instrumentalness = trackAnalysis.Instrumentalness,
                            Loudness = trackAnalysis.Loudness,
                            Tempo = trackAnalysis.Tempo,
                            LyricSimplicity = 0,
                            Sections = api.GetAudioAnalysis(track.Id).Sections.Count,
                        };

                        // Try model on sample data
                        ModelOutput result = predEngine.Predict(input);

                        if (result.Score[1] > .9) { singableSongs.Add(input.Name); }
                    }
                }

                foreach (var song in singableSongs)
                {
                    Console.WriteLine(song);
                }
            };

            auth.Start(); // Starts an internal HTTP Server
            auth.OpenBrowser();

            Console.ReadKey();
        }
    }
}