import streamlit as st
import json
import re

@st.cache_data
def import_data(filename):
    with open(filename) as file:
        content = file.read()
    output = json.loads(content)
    return output

def show_initial_information():
    st.title(":primary[Platsbanken - Närliggande yrken]")

def initiate_session_state():
    if "occupationdata" not in st.session_state:
        st.session_state.occupationdata = import_data("data/occupationsId.json")
    if "occupationsSsykLevel4" not in st.session_state:
        st.session_state.occupations_ssyk_level_4 = import_data("data/occupationIdSssykLevel4Id.json")
    if "similar_occupations" not in st.session_state:
        st.session_state.similar_occupations = import_data("data/shortenSimilarData.json")
    if "occupation_keywords" not in st.session_state:
        st.session_state.occupation_keywords = import_data("data/shortenKeywordsData.json")

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

def create_links(name, id_groups, keywords = None):
    #Multiple groups in Platsbanken - p=5:5qT8_z9d_8rw;5:J17g_Q2a_2u1
    #There seems to be a 255 character limit for the link and therefore it is difficult to add more than 10 words

    weight = 1.2

    test = f"^{str(weight)}"
    
    base = f"https://arbetsformedlingen.se/platsbanken/annonser?p=5:{id_groups[0]}&q="
    
    keywords_split = []
    for s in keywords:
        s = convert_text(s)
        keywords_split.append(s)

    keywordsString = "%20".join(keywords_split)

    baseAndName = base + "%20" + name
    onlyName = f"https://arbetsformedlingen.se/platsbanken/annonser?&q={name}"

    baseAndNameAndFirstKeyword = base + "%20" + name + "%20" + keywords_split[0]
    baseAndNameAndSecondKeyword = base + "%20" + name + "%20" + keywords_split[1]

    baseAndFirstKeyword  = base + "%20" + keywords_split[0]
    baseAndSecondKeyword = base + "%20" + keywords_split[1]
    baseAndThirdKeyword = base + "%20" + keywords_split[2]
    baseAndFourthKeyword = base + "%20" + keywords_split[3]

    links = [base, onlyName, baseAndName, baseAndFirstKeyword, baseAndSecondKeyword, baseAndThirdKeyword, baseAndFourthKeyword]
    
    return links 


def post_selected_occupation(nameOccupation, idOccupation):
    ssykId = st.session_state.occupations_ssyk_level_4.get(idOccupation)
    similar = st.session_state.similar_occupations.get(idOccupation)
    keywords = st.session_state.occupation_keywords.get(idOccupation)

    match = re.match(r"^(.*?)\s*\(", nameOccupation)
    if match:
        name = match.group(1)
    else:
        name = nameOccupation


    if keywords:
        links = create_links(name, [ssykId], keywords)

        a, b = st.columns(2)

        a.link_button(f"Yrkesgrupp", links[0], icon = ":material/link:")

        b.link_button(f"Valt yrke/jobbtitel", links[1], icon = ":material/link:")        

        a.link_button(f"Yrkesgrupp och valt yrke/jobbtitel", links[2], icon = ":material/link:")        

        st.divider()

        c, d = st.columns(2)
        
        c.link_button(f"Yrkesgrupp och valt nyckelord ({keywords[0]})", links[3], icon = ":material/link:")

        d.link_button(f"Yrkesgrupp och valt nyckelord ({keywords[1]})", links[4], icon = ":material/link:")

        c.link_button(f"Yrkesgrupp och valt nyckelord ({keywords[2]})", links[5], icon = ":material/link:")

        d.link_button(f"Yrkesgrupp och valt nyckelord ({keywords[3]})", links[6], icon = ":material/link:")

    if similar:
        st.divider()
        st.header("Närliggande yrken")

        for nameSimilar, id in similar.items():
            ssykIdSimilar = st.session_state.occupations_ssyk_level_4.get(id)
            keywordsSimilar = st.session_state.occupation_keywords.get(id)
            linksSimilar = create_links(nameSimilar, [ssykIdSimilar], keywordsSimilar)
            st.link_button(nameSimilar, linksSimilar[2], icon = ":material/link:")

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