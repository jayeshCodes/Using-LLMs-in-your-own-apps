import os

import os.path

import openai
import json

openai.api_key =  os.environ['OPENAI_API_KEY']
# or use it directly:
#openai.api_key="SK...."

# List 10 fine-tuning jobs
#print(openai.FineTuningJob.list(limit=10))

# Retrieve the state of a fine-tune
#print(openai.FineTuningJob.retrieve("ftjob-J0V1mxPCcpdIkHyxf5IHjsZg"))

# Cancel a job
#openai.FineTuningJob.cancel("ft-abc123")

# List up to 10 events from a fine-tuning job
#openai.FineTuningJob.list_events(id="ft-abc123", limit=10)

# Delete a fine-tuned model (must be an owner of the org the model was created in)
#openai.Model.delete("ft-abc123")

i=0
while (i<20):
    user_input = input("Chat Input:")
    completion = openai.ChatCompletion.create(
        #model="ft:gpt-3.5-turbo-0613:personal::82OOrYsV",
        model="ft:gpt-3.5-turbo-0613:personal::8DdiQ7Ac",
        messages=[
        {"role": "system", "content": "AiBot is a theocean.ai chatbot"},
        {"role": "user", "content": user_input}
        ])
    print(completion.choices[0].message)
    
