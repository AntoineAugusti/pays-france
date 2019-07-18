import urllib.request

import json
import csv


def rest_countries():
    url = "https://restcountries.eu/rest/v2/all"
    content = json.load(urllib.request.urlopen(url))

    data = {}
    for country in content:
        data[country["alpha2Code"]] = country

    return data


nationalites = json.load(open("nationalites.json"))
nom_pays = json.load(open("nom_pays.json"))
json_countries = rest_countries()

res = []
with open("cogpays2019.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        iso = row["codeiso2"]
        if iso == "" or iso not in json_countries:
            continue
        res.append(
            {
                "codeiso2": iso,
                "codeiso3": row["codeiso3"],
                "cog": row["cog"],
                "nom": nom_pays[iso],
                "nationalite": nationalites.get(iso),
                "capitale": json_countries[iso]["capital"],
                "population": json_countries[iso]["population"],
                "latitude": json_countries[iso]["latlng"][0],
                "longitude": json_countries[iso]["latlng"][1],
                "aire": json_countries[iso]["area"],
                "coefficient_gini": json_countries[iso]["gini"],
                "fuseaux_horaires": json_countries[iso]["timezones"],
                "frontieres": json_countries[iso]["borders"],
                "devises": json_countries[iso]["currencies"],
                "langues": json_countries[iso]["languages"],
                "traductions": json_countries[iso]["translations"],
                "cioc": json_countries[iso]["cioc"],
            }
        )

with open("pays.json", "w") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
