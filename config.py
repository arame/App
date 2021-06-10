
class Hyper:
    UseUserLocation = False
    no_language_cnt = 0
    tweet_saved_cnt = 0

    def __init__(self) -> None:
        self.dirOutput =  "../Summary_Details_files4"
        self.IsOutputCsv = True
        #@title Enter range of dates to Hydrate { run: "auto" }
        self.start_date = '2020-03-22' #@param {type:"date"}
        self.end_date = '2020-03-24' #@param {type:"date"}
        #@title Check Keywords to Hydrate { run: "auto" }
        coronavirus = True #@param {type:"boolean"}
        virus = False #@param {type:"boolean"}
        covid = False #@param {type:"boolean"}
        ncov19 = False #@param {type:"boolean"}
        ncov2019 = False #@param {type:"boolean"}
        self.keyword_dict = {"coronavirus": coronavirus, "virus": virus, "covid": covid, "ncov19": ncov19, "ncov2019": ncov2019}
        self.covid_loc = "../COVID19_Tweets_Dataset"
 