import os, re
from csv import DictWriter
from config import Hyper

class HydratedTweets:
    def __init__(self, hydrated_tweets):
        self.hydrated_tweets = hydrated_tweets
        self.no_language_cnt = 0
        self.tweet_saved_cnt = 0

    def output_to_csv(self):
        directory_path = os.getcwd()
        for tweet in self.hydrated_tweets:
            os.chdir(directory_path)
            language = tweet["lang"]
            if len(language) == 0:
                self.no_language_cnt += 1
                continue

            #ignore retweets
            
            if 'retweeted_status' in tweet:
                continue            

            self.change_working_directory(language)
            country = self.get_country(tweet)
            if len(country) > 0:
                self.change_working_directory("country")
                self.change_working_directory(country)
                self.output_file(tweet)
                self.tweet_saved_cnt += 1
                continue

            if Hyper.UseUserLocation:
                user_location = self.get_user_location(tweet)
                if len(user_location) > 0:
                    self.change_working_directory("user")
                    self.change_working_directory(user_location)
                    self.output_file(tweet)
                    continue
   
        # Return to root directory
        os.chdir(directory_path) 
        Hyper.no_language_cnt += self.no_language_cnt
        Hyper.tweet_saved_cnt += self.tweet_saved_cnt   
            
    def change_working_directory(self, folder):
        # Replace invalid characters for folder name with underbar.
        folder = re.sub('[^\w_.)( -]', '_', folder)
        if not os.path.exists(folder):
            os.makedirs(folder)

        os.chdir(folder)

    def get_user_location(self, tweet):
        user = tweet["user"]
        if user == None or len(user) == 0:
            return ""

        user_location = user["location"]
        if user_location == None or len(user_location) == 0:
            return ""

        user_location = user_location.replace(" ", "").replace(",", "_")
        return user_location

    def get_country(self, tweet):
        place = tweet["place"]
        if place == None or len(place) == 0:
            return ""

        country = place["country"]
        if country == None or len(country) == 0:
            return ""

        return country

    def output_file(self, tweet):
        field_names = ['Id', 'Language', 'User Location', 'Country', 'Full Text', 'Retweet Count', 'Favourite Count']
        id = tweet["id"]
        language = tweet["lang"]
        user_location = self.get_user_location(tweet) 
        country = self.get_country(tweet)              
        full_text = tweet["full_text"]
        retweet_count = tweet["retweet_count"]
        favorite_count = tweet["favorite_count"]
        row = {'Id':id, 'Language': language, 'User Location': user_location, 'Country': country, 'Full Text': full_text, 'Retweet Count': retweet_count, 'Favourite Count': favorite_count}
        self.append_dict_as_row(row, field_names)

    def append_dict_as_row(self, row, field_names):
        output_file = "tweets.csv"
        if os.path.exists(output_file):
            # Open file in append mode
            with open(output_file, 'a+', encoding="utf-8", newline='') as write_obj:
                dict_writer = DictWriter(write_obj, fieldnames=field_names)
                dict_writer.writerow(row)
                return

        with open(output_file, 'w', encoding="utf-8", newline='') as write_obj:
            dict_writer = DictWriter(write_obj, fieldnames=field_names)
            dict_writer.writeheader()
            dict_writer.writerow(row)
