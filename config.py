import os
class Hyper:
    UseUserLocation = False
    MustTranslate = False
    WordcloudDir = "D:/363/wordcloud"
    UserLocationFile = "D:/363/Lookup/UserLocations.csv"
    HyrdatedTweetDirNoCountry = "D:/363/Summary_Details_files11/en/no_country"
    HyrdatedTweetLangEnDir = "D:/363/Summary_Details_files11/en"
    HyrdatedTweetDir = "D:/363/Summary_Details_files11"
    HyrdatedTweetFile = "tweets.csv"
    no_language_cnt = 0
    tweet_saved_cnt = 0
    # Keys, access tokens and secrets taken from Twitter are stored as environment variables
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    field_names = ['Id', 'Language', 'User Location', 'Country', 'Tweet', 'English Tweet', 'Retweet Count', 'Favourite Count']

    def __init__(self) -> None:
        self.dirOutput =  "../Summary_Details_files11"
        self.IsOutputCsv = True
        #@title Enter range of dates to Hydrate { run: "auto" }
        self.start_date = '2020-03-22' #@param {type:"date"}
        self.end_date = '2020-03-24' #@param {type:"date"}
        #@title Check Keywords to Hydrate { run: "auto" }
        coronavirus = True #@param {type:"boolean"}
        virus = False #@param {type:"boolean"}
        covid = True #@param {type:"boolean"}
        ncov19 = False #@param {type:"boolean"}
        ncov2019 = False #@param {type:"boolean"}
        self.keyword_dict = {"coronavirus": coronavirus, "virus": virus, "covid": covid, "ncov19": ncov19, "ncov2019": ncov2019}
        self.covid_loc = "../COVID19_Tweets_Dataset"
 