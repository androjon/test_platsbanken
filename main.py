import streamlit as st
import requests
import json
import re

@st.cache_data
def import_data(filename):
    with open(filename) as file:
        content = file.read()
    output = json.loads(content)
    return output

def show_initial_information():
    st.title(":blue[Platsbanken - Närliggande yrken]")

def initiate_session_state():
    if "occupationdata" not in st.session_state:
        st.session_state.occupationdata = import_data("data/occupationsId.json")
    if "occupationsSsykLevel4" not in st.session_state:
        st.session_state.occupations_ssyk_level_4 = import_data("data/occupationIdSssykLevel4Id.json")
    if "similar_occupations" not in st.session_state:
        st.session_state.similar_occupations = import_data("data/shortenSimilarData.json")
    if "occupation_keywords" not in st.session_state:
        st.session_state.occupation_keywords = import_data("data/shortenKeywordsData.json")

def fetch_number_of_ads(url):
    response = requests.get(url)
    data = response.text
    json_data = json.loads(data)
    json_data_total = json_data["total"]
    number_of_ads = list(json_data_total.values())[0]
    return number_of_ads

def number_of_ads(ssyk_id, word = None):
    base = "https://jobsearch.api.jobtechdev.se/search?"
    end = "&limit=0"

    regionId = "zdoY_6u5_Krt"

    if word:
        word = word.replace(",", "%2B").replace(" ", "")
        url = base + "occupation-group=" + ssyk_id + "&region=" + regionId + "&q=" + word + end
    else:
        url = base + "occupation-group=" + ssyk_id + "&region=" + regionId + end

    number_of_ads = fetch_number_of_ads(url)
    return number_of_ads

def convert_text(text):
    text = text.strip()
    text = text.lower()
    to_clean = {
        " ": "%20",
        "\^": "%5E",
        "'": "%22"}
    for key, value in to_clean.items():
        text = re.sub(key, value, text)
    return text

def create_links(name, id_group, keywords = None):
    #Multiple groups in Platsbanken - p=5:5qT8_z9d_8rw;5:J17g_Q2a_2u1
    #There seems to be a 255 character limit for the link and therefore it is difficult to add more than 10 words

    #Går fortfarande inte att hitta flera olika Maskinoperatörer (Maskinoperatör, tobaksindustri/läkemedel och så vidare). Antagligen eftersom den inte söker i taxonomivärdena utan bara i rubrik och text.

    #För att exkludera går det att använda projektledare -it
    #https://arbetsformedlingen.se/platsbanken/annonser?q=projektledare%20-it

    #projektledare AND ("utvecklare" OR "it") -junior
    #https://arbetsformedlingen.se/platsbanken/annonser?q=projektledare%20AND%20(%22utvecklare%22%20OR%20%22it%22)%20-junior

    #%2B = +
    name = name.replace(",", "%2B").replace(" ", "")

    regionId = "zdoY_6u5_Krt"
    regionQuery = "&l=2:" + regionId

    base = f"https://arbetsformedlingen.se/platsbanken/annonser?p=5:{id_group}&q="
    baseAndName = base + "%20" + name + regionQuery
    onlyName = f"https://arbetsformedlingen.se/platsbanken/annonser?&q={name}{regionQuery}"

    if keywords:    
        keywordsSearchable = []
        for s in keywords:
            s = convert_text(s)
            keywordsSearchable.append(s)

        baseAndFirstKeyword  = base + "%20" + keywordsSearchable[0] + regionQuery
        baseAndSecondKeyword = base + "%20" + keywordsSearchable[1] + regionQuery
        baseAndThirdKeyword = base + "%20" + keywordsSearchable[2] + regionQuery
        baseAndFourthKeyword = base + "%20" + keywordsSearchable[3] + regionQuery
    
    else:
        baseAndFirstKeyword = None
        baseAndSecondKeyword = None
        baseAndThirdKeyword = None
        baseAndFourthKeyword = None

    links = [base + regionQuery, onlyName, baseAndName, baseAndFirstKeyword, baseAndSecondKeyword, baseAndThirdKeyword, baseAndFourthKeyword]
    
    return links 


def post_selected_occupation(nameOccupation, idOccupation):
    ssykInfo = st.session_state.occupations_ssyk_level_4.get(idOccupation)
    ssykId = ssykInfo["ssyk_id"]
    ssykName = ssykInfo["ssyk_name"]

    st.write("För att göra det lite mer realistiskt sker alla sökningar i **Västra Götalands län**")

    if ssykId:
        similar = st.session_state.similar_occupations.get(idOccupation)
        keywords = st.session_state.occupation_keywords.get(idOccupation)

        match = re.match(r"^(.*?)\s*\(", nameOccupation)
        if match:
            name = match.group(1)
        else:
            name = nameOccupation


        if keywords:
            links = create_links(name, ssykId, keywords)

            a, b = st.columns(2)

            a.write("**Utifrån vald yrkesgrupp och valt yrke**")
            b.write("**Utifrån vald yrkesgrupp**")

            adsGroup = number_of_ads(ssykId, None)
            adsGroupAndSelectedName = number_of_ads(ssykId, name)

            a.link_button(f"{ssykName} och *{name}* ({adsGroupAndSelectedName})", links[2], icon = ":material/link:")  

            b.link_button(f"{ssykName} ({adsGroup})", links[0], icon = ":material/link:")      

            st.write("**Utifrån vald yrkesgrupp och ett relevant nyckelord**")

            c, d = st.columns(2)

            adsGroupAndWord1 = number_of_ads(ssykId, keywords[0])
            adsGroupAndWord2 = number_of_ads(ssykId, keywords[1])
            adsGroupAndWord3 = number_of_ads(ssykId, keywords[2])
            adsGroupAndWord4 = number_of_ads(ssykId, keywords[3])
            
            c.link_button(f"{ssykName} och *{keywords[0]}* ({adsGroupAndWord1})", links[3], icon = ":material/link:")

            d.link_button(f"{ssykName} och *{keywords[1]}* ({adsGroupAndWord2})", links[4], icon = ":material/link:")

            c.link_button(f"{ssykName} och *{keywords[2]}* ({adsGroupAndWord3})", links[5], icon = ":material/link:")

            d.link_button(f"{ssykName} och *{keywords[3]}* ({adsGroupAndWord4})", links[6], icon = ":material/link:")

        if similar:
            st.header("Närliggande yrken")

            similarWithMostAds = {}

            for nameSimilar, id in similar.items():
                ssykInfoSimilar = st.session_state.occupations_ssyk_level_4.get(id)
                ssykIdSimilar = ssykInfoSimilar["ssyk_id"]
                ssykNameSimilar = ssykInfoSimilar["ssyk_name"]
                if ssykIdSimilar:
                    linksSimilar = create_links(nameSimilar, ssykIdSimilar, None)
                    adsSimilarOccupation = number_of_ads(ssykIdSimilar, nameSimilar)
                    adsSimilarGroup = number_of_ads(ssykIdSimilar, None)

                    similarWithMostAds[nameSimilar] = {
                        "ads": adsSimilarOccupation,
                        "adsGroup": adsSimilarGroup,
                        "linkGroup": linksSimilar[0],
                        "groupName": ssykNameSimilar,
                        "linkGroupAndName": linksSimilar[2]}
                    
            similarWithMostAds = dict(sorted(similarWithMostAds.items(), key = lambda item: item[1]["ads"], reverse = True)[:5])

            e, f = st.columns(2)

            e.write("**Utifrån närliggande yrkesgrupp och yrke**")
            f.write("**Utifrån närliggande yrkesgrupp**")

            for nameSimilar, information in similarWithMostAds.items():
                e.link_button(f"{information['groupName']} och *{nameSimilar}* ({information['ads']})", information["linkGroupAndName"], icon = ":material/link:")

                f.link_button(f"{information['groupName']} ({information['adsGroup']})", information["linkGroup"], icon = ":material/link:")

def choose_occupation_name():
    show_initial_information()

    selectedOccupation = st.selectbox(
        "Välj en yrkesbenämning",
        list(st.session_state.occupationdata),
        placeholder = "",
        index = None)

    if selectedOccupation:
        idSelectedOccupation = st.session_state.occupationdata.get(selectedOccupation)
        post_selected_occupation(selectedOccupation, idSelectedOccupation)

def main ():
    initiate_session_state()
    choose_occupation_name()
    
if __name__ == '__main__':
    main ()