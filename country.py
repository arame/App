import csv
from csv import writer
from config import Hyper
from data_cleaner import DataCleaner
from geopy.geocoders import Nominatim

class Country:
    def __init__(self) -> None:
        self.geolocator = Nominatim(user_agent='Tweet_locator')
        self.saved_countries = []
        reader = csv.reader(open(Hyper.UserLocationFile, encoding='utf-8', errors="ignore"))
        for row in reader:
            country = DataCleaner.remove_noise(row[0])
            self.saved_countries.append(country)


    def save(self, country):
        if country in self.saved_countries:
            return

        self.saved_countries.append(country)
        country_1 = self.geo_locator(country)
        with open(Hyper.UserLocationFile, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            try:
                csv_writer.writerow([country, country_1])
            except:
                pass

    def geo_locator(self, country):
        try :
            # get location
            location = self.geolocator.geocode(country, language='en')
            # get coordinates
            location_exact = self.geolocator.reverse(
                        [location.latitude, location.longitude], language='en')
            # get country codes
            c_code = location_exact.raw['address']['country_code']
            country_1 = location_exact.raw['address']['country']
            return country_1

        except:
            return ""
