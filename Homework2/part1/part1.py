import os
from groq import Groq
import requests
import json

api_key = os.environ.get("GROQ_API_KEY")


def get_current_weather(location, date):  # taken from notebook 1
    """Get the current weather in a given location and date"""
    url = 'https://api.weatherapi.com/v1/current.json?key=f2b1a3991c524713847144853231406&q=' + \
        location+'&dt='+date
    response = requests.get(url)
    if response.status_code == 200:
        # Loading the response data into a dictionary variable
        weather_info = json.loads(response.text)
    else:
        print("Failed to retrieve data")
    return json.dumps(weather_info)


def talk_about_weather(location, date):
    info = get_current_weather(location, date)
    # Initialize Groq client with API KEY
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    # Create a chat completion with the user's input
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"talk about the weather info which i am about to provide: {info}, dont say anything like - heres the information you provided, or based on the information you provided and so on. be as fun as possible",
            }
        ],
        model="llama3-8b-8192",
    )

    # Print the chatbot's response
    response = chat_completion.choices[0].message.content
    print(f"Chatbot: {response}")


def chatbot():
    # Initialize Groq client with API KEY
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    while True:
        user_input = input("You: ")
        # Exit the chat if the user types 'exit'
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        if "weather" in user_input.lower():
            messages = [
                {
                    "role": "user",
                    "content": f"extract the weather and date from this inquiry, and store it in a json format like so {{'location':'location input by the user', 'date':'date input by the user'}}: {user_input}, keep in mind to only return this json and nothing else, dont even say something like Here is the extracted information in JSON format:. the date can be today, tomorrow, or any other specific date. If you cannot process the input to extract either location or date, reply only return by saying 'false' and nothing else"
                }
            ]
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama3-8b-8192",
            )
            extracted_data = chat_completion.choices[0].message.content
            # print(extracted_data)

            try:
                # Convert the string to a dictionary
                data_dict = json.loads(extracted_data)

                # Check if the required keys are present
                if "location" in data_dict and "date" in data_dict:
                    # Access the values
                    location = data_dict["location"]
                    date = data_dict["date"]

                else:
                    print("Chatbot: Looks like you are trying to get the weather at a certain place! I didn't quite understand your phrase though. Please input the location and date and I will get you the data right away!")
                    location = input("Location: ")
                    date = input("Date: ")

                # Handle the case where the data is incomplete
                # For example, you could log an error, raise an exception, etc.

            except json.JSONDecodeError:
                print("Chatbot: Looks like you are trying to get the weather at a certain place! I didn't quite understand your phrase though. Please input the location and date and I will get you the data right away!")
                location = input("Location: ")
                date = input("Date: ")


            # Call the function to talk about the weather
            talk_about_weather(location=location, date=date)

            continue

        # Create a chat completion with the user's input
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama3-8b-8192",
        )

        # Print the chatbot's response
        response = chat_completion.choices[0].message.content
        print(f"Chatbot: {response}")


chatbot()
