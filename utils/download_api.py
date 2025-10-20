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
    url = "https://api-jobtech-taxonomy-api-prod-write.prod.services.jtech.se/v1/taxonomy/graphql?"
    curl = url + "query=" + text
    return curl

def download_api(query):
    curl = convert_query_to_curl(query)
    header = {"api-key": "admin-3|kvalificerad-yrkesfiskare-3"}
    response = requests.get(url = curl, headers = header)
    data = response.text
    jsonData = json.loads(data)
    return jsonData

def get_data_api(url):
    response = requests.get(url = url)
    data = response.text
    try:
        jsonData = json.loads(data)
        return jsonData
    except json.JSONDecodeError as e:
        return None