import os, re
import time
class Hyper:
    UseUserLocation = False
    MustTranslate = False
    time = time.strftime('%Y_%m_%d %H_%M_%S')
    version = 15
    language = "en"
    WordcloudDir = "D:/363/wordcloud"
    UserLocationFile = "D:/363/Lookup/UserLocations.csv"
    HyrdatedTweetDirNoCountry = f"D:/363/Summary_Details_files{time}/{language}/no_country"
    HyrdatedTweetLangDir = f"D:/363/Summary_Details_files{time}/{language}"
    HyrdatedTweetDir = f"D:/363/Summary_Details_files{time}"
    HyrdatedTweetFile = "tweets.csv"
    HyrdatedTweetLangFile = f"{language}_tweets.csv"
    no_language_cnt = 0
    tweet_saved_cnt = 0
    # Keys, access tokens and secrets taken from Twitter are stored as environment variables
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET'] 
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    field_names = ['Id', 'Language', 'Place', 'User Location', 'Country', 'Full Text', 'clean_text', 'Retweet Count', 'Favourite Count']
    no_retweets = True                 #@param {type:"boolean"}
    covid_2021_loc = "../COVID19_2021_Tweets_Dataset"
    
    def __init__(self) -> None:
        self.dirOutput =  f"../Summary_Details_files{Hyper.time}"
        self.IsOutputCsv = True
        # self.start_date = '2020-03-16' #@param {type:"date"}
        # self.end_date = '2020-03-18' #@param {type:"date"} 
        #@title Enter range of dates to Hydrate { run: "auto" }
        self.start_date = '2021-04-04' #@param {type:"date"}
        self.end_date = '2021-04-08' #@param {type:"date"}
        #@title Check Keywords to Hydrate { run: "auto" }
        coronavirus = True #@param {type:"boolean"}
        virus = False #@param {type:"boolean"}
        covid = True #@param {type:"boolean"}
        ncov19 = True #@param {type:"boolean"}
        ncov2019 = True #@param {type:"boolean"}
        self.keyword_dict = {"coronavirus": coronavirus, "virus": virus, "covid": covid, "ncov19": ncov19, "ncov2019": ncov2019}
        self.covid_loc = "../COVID19_Tweets_Dataset"
        
 
class Constants:
    USER_HANDLES_REGEX = re.compile(r"@\S+")
    NEW_LINE_REGEX = re.compile(r'\s+|\\n')