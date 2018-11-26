from SPARQLWrapper import SPARQLWrapper, JSON
from requests import get
import json


def get_spaqrl_id(film_name):
    json_get = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbgetentities',
        'titles': film_name,
        'sites': 'enwiki',
        'props': '',
        'format': 'json'
    }).json()
    result = list(json_get['entities'])[0]
    return result


def get_sparql_result_by_film_name(film_name):
    film_id = get_spaqrl_id(film_name)
    try:
        if int(film_id) == -1:
            return -1
    except ValueError:
        pass
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""SELECT ?avLabel WHERE {
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
      wd:""" + film_id + """ wdt:P57 ?name
      OPTIONAL {?name wdt:P166 ?av.}
    }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    clean_json = []
    for result in results["results"]["bindings"]:
        clean_json.append(result["avLabel"]["value"])
    return json.dumps(clean_json, indent=4)
