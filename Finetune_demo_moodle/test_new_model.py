from openai import OpenAI
client = OpenAI()

openai.api_key =  os.environ['OPENAI_API_KEY']
# or use it directly:
#openai.api_key="SK...."

completion = client.chat.completions.create(
  #make sure change this to your new model
  model="ft:gpt-4o-mini-2024-07-18:personal::ADhoG2KS",
  
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)
print(completion.choices[0].message)
