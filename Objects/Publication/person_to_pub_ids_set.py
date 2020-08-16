import sys
import requests
import json
import logging

from Packages.lib.print import eprint, epprint

# logging_format = "{levelname}: {pathname}#{lineno} --> {msg}"  # {asctime}
logging_format = r"%(levelname)s: #%(lineno)d --> %(msg)s"  # %(asctime)s

logging_kwargs = {
    "filename": "person_to_pub_ids_set.log",
    "filemode": "w",
    # "stream": sys.stderr,
    "level": logging.DEBUG,
    "style": r"%",
    "format": logging_format,
    "datefmt": r"%Y-%m-%d %H:%M:%S",
    # "force": True,
}


logging.basicConfig(**logging_kwargs)

########################################################


def get_pub_ids_set(person, cache):
    query = make_query(person)
    docs = scanr_publications_request(query, cache)
    assert isinstance(docs, list), epprint(docs)
    pub_ids_set = filter(docs, person)
    return pub_ids_set


########################################################


def make_query(person):
    firstname_key_initial = person["firstname_key_initial"]
    firstname_key = person["firstname_key"]
    lastname_key = person["lastname_key"]
    query = f"({firstname_key_initial} {lastname_key})|({firstname_key} {lastname_key})"
    return query


########################################################


def filter(docs, person):
    pub_ids_set = set()
    for publication in docs:
        data = publication["value"]
        pub_id = data["id"]
        pub_ids_set.add(pub_id)
    return pub_ids_set


########################################################
URL = "https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/publications/search"


def scanr_publications_request(query, cache):
    ##
    params = {
        "pageSize": 10000,
        "query": query,
        "searchFields": ["authors.fullName"],
        "sourceFields": ["id"],
        "filters": {
            "year": {
                "type": "LongRangeFilter",
                "max": 2021,
                "min": 2015,
                "missing": False,
            }
        },
    }
    key = json.dumps(params)
    if cache.holds_key(key):
        results = cache.get_key_value(key)
        return results
    eprint(f"\tSending request to ScanR for {query}", end="... ")
    r = requests.post(URL, json=params)
    eprint(f"Done, response size = {len(r.content)}")
    assert r.status_code == 200, r
    r_json = r.json()
    if int(r_json["total"]) >= 10000:
        eprint(f'{"="*50}> Too many results! Skipping results beyond 10000')
    results = r_json["results"]
    cache.update_key_value(key, results)
    return results

