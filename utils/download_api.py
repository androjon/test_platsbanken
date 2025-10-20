import re
import json
import requests

def convert_query_to_curl(text):
    convert = {
       "{": "%7B",
       "}": "%7D",
       "\n": "%0A",
       ":": "%3A",
       "\"": "%22",
       " ": "%20"}
    for key, value in convert.items():
        text = re.sub(key, value, text)
    url = "https://taxonomy.api.jobtechdev.se/v1/taxonomy/graphql?"
    curl = url + "query=" + text
    return curl

def download_api(query):
    curl = convert_query_to_curl(query)
    response = requests.get(url = curl)
    data = response.text
    json_data = json.loads(data)
    return json_data

def get_data_api(url):
    response = requests.get(url = url)
    data = response.text
    try:
        json_data = json.loads(data)
        return json_data
    except json.JSONDecodeError as e:
        return None