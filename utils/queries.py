queryOccupationIdSssykId = """
query occupation_info {
  concepts(type: "occupation-name") {
    id
    occupationGroup: broader(type: "ssyk-level-4"){
      id
      ssyk_code_2012
      preferred_label}
    }
  }"""