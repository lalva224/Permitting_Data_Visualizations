import requests 
from dotenv import load_dotenv
import os 
import pandas
load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')

#first get zipcode from neighborhood
def zipcode_from_neighborhood(neighborhood):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={neighborhood},Orlando,FL&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    zipcode = data['results'][0]['address_components'][-1]['long_name']
    return zipcode 

def zipcode_from_address(address):
    encoded_address = address.replace(' ','+')

    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address},Orlando,FL&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    # print(data)
    zipcode = data['results'][0]['address_components'][-2]['long_name']

    return zipcode

# def read_total_num_permits_file():
