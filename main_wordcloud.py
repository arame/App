import numpy as np
import pandas as pd
import os
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from config import Hyper
import time

# See https://www.datacamp.com/community/tutorials/wordcloud-python
def main():
    print(f"{get_time()}     Start wordcount")
    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(["coronavirus", "covid", "time", "today", "know", "support", "update", "say", "take", "please", "need", "well", "think", "virus", "thank", "read", "new", "going", "read", "help", "people", "let", "will", "one", "said", "due", "see", "day", "via", "make", "call", "really", "every", "great", "still", "keep", "now", "im", "case", "patient", "everyone", "many", "corona", "says", "go", "even", "week", "dont", "outbreak", "first", "cant", "way", "good", "work", "spread", "live", "right", "come", "back", "news", "stop", "number", "want", "may", "home", "country", "hope", "got", "US", "pandemic", "crisis", "cases", "stay", "thing", "amid", "look"])
    dirs = os.listdir(Hyper.HyrdatedTweetLangEnDir)
    for countrydir in dirs:
        countryfile = path.join(Hyper.HyrdatedTweetLangEnDir, countrydir, Hyper.HyrdatedTweetFile)
        file_size = os.path.getsize(countryfile)
        if file_size < 100000:
            continue

        print (f"{get_time()}     Generate wordcloud for country {countrydir}")
        filename = f"wordcloud_{countrydir}.png"
        wordcloudfig = path.join(Hyper.WordcloudDir, filename)
        output_wordcloud(countryfile, wordcloudfig, stopwords)
        print(f"{get_time()}     Wordcloud output for country {countrydir}")
    
    print("The End")

def output_wordcloud(countryfile, wordcloudfig, stopwords):
    #file = path.join(Hyper.HyrdatedTweetDirNoCountry, Hyper.HyrdatedTweetFile)
    df = pd.read_csv(countryfile, index_col=0)
    print(df.head())
    text_arr = df["Tweet"].values
    text = ""
    for txt in text_arr:
        if type(txt) == str:
            text = " ".join([text, txt])
    print (f"{get_time()}     There are {len(text)} words used in the selected tweets")
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(wordcloudfig)
    

def get_time():
    return time.strftime('%Y/%m/%d %H:%M:%S')

if __name__ == "__main__":
    main()