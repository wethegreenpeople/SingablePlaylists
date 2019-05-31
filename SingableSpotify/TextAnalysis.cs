using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SingableSpotify
{
    public class TextAnalysis
    {
        public TextAnalysis()
        {

        }

        public int FleschReadingEase(string text)
        {
            return 0;
        }

        private int WordCount(string text)
        {
            return text.Split(' ').Length;
        }

        private int SentenceCount(string text)
        {
            return text.Split('.', '?', '!', ';').Length;
        }

        private int SyllableCount(string text)
        {
            text = text.ToLower();
            var vowels = new[] { 'a', 'e', 'i', 'o', 'u', 'y' };
            int syllableCount = 0;
            bool wasPreviousCharacterVowel = false;

            foreach (var word in text.Split(' '))
            {
                foreach (var character in text)
                {
                    if (vowels.Contains(character))
                    {
                        if (!wasPreviousCharacterVowel) { ++syllableCount; }
                        wasPreviousCharacterVowel = true;
                    }
                    else
                    {
                        wasPreviousCharacterVowel = false;
                    }
                }

                if ((word.EndsWith("e") || (word.EndsWith("es") || word.EndsWith("ed")))
                      && !word.EndsWith("le"))
                    syllableCount--;
            }
        }
    }
}
