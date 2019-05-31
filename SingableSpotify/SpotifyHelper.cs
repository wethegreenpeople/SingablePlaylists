using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using SpotifyAPI.Web; //Base Namespace
using SpotifyAPI.Web.Auth; //All Authentication-related classes
using SpotifyAPI.Web.Enums; //Enums
using SpotifyAPI.Web.Models; //Models for the JSON-responses

namespace SingableSpotify
{
    public class SpotifyHelper
    {
        private readonly SpotifyWebAPI _spotify;
        private readonly Random _rand = new Random();

        public SpotifyHelper()
        {
            ImplicitGrantAuth auth =
        new ImplicitGrantAuth("6333b8e3c6de47cdadcd860e8d9a881c", "http://localhost", "http://localhost", Scope.UserReadPrivate);
            auth.AuthReceived += (sender, payload) =>
            {
                auth.Stop(); // `sender` is also the auth instance
                SpotifyWebAPI api = new SpotifyWebAPI() { TokenType = payload.TokenType, AccessToken = payload.AccessToken };
                // Do requests with API client
            };
            auth.Start(); // Starts an internal HTTP Server
            auth.OpenBrowser();
            _spotify = new SpotifyWebAPI()
            {
                UseAuth = true,
            };
        }

        public FullTrack GetRandomTrack()
        {
            var doot = _spotify.GetSavedTracks(1, _rand.Next(0, 1285)).Items;
            return doot.First().Track;
        }
    }
}
