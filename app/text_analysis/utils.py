import spacy
import requests
from .models import Person, Frequency
import collections


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


def get_person_infos_from_wikidata(lst_names, names_frequency):
    """
        Function that allows to extract some basics person infos from wikidata
    """
    output = []
    for name in lst_names:
        person_name = ""
        name_splitted = name.split(" ")
        for element in name_splitted:
            if element == name_splitted[-1]:
                person_name += element
            else:
                person_name += element + "_"

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
        if not len(data['results']['bindings']):
            person_json = {'info' : f'no data found from wikidata for {person_name}'}
            output.append(person_json)
        else:
            data = data['results']['bindings'][0]
            person_json = formatting_Wiki_Data_Result(data)
            save_to_database(person_json, names_frequency)
            output.append(person_json)

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

def save_to_database(data_dict, names_frequency):
    """
        Function that allows saving data into database
    """
    print("------- save to the db function")
    name = data_dict["name"]
    frequency = names_frequency[str(name)]
    print("-------------------------- name", name)
    print("------ name frequency : ", names_frequency[str(name)])
    if Person.objects.filter(name=name).exists():
        print("---------------------- existe dans la database !!!")
        p = Person.objects.get(name=name)
        p2 = Frequency.objects.get(person=p.id)
        old_freq = p2.freq
        new_freq = old_freq + frequency
        Frequency.objects.filter(id=p2.id).update(freq=new_freq)
        print("value saved !!!")
    else:
        print("---------------------- n existe PAS dans la database !!!")
        p = Person(**data_dict)
        p2 = Frequency(person=p, freq=frequency)
        p.save()
        p2.save()

def extract_names_frequency(lst_names):
    """
        Function that allows to exract name frequency from a list
    """
    counter = collections.Counter(lst_names)
    return dict(counter)

def remove_duplicates(lst_names):
    """
        Function that allow to remove duplicate name from a list
    """
    return list(set(lst_names))
