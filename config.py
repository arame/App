
class Hyper:
    UseUserLocation = False
    no_language_cnt = 0
    tweet_saved_cnt = 0
    consumer_key = "JLuZDxu7NcuPnTno0qgztrsoZ"                                  #@param {type:"string"}
    consumer_secret = "KL16xLRhvErmrMPOUvex3KbiGk3Ao9e0ziGhaDNq1y4tNuI9uW"      #@param {type:"string"}
    access_token = "1253768165923880961-Yhct3tMh9LYpdrFkazJl1KqvDzOTg2"         #@param {type:"string"}
    access_token_secret = "QpQykkfzvnVKg5pVyP0Kf3V1ZPAR30617XfoN3o43fDMu"       #@param {type:"string"}

    def __init__(self) -> None:
        self.dirOutput =  "../Summary_Details_files6"
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
 