import streamlit as st
import requests
import json
import re
from dotenv import load_dotenv
import os
import pandas as pd
from googleapiclient.discovery import build
from googlesearch import search
from bs4 import BeautifulSoup
import wikipedia


load_dotenv()


def get_current_weather(location):  # taken from notebook 1
    """Get the current weather in a given location and date"""
    url = 'https://api.weatherapi.com/v1/current.json?key=f2b1a3991c524713847144853231406&q=' + \
        location+'&dt=today'
    response = requests.get(url)
    if response.status_code == 200:
        # Loading the response data into a dictionary variable
        weather_info = json.loads(response.text)
        # print(weather_info)
    else:
        print("Failed to retrieve data")
    return json.dumps(weather_info)


def get_location_info(location):
    try:
        # Search for the page
        search_results = wikipedia.search(location)
        if not search_results:
            return f"No Wikipedia page found for '{location}'."

        # Get the page
        page = wikipedia.page(search_results[0])

        # Get the summary
        summary = wikipedia.summary(search_results[0], sentences=3)

        # Get the full URL
        url = page.url

        # Fetch the full page content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Try to extract some key information
        info_box = soup.find('table', class_='infobox')
        key_info = {}
        if info_box:
            rows = info_box.find_all('tr')
            for row in rows:
                header = row.find('th')
                data = row.find('td')
                if header and data:
                    key_info[header.text.strip()] = data.text.strip()

        # Compile the results
        result = {
            "title": page.title,
            "summary": summary,
            "url": url,
            "key_info": key_info
        }

        return result

    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found for '{location}'. Please be more specific. Options: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{location}'."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_location_images(location, num_images=3):
    try:
        # Step 1: Search for the Wikipedia page related to the location
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": location,
            "format": "json"
        }

        search_response = requests.get(search_url, params=search_params)
        search_data = search_response.json()

        # Check if any search results were found
        if not search_data['query']['search']:
            print("No Wikipedia page found for this location.")
            return []

        # Get the title of the first result
        page_title = search_data['query']['search'][0]['title']

        # Step 2: Retrieve the images from the Wikipedia page
        image_query_url = "https://en.wikipedia.org/w/api.php"
        image_query_params = {
            "action": "query",
            "titles": page_title,
            "prop": "images",
            "format": "json"
        }

        image_response = requests.get(
            image_query_url, params=image_query_params)
        image_data = image_response.json()

        page = next(iter(image_data['query']['pages'].values()))
        if "images" not in page:
            print("No images found for this location.")
            return []

        # Extract image titles
        image_titles = [img['title'] for img in page['images']][:num_images]

        # Step 3: Retrieve URLs for the images
        image_urls = []
        for title in image_titles:
            image_info_url = "https://en.wikipedia.org/w/api.php"
            image_info_params = {
                "action": "query",
                "titles": title,
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json"
            }

            image_info_response = requests.get(
                image_info_url, params=image_info_params)
            image_info_data = image_info_response.json()

            page_info = next(iter(image_info_data['query']['pages'].values()))
            if "imageinfo" in page_info:
                image_url = page_info['imageinfo'][0]['url']
                image_urls.append(image_url)

        return image_urls

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_coordinates(location):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={
        location}&limit=5&appid={os.getenv("OPENWEATHER_API_KEY")}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()

        if not data:
            print(f"No results found for location: {location}")
            return None

        first_result = data[0]
        df = pd.DataFrame({
            'lat': [first_result["lat"]],
            'lon': [first_result["lon"]]
        })

        return df

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None


def chat_with_llm(prompt, model="llama3.1"):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": model,
        "prompt": f"If a location is mentioned in the user's prompt, respond only with {{location: 'name_of_location'}}. If no location is mentioned, respond as you normally would and make no mention of any location data. After returning the location, forget about the location context entirely. Here is the user's prompt: {prompt}",
        "stream": False
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        llm_response = json.loads(response.text)['response']
        # Regular expression to capture location if it's in the expected format
        location_match = re.search(
            r"\{\s*location\s*:\s*'([^']*)'\s*\}", llm_response)

        if location_match:
            # Extract the location name as a string
            location = location_match.group(1)
            location_coordinates = get_coordinates(location)
            st.map(location_coordinates)
            # Get and display images
            images = get_location_images(location)
            if images:
                st.subheader("Top 3 Images")
                cols = st.columns(3)
                for i, img_url in enumerate(images):
                    cols[i].image(img_url, use_column_width=True,
                                  caption=f"Image {i+1}")
            else:
                st.write("No images found for this location.")

            location_info = get_location_info(location)
            weather_info = get_current_weather(location)

            data = {
                "model" : model,
                "prompt" : f"Here is the information about the location - {location_info} and it's weather information for today - {weather_info}. Summarize it in a bite sized manner, more specifically, a short paragraph. Make it fun, and do not mention lines such as - based on the information you provided and the like. Thank you.",
                "stream" : False
            }

            response = requests.post(url, json=data)
            if response.status_code==200:
                llm_response = json.loads(response.text)['response']
                return llm_response



        else:
            return llm_response  # Return the normal response as a string

    else:
        return f"Error: {response.status_code} - {response.text}"


st.title("lLama with Location capabilities")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your message?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get bot response
    full_prompt = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    response = chat_with_llm(full_prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
