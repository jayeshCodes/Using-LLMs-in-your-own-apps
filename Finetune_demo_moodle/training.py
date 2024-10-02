import os

import os.path

import openai
import json



# Import the required library
#from geopy.geocoders import Nominatim

# Initialize Nominatim API
#geolocator = Nominatim(user_agent="geoapi_oceanai")


openai.api_key =  os.environ['OPENAI_API_KEY']
# or use it directly:
#openai.api_key="SK...."

#please MAKE SURE FIND YPUR UPLOADED FILE id!!!!!!!!!!!!!!!!!!!!!!!
#openai.FineTuningJob.create(training_file="file-y8kFJBVB0jA7nbCbUDVZhQKD", model="gpt-4o-mini-2024-07-18")
#gpt-4o-mini-2024-07-18
#gpt-3.5-turbo

from openai import OpenAI
client = OpenAI()

client.fine_tuning.jobs.create(
  training_file="file-y8kFJBVB0jA7nbCbUDVZhQKD",
  model="gpt-4o-mini-2024-07-18"
)


# List 10 fine-tuning jobs
print(client.fine_tuning.jobs.list(limit=10))

# Retrieve the state of a fine-tune
#print(client.fine_tuning.jobs.retrieve("ftjob-abc123"))

# Cancel a job
#client.fine_tuning.jobs.cancel("ftjob-abc123")

# List up to 10 events from a fine-tuning job
#openai.FineTuningJob.list_events(id="ft-abc123", limit=10)

# Delete a fine-tuned model (must be an owner of the org the model was created in)
#openai.Model.delete("ft-abc123")

