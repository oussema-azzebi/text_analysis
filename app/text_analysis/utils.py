import spacy
import requests
from .models import Person


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
    output = []
    for name in lst_names:
        person_name = ""
        name_splitted = name.split(" ")
        print("name_splitted : ", name_splitted)
        print("name de -1: ", name_splitted[-1])
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
        data = data['results']['bindings'][0]
        person_json = formatting_Wiki_Data_Result(data)
        print("---------- person_json :", person_json)
        #save_to_database(person_json)
        output.append(person_json)
    print("--------------------- database content", Person.objects.all())

    return output

def formatting_Wiki_Data_Result(data):
    """
        Function that allows to put the data received by wikidata in
        the json format that we want to display and save into the database.
    """
    person_json = {}
    person_json['name'] = data['itemLabel']['value']
    person_json['occupation'] = data['occupationLabel']['value']
    person_json['gender'] = data['genderLabel']['value']
    person_json['birthday'] = data['bdayLabel']['value']
    person_json['sex'] = data['sexLabel']['value']
    person_json['nationality'] = data['nationalityLabel']['value']
    person_json['image_link'] = data['imageLabel']['value']
    return person_json

def save_to_database(data_dict):
    """
        Function that allows saving data into Person model
    """
    name = data_dict["name"]
    if not Person.objects.filter(name=name).exists():
        p = Person(**data_dict)
        p.save()
