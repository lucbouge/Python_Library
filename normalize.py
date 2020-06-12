import re
import unidecode


def normalize_name(s, strong=False):
    assert isinstance(s, str), s
    initial_s = s
    # Project on ASCII
    s = unidecode.unidecode(s)
    # Project on lower-case letters
    s = s.lower()
    # Strip to remove extrem spaces
    s = s.strip()
    # Remove repeated spaces and make them '_'
    s = re.sub(r"\s+", r"_", s)
    # Remove repeated '_', if any left
    s = re.sub(r"_+", r"_", s)
    ##
    if not strong:
        return s
    # Remove all non-letters
    s = re.sub(r"[^a-z]", "", s)
    # Remove all repeated letters
    s = re.sub(r"(.)\1+", r"\1", s)
    assert s != "", initial_s
    return s
