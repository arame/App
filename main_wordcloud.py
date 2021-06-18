import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from config import Hyper

# See https://www.datacamp.com/community/tutorials/wordcloud-python
def main():
    print("start wordcount")
    
    file = path.join(Hyper.HyrdatedTweetDir, Hyper.HyrdatedTweetFile)
    df = pd.read_csv(file, index_col=0)
    print(df.head())
    text_arr = df["Tweet"].values
    text = ""
    for txt in text_arr:
        if type(txt) == str:
            text = " ".join([text, txt])
    print (f"There are {len(text)} words used in the selected tweets")
    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(["coronavirus", "covid", "time", "today", "know", "support", "update", "say", "take", "please", "need", "well", "think", "virus", "thank", "read", "new", "going", "read", "help", "people", "let", "will", "one", "said", "due", "see", "day", "via", "make", "call", "really", "every", "great", "still", "keep", "now", "im", "case", "patient", "everyone", "many", "corona", "says", "go", "even", "week", "dont", "outbreak", "first", "cant", "way", "good", "work", "spread", "live", "right", "come", "back", "news", "stop", "number", "want", "may", "home", "country", "hope", "got", "US", "pandemic", "crisis", "cases", "stay", "thing", "amid", "look"])
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloud.png')
    print("The End")

if __name__ == "__main__":
    main()