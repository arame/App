import csv, os
import pandas as pd
from config import Hyper
from user_location import UserLocation
import time

def main():
    #part1()
    part2()

def part1():
    _time = time.strftime('%Y/%m/%d %H:%M:%S')
    print(f"{_time}     ** Started Part 1")
    file = os.path.join(Hyper.HyrdatedTweetDirNoCountry, Hyper.HyrdatedTweetFile)
    i = 0
    ul = UserLocation()
    with open(file, encoding="utf-8", newline='') as csvfile:
        _time = time.strftime('%Y/%m/%d %H:%M:%S')
        print(f"{_time}     {file} opened")
        reader = csv.DictReader(csvfile)
        for row in reader:
            i += 1
            output_row(ul, row)
            if i % 100 == 0:
                _time = time.strftime('%Y/%m/%d %H:%M:%S')
                print(f"{_time}     {i} rows processed")

    _time = time.strftime('%Y/%m/%d %H:%M:%S')
    print(f"{_time}     ** Part 1 Ended")

def part2():
    # Join all the tweet files for each country into one file for the langauage
    _time = time.strftime('%Y/%m/%d %H:%M:%S')
    print(f"{_time}     ** Started Part 2")
    os.chdir(Hyper.HyrdatedTweetLangDir_part2)
    print(f"Changed directory to {Hyper.HyrdatedTweetLangDir_part2}")
    en_tweet_file = 'en_tweets.csv'
    list_dirs = os.listdir()
    big_df = pd.concat( [pd.read_csv(os.path.join(_dir,'tweets.csv')) for _dir in list_dirs]) 
    big_df.to_csv(en_tweet_file)

    _time = time.strftime('%Y/%m/%d %H:%M:%S')
    print(f"{_time}     ** Part 2 Ended")

def output_row(ul, row):
    user_location = row["User Location"]
    country = ul.locator(user_location)
    if len(country) == 0:
        return  # Ignore, no country to save

    row["Country"] = country
    save_dir = os.path.join(Hyper.HyrdatedTweetLangDir_part2, country)
    ul.save_to_country_file(save_dir, row)

if __name__ == "__main__":
    main()