import sys
import requests
import json
import logging
import urllib

from Packages.lib.print import eprint, epprint

# logging_format = "{levelname}: {pathname}#{lineno} --> {msg}"  # {asctime}
logging_format = r"%(levelname)s: #%(lineno)d --> %(msg)s"  # %(asctime)s

logging_kwargs = {
    "filename": "pub_id_to_publication.log",
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


def get_data(pub_id, cache):
    result = scanr_publications_request(pub_id, cache)
    if result is None:
        return None
    assert isinstance(result, dict), epprint(result)
    data = extract_data(result, pub_id)
    return data


########################################################


def extract_data(result, requested_pub_id):
    assert result is not None, requested_pub_id
    pub_id = result["id"]
    assert pub_id == requested_pub_id
    ##
    year = int(result["year"])
    ##
    dico = result["title"]
    title = dico.get("default", dico.get("en", dico.get("fr", "No_title")))
    ##
    kind = result.get("type", "No_type")
    ##
    authors = result["authors"]
    author_fullnames = list()
    author_roles = list()
    for author in authors:
        fullname = author["fullName"]
        role = author.get("role", "author")
        author_fullnames.append(fullname)
        author_roles.append(role)
    ##
    pub_data = {
        "pub_id": pub_id,
        "title": title,
        "year": year,
        "kind": kind,
        "author_fullnames": author_fullnames,
        "author_roles": author_roles,
    }
    return pub_data


########################################################

API_publications_URL_string = (
    "https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/publications/"
)


def scanr_publications_request(pub_id, cache):
    # Warning: Pretty tricky!
    key = urllib.parse.quote(pub_id, safe="")
    key = urllib.parse.quote(key, safe="")
    if cache.holds_key(key):
        return cache.get_key_value(key)
    URL = API_publications_URL_string + key
    eprint(f"Sending request to ScanR: {pub_id}", end="... ")
    r = requests.get(URL, timeout=60)
    eprint(f"Done, response size = {len(r.content)}")
    if r.status_code != 200:
        return None
    r_json = None
    if r.text != "":  # Empty answer, return None
        r_json = r.json()
    cache.update_key_value(key, r_json)
    return r_json
