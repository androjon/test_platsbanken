def create_regional_link(id_group, idRegion = None):
    if idRegion == "i46j_HmG_v64":
        idRegion = None
    link = f"https://arbetsformedlingen.se/platsbanken/annonser?p=5:{id_group}&q="
    if idRegion:
        region = "&l=2:" + idRegion
        return link + region
    else:
        return link