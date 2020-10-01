import os
import re
import time
import pandas as pd

from .print import eprint


def isna(x):
    return pd.isna(x)


def notna(x):
    return pd.notna(x)


def date_to_year(date):
    assert date is not None
    year = time.strftime("%Y", time.gmtime(date / 1000))
    assert re.fullmatch(r"\d{4}", year), year
    assert 1900 <= int(year) <= 2050, year
    return year


def dump_dict_to_xlsx(dico, *, dataname=None, dir=None, columns=None):
    df = pd.DataFrame.from_dict(dico, orient="index")
    path = os.path.join(dir, dataname + ".xlsx")
    eprint(f"Dumping dict to {path}")
    if columns is not None:
        df = df[list(columns)]
    df.to_excel(path, index=False)
