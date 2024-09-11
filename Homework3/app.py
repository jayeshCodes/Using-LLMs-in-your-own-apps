from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)
url = 'http://localhost:11434/api/generate'


def get_current_weather(location, date):  # taken from notebook 1
    """Get the current weather in a given location and date"""
    url = 'https://api.weatherapi.com/v1/current.json?key=f2b1a3991c524713847144853231406&q=' + \
        location+'&dt='+date
    response = requests.get(url)
    if response.status_code == 200:
        # Loading the response data into a dictionary variable
        weather_info = json.loads(response.text)
        # print(weather_info)
    else:
        print("Failed to retrieve data")
    return json.dumps(weather_info)


def talk_about_weather(location, date):
    info = get_current_weather(location, date)

    # init payload for response
    payload = {
        "model": "llama3.1",
        "prompt": f"talk about the weather info which i am about to provide: {info}, dont say anything like - heres the information you provided, or based on the information you provided and so on. be as fun as possible",
        "stream": False
    }

    # Print the chatbot's response
    response = requests.post(url, json=payload)
    return response.json()['response']


@app.route('/get-manual-input', methods=['POST'])
def manual_input():
    """
    Receives location and date input from the frontend
    """
    data = request.get_json()
    location = data.get('location')
    date = data.get('date')

    if location and date:
        return jsonify({"location": location, "date": date, "status": "success"})
    else:
        return jsonify({"error": "Location and date are required.", "status": "error"})


def llama_response(prompt='', location=None, date=None):
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }

    if "weather" in prompt.lower() and not (location and date):
        payload = {
            "model": "llama3.1",
            "prompt": f"extract the weather and date from this inquiry, and store it in a json format like so {{'location':'location input by the user', 'date':'date input by the user'}}: {prompt}, keep in mind to only return this json and nothing else. The date can be today, tomorrow, or any other specific date. If you cannot process the input to extract either location or date, reply by saying 'false' and nothing else.",
            "stream": False
        }

        response = requests.post(url, json=payload)
        extracted_data = response.json().get('response')

        try:
            # Convert the string to a dictionary
            data_dict = json.loads(extracted_data)

            if "location" in data_dict and "date" in data_dict:
                # Extracted successfully
                location = data_dict["location"]
                date = data_dict["date"]
                return talk_about_weather(location, date)
            else:
                # Failed to extract location or date
                # return {"error": "Invalid location/date. Please provide them manually."}
                location, date = manual_input()
                print(location, date)
                return talk_about_weather(location, date)
        except json.JSONDecodeError:
            # Handle JSON decode error
            return {"error": "Unable to extract location/date. Please provide them manually."}

    elif location and date:
        # Use location and date provided by the user
        return talk_about_weather(location, date)

    else:
        # For non-weather-related responses
        return requests.post(url, json=payload).json().get('response', 'Error in response')


@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data['message']
    location = data.get('location')
    date = data.get('date')

    # if(location!='' and date!=''):
    #     bot_reply=talk_about_weather(location, date)

    # else:
    # Get bot reply
    bot_reply = llama_response(user_message, location, date)

    if isinstance(bot_reply, dict) and 'error' in bot_reply:
        return jsonify({"reply": bot_reply['error'], "request_input": True})
    else:
        return jsonify({"reply": bot_reply})


@app.route("/")
def index():
    return render_template('index.html')  # Serve the HTML interface


if __name__ == '__main__':
    app.run(debug=True)
