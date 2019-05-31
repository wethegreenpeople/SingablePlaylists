//*****************************************************************************************
//*                                                                                       *
//* This is an auto-generated file by Microsoft ML.NET CLI (Command-Line Interface) tool. *
//*                                                                                       *
//*****************************************************************************************

using Microsoft.ML.Data;

namespace SingableSpotifyML.Model.DataModels
{
    public class ModelInput
    {
        [ColumnName("Name"), LoadColumn(0)]
        public string Name { get; set; }


        [ColumnName("Duration"), LoadColumn(1)]
        public float Duration { get; set; }


        [ColumnName("Popularity"), LoadColumn(2)]
        public float Popularity { get; set; }


        [ColumnName("Key"), LoadColumn(3)]
        public float Key { get; set; }


        [ColumnName("TimeSig"), LoadColumn(4)]
        public float TimeSig { get; set; }


        [ColumnName("Energy"), LoadColumn(5)]
        public float Energy { get; set; }


        [ColumnName("Instrumentalness"), LoadColumn(6)]
        public float Instrumentalness { get; set; }


        [ColumnName("Loudness"), LoadColumn(7)]
        public float Loudness { get; set; }


        [ColumnName("Tempo"), LoadColumn(8)]
        public float Tempo { get; set; }


        [ColumnName("LyricSimplicity"), LoadColumn(9)]
        public float LyricSimplicity { get; set; }


        [ColumnName("Sections"), LoadColumn(10)]
        public float Sections { get; set; }


        [ColumnName("Singable"), LoadColumn(11)]
        public bool Singable { get; set; }


    }
}
