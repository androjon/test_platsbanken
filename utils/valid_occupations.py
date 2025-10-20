def create_valid_occupations(data):
    output = {}
    outputOccupationIdSsykLevel4Id = {}
    for i in data["data"]:
        if i["type"] == "job-title":
            term = f"{i['preferred_label']({i['occupation_name_preferred_label']})}"
            id = i["occupation_name_id"]
            output[term] = id
            outputOccupationIdSsykLevel4Id[id] = i["ssyk_level_4_id"]
        else:
            output[i["preferred_label"]] = i["id"]
            outputOccupationIdSsykLevel4Id[i["preferred_label"]] = i["ssyk_level_4_id"]

    output = dict(sorted(output.items()))
    return output, outputOccupationIdSsykLevel4Id