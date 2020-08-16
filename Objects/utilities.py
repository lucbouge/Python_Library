import re
import time
import pandas as pd


from ..System.normalize import normalize_name
from ..System.print import eprint


def print_stats_len(title, dico):
    assert isinstance(dico, dict)
    total = len(dico)
    histo = dict()
    for (_, v) in dico.items():
        n = len(v)
        if n not in histo:
            histo[n] = 0
        histo[n] += 1
    print("_" * 30)
    eprint(title)
    for (n, nb) in sorted(histo.items()):
        eprint(f"{n}:\t{nb}")
    eprint(f"Total:\t{total}")


def date_to_year(date):
    assert date is not None
    year = time.strftime("%Y", time.gmtime(date / 1000))
    assert re.fullmatch(r"\d{4}", year), year
    assert 1900 <= int(year) <= 2050, year
    return year
