import os
import time
class Hyper:
    UseUserLocation = False
    MustTranslate = False
    time = time.strftime('%Y_%m_%d %H_%M_%S')
    version = 15
    language = "en"
    WordcloudDir = "../wordcloud"
    UserLocationFile = "../../Lookup/UserLocations.csv"
    HyrdatedTweetDirNoCountry = f"../Summary_Details_files{time}/{language}/no_country"
    HyrdatedTweetLangDir = f"../Summary_Details_files{time}/{language}"
    HyrdatedTweetDir = f"../Summary_Details_files{time}"
    HyrdatedTweetFile = "tweets.csv"
    no_language_cnt = 0
    tweet_saved_cnt = 0
    # Keys, access tokens and secrets taken from Twitter are stored as environment variables
    consumer_key = 'JLuZDxu7NcuPnTno0qgztrsoZ'
    consumer_secret = 'KL16xLRhvErmrMPOUvex3KbiGk3Ao9e0ziGhaDNq1y4tNuI9uW'
    access_token = '1253768165923880961-Yhct3tMh9LYpdrFkazJl1KqvDzOTg2'
    access_token_secret = 'QpQykkfzvnVKg5pVyP0Kf3V1ZPAR30617XfoN3o43fDMu'
    field_names = ['Id', 'Language', 'Place', 'User Location', 'Country', 'Full Text', 'Tweet', 'English Tweet', 'Retweet Count', 'Favourite Count']
    
    def __init__(self) -> None:
        self.dirOutput =  f"../Summary_Details_files{Hyper.time}"
        self.IsOutputCsv = True
        #@title Enter range of dates to Hydrate { run: "auto" }
        self.start_date = '2020-03-22' #@param {type:"date"}
        self.end_date = '2020-03-24' #@param {type:"date"}
        #@title Check Keywords to Hydrate { run: "auto" }
        coronavirus = True #@param {type:"boolean"}
        virus = False #@param {type:"boolean"}
        covid = True #@param {type:"boolean"}
        ncov19 = True #@param {type:"boolean"}
        ncov2019 = True #@param {type:"boolean"}
        self.keyword_dict = {"coronavirus": coronavirus, "virus": virus, "covid": covid, "ncov19": ncov19, "ncov2019": ncov2019}
        self.covid_loc = "../COVID19_Tweets_Dataset"
 