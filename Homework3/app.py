from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
url = 'http://localhost:11434/api/generate'


def llama_response(prompt=''):
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        # "format": "json",
        "stream": False
    }

    return requests.post(url, json=payload).json()['response']

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data['message']

    # if "weather" in user_message.lower():

    #         payload = {
    #             "model": "llama3.1",
    #             "prompt": f"extract the weather and date from this inquiry, and store it in a json format like so {{'location':'location input by the user', 'date':'date input by the user'}}: {user_input}, keep in mind to only return this json and nothing else, dont even say something like Here is the extracted information in JSON format:. the date can be today, tomorrow, or any other specific date. If you cannot process the input to extract either location or date, reply only return by saying 'false' and nothing else",
    #             "stream": False
    #         }

    #         response = requests.post(url, json=payload)
    #         extracted_data = response.json()['response']
    #         # print(extracted_data)

    #         try:
    #             # Convert the string to a dictionary
    #             data_dict = json.loads(extracted_data)

    #             # Check if the required keys are present
    #             if "location" in data_dict and "date" in data_dict:
    #                 # Access the values
    #                 location = data_dict["location"]
    #                 date = data_dict["date"]

    #             else:
    #                 print("Chatbot: Looks like you are trying to get the weather at a certain place! I didn't quite understand your phrase though. Please input the location and date and I will get you the data right away!")
    #                 location = input("Location: ")
    #                 date = input("Date: ")

    #             # Handle the case where the data is incomplete
    #             # For example, you could log an error, raise an exception, etc.

    #         except json.JSONDecodeError:
    #             print("Chatbot: Looks like you are trying to get the weather at a certain place! I didn't quite understand your phrase though. Please input the location and date and I will get you the data right away!")
    #             location = input("Location: ")
    #             date = input("Date: ")

    #         # Call the function to talk about the weather
    #         talk_about_weather(location=location, date=date)


    # render bot reply 
    bot_reply = llama_response(user_message)

    return jsonify({"reply": bot_reply})


@app.route("/")
def index():
    return render_template('index.html') # Serve the HTML interface



if __name__ == '__main__':
    app.run(debug=True)
