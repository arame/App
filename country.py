import csv
from csv import writer
from config import Hyper
from data_cleaner import DataCleaner

class Country:
    def __init__(self) -> None:
        self.saved_countries = []
        reader = csv.reader(open(Hyper.UserLocationFile, encoding='utf-8', errors="ignore"))
        for row in reader:
            country = DataCleaner.remove_noise(row[0])
            self.saved_countries.append(country)

        print("Countries from lookup are input")

    def save(self, country):
        if country in self.saved_countries:
            return

        self.saved_countries.append(country)
        with open(Hyper.UserLocationFile, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            try:
                csv_writer.writerow([country, country])
            except:
                pass

