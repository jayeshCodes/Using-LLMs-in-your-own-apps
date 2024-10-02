import os
import json
import os.path

import openai

upload_file_path="train.jsonl"

openai.api_key =  os.environ['OPENAI_API_KEY']
# or use it directly:
#openai.api_key="SK...."
'''


# Import the required library
#from geopy.geocoders import Nominatim

# Initialize Nominatim API
#geolocator = Nominatim(user_agent="geoapi_oceanai")






with open(upload_file_path, "rb") as file:
    response=openai.File.create(
        file=file,
        purpose='fine-tune'
    )

file_id=response['id']
print (f"File uploaded sucessfully with ID:{file_id}")
'''

from openai import OpenAI
client = OpenAI()


with open(upload_file_path, "rb") as file:
    response=client.files.create(
        file=file,
        purpose='fine-tune',
    )

print (response)
file_id=response.id
print (f"File uploaded sucessfully with ID:{file_id}")
