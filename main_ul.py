import csv, os
from config import Hyper
from user_location import UserLocation
import time

def main():
    _time = time.strftime('%Y/%m/%d %H:%M:%S')
    print(f"{_time}     ** Started")
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
    print(f"{_time}     ** Ended")

def output_row(ul, row):
    user_location = row["User Location"]
    country = ul.locator(user_location)
    if len(country) == 0:
        return  # Ignore, no country to save

    row["Country"] = country
    save_dir = os.path.join(Hyper.HyrdatedTweetLangDir, country)
    ul.save_to_country_file(save_dir, row)

            
if __name__ == "__main__":
    main()