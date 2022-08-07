import spacy
import requests

def extract_names(text):
    """
        Function that allows to extract the names of people from a text
    """
    english_nlp = spacy.load('en_core_web_sm')
    spacy_parser = english_nlp(text)
    names = []
    for entity in spacy_parser.ents:
        if entity.label_ == "PERSON":
            names.append(entity.text)
    return names


def get_person_infos_from_wikidata(lst_names):
    """
        Function that allows to extract some basics person infos from wikidata
    """
    for name in lst_names:
        person_name = ""
        name_splitted = name.split(" ")
        print("name_splitted : ", name_splitted)
        print("nem de -1: ", name_splitted[-1])
        for element in name_splitted:
            if element == name_splitted[-1]:
                print("---- TRUEEEE")
                person_name += element
            else:
                person_name += element + "_"
        print("---------------------- person name : ", person_name)
        sparql_query ="""
            prefix schema: <http://schema.org/>
            SELECT ?itemLabel ?occupationLabel ?genderLabel ?bdayLabel ?sexLabel ?nationalityLabel ?imageLabel
            WHERE {
              <https://en.wikipedia.org/wiki/%s> schema:about ?item .
              ?item wdt:P106 ?occupation .
              ?item wdt:P21 ?gender .
              ?item wdt:P569 ?bday .
              ?item wdt:P21 ?sex .
              ?item wdt:P27 ?nationality .
              ?item wdt:P18 ?image
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
            }
            LIMIT 1""" % person_name


        url = 'https://query.wikidata.org/sparql'

        r = requests.get(url, params={'format': 'json', 'query': sparql_query})
        data = r.json()
        print("-------- resultat bindings : ", data['results']['bindings'])
        print("-------- resultat bindings zero : ", data['results']['bindings'][0])
        print("-----------------------------------------------------------------")
    return 1
