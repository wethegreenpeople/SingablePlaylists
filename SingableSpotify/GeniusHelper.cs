using Genius;
using HtmlAgilityPack;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SingableSpotify
{
    public class GeniusHelper
    {
        public GeniusHelper()
        {

        }

        public string GetLyrics(string artist, string songTitle)
        {
            artist = artist.ToLower();
            songTitle = songTitle.ToLower();

            var geniusClient = new GeniusClient("kagwNkaoSmy_bt0asl8IZedmPZY-E9nW88K5NgbyyV3C2y1YruRMsETwsQtI8850");
            var searchResults = geniusClient.SearchClient.Search(Genius.Models.TextFormat.Plain, $"{songTitle} by {artist}").Result.Response;
            GeniusSong song = new GeniusSong();
            try
            {
                var gsong = JsonConvert.DeserializeObject<GeniusSong>(searchResults.First().Result.ToString());
                var web = new HtmlWeb();
                var doc = web.Load(gsong.Url);
                var lyrics = doc.DocumentNode.SelectSingleNode(@"//div[@class='lyrics']");

                return lyrics.InnerText.Trim();
            }
            catch (InvalidOperationException)
            {
                return string.Empty;
            }
        }
    }
}
