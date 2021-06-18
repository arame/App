import csv, os
from config import Hyper
from user_location import UserLocation

def main():
    file = os.path.join(Hyper.HyrdatedTweetDir, Hyper.HyrdatedTweetFile)
    i = 0
    ul = UserLocation()
    with open(file, encoding="utf-8", newline='') as csvfile:
        print(f"{file} opened")
        reader = csv.DictReader(csvfile)
        for row in reader:
            i += 1
            output_row(ul, row)
            if i % 100 == 0:
                print(f"{i} rows processed")

    print(f"")

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