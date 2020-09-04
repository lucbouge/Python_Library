from ...System.normalize import normalize_name
from ...System.print import eprint


def identify(*, person1=None, person2=None):
    assert person1 is not None
    assert person2 is not None

    firstname1 = person1["firstname"]
    normalized_firstname1 = normalize_name(firstname1)
    # lastname1 = person1["lastname"]
    fullname1 = person1["fullname"]
    normalized_fullname1 = normalize_name(fullname1)
    # person_id1 = person1["person_id"]
    # firstname_key1 = person1["firstname_key"]  # Normalized
    lastname_key1 = person1["lastname_key"]  # Normalized
    firstname_key_initial1 = person1["firstname_key_initial"]  # Normalized

    firstname2 = person2["firstname"]
    normalized_firstname2 = normalize_name(firstname2)
    # lastname2 = person2["lastname"]
    fullname2 = person2["fullname"]
    normalized_fullname2 = normalize_name(fullname2)
    # person_id2 = person2["person_id"]
    # firstname_key2 = person2["firstname_key"]  # Normalized
    lastname_key2 = person2["lastname_key"]  # Normalized
    firstname_key_initial2 = person2["firstname_key_initial"]  # Normalized

    test1 = (lastname_key1 in normalized_fullname2) and (
        lastname_key2 in normalized_fullname1
    )
    if not test1:
        return False
    test2 = (firstname_key_initial1 in normalized_firstname2) and (
        firstname_key_initial2 in normalized_firstname1
    )
    if not test2:
        return False
    eprint(f"Identified: {fullname1} = {fullname2}")
    return True
