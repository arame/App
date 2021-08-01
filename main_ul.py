import csv, os
import pandas as pd
from config import Hyper
from user_location import UserLocation
import time
from helper import Helper

def main():
    #part1()
    part2()

def part1():
    Helper.printline("     ** Started Part 1")
    file = os.path.join(Hyper.HyrdatedTweetDirNoCountry, Hyper.HyrdatedTweetFile)
    i = 0
    ul = UserLocation()
    with open(file, encoding="utf-8", newline='') as csvfile:
        Helper.printline(f"     {file} opened")
        reader = csv.DictReader(csvfile)
        for row in reader:
            i += 1
            output_row(ul, row)
            if i % 100 == 0:
                Helper.printline(f"     {i} rows processed")

    Helper.printline(f"     ** Part 1 Ended")

def part2():
    # Join all the tweet files for each country into one file for the langauage
    Helper.printline("     ** Started Part 2")
    os.chdir(Hyper.HyrdatedTweetLangDir_part2)
    Helper.printline(f"Changed directory to {Hyper.HyrdatedTweetLangDir_part2}")
    list_dirs = os.listdir()
    list_dirs.remove("no_country")
    big_df = pd.concat( [pd.read_csv(os.path.join(_dir,'tweets.csv')) for _dir in list_dirs]) 
    big_df.to_csv(Hyper.HyrdatedTweetLangFile)

    Helper.printline(f"     ** Part 2 Ended")

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