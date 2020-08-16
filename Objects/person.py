import re
import pandas as pd

from Packages.lib.normalize import normalize_name
from Packages.lib.print import eprint

from .Person.name_to_keys import get_keys
from .Person.get_conflicts_list import get_conflicts_list
from .Person.identify import identify

##################################################################

# "firstname": firstname,
# "lastname": lastname,
# "fullname": fullname,
# "person_id": person_id,  # Normalized
# "firstname_key": firstname_key,  # Normalized
# "lastname_key": lastname_key,  # Normalized
# "firstname_key_initial": firstname_key_initial,  # Normalized

##################################################################


class Person:
    def __init__(self, firstname=None, lastname=None, fullname=None):
        if fullname is not None:
            assert pd.notna(fullname)
            assert firstname is None
            assert lastname is None
        else:
            assert fullname is None
            assert firstname is not None
            assert lastname is not None
            assert pd.notna(firstname)
            assert pd.notna(lastname)
        ##
        keys = get_keys(firstname=firstname, lastname=lastname, fullname=fullname)
        ##
        self.data = {
            "firstname": keys["firstname"],
            "lastname": keys["lastname"],
            "fullname": keys["fullname"],
            "person_id": keys["person_id"],
            "firstname_key": keys["firstname_key"],
            "firstname_key_initial": keys["firstname_key_initial"],
            "lastname_key": keys["lastname_key"],
            "firstname_normalized": normalize_name(keys["firstname"]),
            "lastname_normalized": normalize_name(keys["lastname"]),
        }

    ##################################################################

    @staticmethod
    def identify(*args):
        return identify(*args)

    @staticmethod
    def get_conflicts_list(**kwargs):
        return get_conflicts_list(**kwargs)

    def __getitem__(self, field):
        return self.data[field]

    def __repr__(self):
        return "Person::" + repr(self.data)

    def __eq__(self, p):
        return self.data["person_tag"] == p.data["person_tag"]
