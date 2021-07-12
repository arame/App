import os, re
from csv import DictWriter
from config import Hyper
import ftfy
from data_cleaner import DataCleaner
from tweet_translator import TweetTranslator
from user_location import UserLocation
from country import Country

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
            if len(language) == 0 or language == "und":
                self.no_language_cnt += 1
                continue

            #ignore retweets
            
            if 'retweeted_status' in tweet:
                continue            

            self.change_working_directory(language)
            country = self.get_country_from_place(tweet)
            if len(country) > 0:
                c = Country()
                c.save(country)
                self.change_working_directory(country)
                self.output_file(tweet)
                self.tweet_saved_cnt += 1
                continue

            # This code slows the execution of this data load
            # Instead of running this code here, use a seperate process
            if Hyper.UseUserLocation:
                _, country = self.get_user_location(tweet)
                if country == None:
                    continue

                if len(country) > 0:
                    self.change_working_directory(country)
                    self.output_file(tweet)
                    self.tweet_saved_cnt += 1
                    continue
   
            user_location, _ = self.get_user_location(tweet)
            if len(user_location) > 0:
                self.change_working_directory("no_country")
                self.output_file(tweet)
                self.tweet_saved_cnt += 1
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
            return "", ""

        country = ""
        user_location = self.get_string_json_data(user, "location")
        if user_location == None or len(user_location) == 0:
            return "", ""

        user_location = DataCleaner.remove_noise(user_location)
        country = ""
        if Hyper.UseUserLocation:
            ul = UserLocation()
            country = ul.locator(user_location)

        return user_location, country

    def get_country_from_place(self, tweet):
        place = tweet["place"]
        if place == None or len(place) == 0:
            return ""

        country = self.get_string_json_data(place, "country")
        if country == None or len(country) == 0:
            return ""

        return country

    # Helper method to get the string from the JSON data
    def get_string_json_data(self, json, property):
        if property not in json:
            print(f"!! object {property} not in json {json}")
            return ""

        if json[property] == None:
            return ""

        return ftfy.fix_text(json[property])    # ftfy library ensures the encoding works, see https://ftfy.readthedocs.io/en/latest/

    def output_file(self, tweet):
        id = tweet["id"]
        language = self.get_string_json_data(tweet, "lang")
        place = self.get_string_json_data(tweet, "place")
        country = self.get_country_from_place(tweet)
        user_location, _ = self.get_user_location(tweet) 
        """ if len(country) == 0:
            country = user_country """

        full_text = self.get_string_json_data(tweet, "full_text")
        full_text_edit = DataCleaner.lowercase_text(full_text)
        full_text_edit = DataCleaner.remove_noise(full_text_edit)
        full_text_en = ""
        if language == "en":
            full_text_en = full_text_edit
        
        # Remove tweet translations from here. The process is too unreliable and should be run seperately
        """ else:
            full_text_en = TweetTranslator.to_english(full_text, language) """

        retweet_count = tweet["retweet_count"]
        favorite_count = tweet["favorite_count"]
        row = {'Id':id, 'Language': language, 'Place': place, 'User Location': user_location, 'Country': country, 'Full Text': full_text, 'Tweet': full_text_edit, 'English Tweet': full_text_en, 'Retweet Count': retweet_count, 'Favourite Count': favorite_count}
        self.append_dict_as_row(row)

    def append_dict_as_row(self, row):
        output_file = Hyper.HyrdatedTweetFile
        if os.path.exists(output_file):
            # Open file in append mode
            with open(output_file, 'a+', encoding="utf-8", newline='') as write_obj:
                dict_writer = DictWriter(write_obj, fieldnames=Hyper.field_names)
                dict_writer.writerow(row)
                return

        with open(output_file, 'w', encoding="utf-8", newline='') as write_obj:
            dict_writer = DictWriter(write_obj, fieldnames=Hyper.field_names)
            dict_writer.writeheader()
            dict_writer.writerow(row)
