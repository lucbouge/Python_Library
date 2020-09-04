import re

from ...System.normalize import normalize_name

ignored_name_blocks = (
    "de",
    "du",
    "des",
    "le",
    "la",
    "les",
    "von",
    "van",
    "der",
    "die",
    "das",
    "della",
    "del",
    "dell",
    "di",
    "dos",
    "el",
    "di",
    "da",
    "d",
    "l",
    "o",
    "al",
    "ben",
    "bar",
)
ignored_name_blocks = tuple(block.lower() for block in ignored_name_blocks)


def get_blocks(name):
    blocks = re.split(r"[\s'.-]+", name)
    assert len(blocks) > 0, name
    clean_blocks = list()
    for block in blocks:
        block = block.strip()
        if len(block) <= 1:
            continue
        if block.lower() in ignored_name_blocks:
            continue
        clean_blocks.append(normalize_name(block))
    if len(clean_blocks) == 0:
        return (blocks[0],)
    return clean_blocks


def split_name(fullname):
    fullname = fullname.strip(" .-'_")
    if "," in fullname:
        assert fullname.count(",") == 1, fullname
        (lastname, firstname) = fullname.split(",")
        return (firstname, lastname)
    assert "," not in fullname
    if fullname.count(" ") == 1:
        (firstname, lastname) = fullname.split(" ")
        return (firstname, lastname)
    fullname = re.sub(r"\s+", " ", fullname)
    if "." in fullname:
        (before, here, after) = fullname.rpartition(".")
        firstname = before + here
        lastname = after
        return (firstname, lastname)
    if " " not in fullname:
        firstname = ""
        lastname = fullname
        return (firstname, lastname)
    assert " " in fullname, fullname
    (before, here, after) = fullname.rpartition(" ")
    firstname = before + here
    lastname = after
    return (firstname, lastname)


def fullname_to_first_and_lastnames(fullname):
    (firstname, lastname) = split_name(fullname)
    firstname = firstname.strip()
    lastname = lastname.strip()
    assert len(lastname) > 0, (fullname, "-->", firstname, lastname)
    if len(firstname) == 0:
        firstname = "No_firstname"
    return (firstname, lastname)


def get_keys(*, fullname=None, firstname=None, lastname=None):
    if fullname is not None:
        assert firstname is None
        assert lastname is None
        ##
        fullname = fullname.strip()
        (firstname, lastname) = fullname_to_first_and_lastnames(fullname)
        firstname = firstname.strip()
        lastname = lastname.strip()
    else:
        assert fullname is None
        assert firstname is not None
        assert lastname is not None
        ##
        firstname = firstname.strip()
        lastname = lastname.strip()
        fullname = f"{firstname} {lastname}"
        fullname = fullname.strip()
    ##
    person_id = normalize_name(fullname)
    ##
    # eprint(fullname, "-->", firstname, "|", lastname)
    firstname_blocks = get_blocks(firstname)  # Normalized
    lastname_blocks = get_blocks(lastname)  # Normalized
    ##
    if len(firstname_blocks) == 0:
        firstname_blocks = ["No_firstname"]
    if len(lastname_blocks) == 0:
        lastname_blocks = ["No_lastname"]
    firstname_key = firstname_blocks[0]
    lastname_key = lastname_blocks[0]
    firstname_key_initial = firstname_key[0]
    ##
    keys = {
        "firstname": firstname,
        "lastname": lastname,
        "fullname": fullname,
        "person_id": person_id,  # Normalized
        "firstname_key": firstname_key,  # Normalized
        "lastname_key": lastname_key,  # Normalized
        "firstname_key_initial": firstname_key_initial,  # Normalized
    }
    return keys
