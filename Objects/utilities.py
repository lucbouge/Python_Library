import re
import time

from ..System.print import eprint
from ..System.utilities import isna, notna, date_to_year


def clean_row(row, *, table=None):
    new_row = dict()
    for (field, value) in row.items():
        if isna(value):
            value = None
        if isinstance(value, str):
            value = value.strip()
        assert field not in new_row
        if table is not None:
            new_field = table[field]
        else:
            new_field = field
        new_row[new_field] = value
    return new_row


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
        eprint(f"{n:5d}: {nb:6d}")
    eprint(f"Total: {total:6d}")

