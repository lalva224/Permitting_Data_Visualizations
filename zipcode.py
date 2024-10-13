import requests 
from dotenv import load_dotenv
import os 
import pandas as pd
from openai import OpenAI
import json
load_dotenv()

API_KEY = os.getenv('OPENAI_KEY')
# NEIGHBORHOODS_TO_TOTAL_PERMITS = {}

#first get zipcode from neighborhood
def zipcode_from_neighborhoods(neighborhoods):
    zipcodes = []
    for neighborhood in neighborhoods:
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={neighborhood},Orlando,FL&key={API_KEY}'
        response = requests.get(url)
        data = response.json()
        zipcode = data['results'][0]['address_components'][-1]['long_name']
        zipcodes.append(zipcode)
    return zipcodes


def zipcode_from_address(address):
    encoded_address = address.replace(' ','+')

    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address},Orlando,FL&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    # print(data)
    zipcode = data['results'][0]['address_components'][-2]['long_name']

    return zipcode

def read_total_num_permits_file(filepath):
    df = pd.read_csv(filepath)
    neighborhoods = df['Neighborhood'].tolist()
    total_permits = df['Number of Permits'].tolist()
    return dict(zip(neighborhoods,total_permits))
    
def get_data(neighborhoods_total_permits_dict):
    prompt = f""""
    I am going to give you a list of dictionaries which will look like this:
   
    {neighborhoods_total_permits_dict} Now please give me the zipcode for each one. 
    Once you have the zipcodes please give me the number of homeowners under that zipcode. 
    Then lastly, I want you to divide the total permits/ home owners and give me the percentage with permitting data
    Please return in json format
    It will look like this:
    {{

    neighborhood : 'Palmetto Bay',
    Total Permits: '3455'
    zipcode : '33157',
    homeowners: 20123
    percentage with permitting data : '23%'
    }}
    """
    client = OpenAI(api_key=API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    response = completion.choices[0].message.content  
    return response  

neighborhoods_total_permits_dict = read_total_num_permits_file('Total_Permitting_By_Neighborhood.xlsx.csv')
data = json.loads(get_data(neighborhoods_total_permits_dict))
dataframe = pd.DataFrame(data['data'])
dataframe.to_csv('percentages of homeowners with permitting data.csv')
print(dataframe)
