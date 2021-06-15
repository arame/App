import re
from geopy.geocoders import Nominatim
from tqdm import tqdm
import csv
from csv import writer
from config import Hyper

class UserLocation:
    def __init__(self) -> None:
        # initialize geolocator
        self.geolocator = Nominatim(user_agent='Tweet_locator')
        self.user_locations ={}
        reader = csv.reader(open(Hyper.UserLocationFile))
        for row in reader:
            key = row[0]
            self.user_locations[key] = row[1]

    def save_user_location(self, user_location, country):
        self.user_locations[user_location] = country
        # Open file in append mode
        with open(Hyper.UserLocationFile, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            try:
                csv_writer.writerow([user_location, country])
            except:
                pass
            
    def locator(self, user_location):
        if user_location == None:
            return ""

        if user_location in self.user_locations:
            country = self.user_locations[user_location]
            return country

        country = self.geo_locator(user_location)
        self.save_user_location(user_location, country)
        return country

    def geo_locator(self, user_location):
        try :
            # get location
            location = self.geolocator.geocode(user_location, language='en')
            # get coordinates
            location_exact = self.geolocator.reverse(
                        [location.latitude, location.longitude], language='en')
            # get country codes
            c_code = location_exact.raw['address']['country_code']
            country = location_exact.raw['address']['country']
            return country

        except:
            return ""
