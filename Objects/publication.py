from Packages.lib.print import eprint, epprint
from Packages.local.person import Person
from .Publication.person_to_pub_ids_set import get_pub_ids_set
from .Publication.pub_id_to_publication import get_data

max_number_authors = 15

roles_values = (
    "author",
    "directeurthese",
    "membrejury",
    "presidentjury",
    "rapporteur",
    "__inventeur",
    "__deposant",
    "__deposant__inventeur",
)

kinds_values = (
    "book",
    "presconf",
    "posted-content",
    "proceedings-article",
    "monograph",
    "other",
    "journal-article",
    "these",
    "No_type",
    "patent",
    "mem",
    "book-chapter",
    "report-series",
    "dataset",
    "reference-entry",
    "report",
    "img",
    "poster",
    "component",
    "peer-review",
)


class Publication:
    def __init__(
        self,
        pub_id=None,
        title=None,
        year=None,
        kind=None,
        author_fullnames=None,
        author_roles=None,
    ):
        assert pub_id is not None
        # assert title is not None
        if title is None:
            title = "No_title_Publication_init"
            eprint(f"Warning: No title for publication {pub_id}")
        assert year is not None
        assert kind is not None
        assert author_fullnames is not None
        if kind == "these":
            assert author_roles is not None
        pub_data = extract_pub_data(
            pub_id=pub_id,
            title=title,
            year=year,
            kind=kind,
            author_fullnames=author_fullnames,
            author_roles=author_roles,
        )
        ##
        self.data = {
            "pub_id": pub_data["pub_id"],
            "author_fullnames": pub_data["author_fullnames"],
            "author_roles": pub_data["author_roles"],
            "title": pub_data["title"],
            "year": pub_data["year"],
            "kind": pub_data["kind"],
        }

    ####################################################

    @staticmethod
    def get_publication(pub_id, cache):
        assert isinstance(pub_id, str), pub_id
        data = get_data(pub_id, cache)
        if data is None:
            eprint(f"No publication data for {pub_id}. Skipping.")
            return None
        publication = Publication(
            pub_id=data["pub_id"],
            title=data["title"],
            year=data["year"],
            kind=data["kind"],
            author_fullnames=data["author_fullnames"],
            author_roles=data["author_roles"],
        )
        return publication

    @staticmethod
    def get_pub_ids_set(person, cache):
        assert isinstance(person, Person), person
        pub_ids_set = get_pub_ids_set(person, cache)
        return pub_ids_set

    ####################################################

    def __getitem__(self, field):
        return self.data[field]

    def __repr__(self):
        return repr("Publication::" + self.data)

    def __eq__(self, p):
        return self.data["pub_id"] == p.data["pub_id"]


####################################################


def extract_pub_data(
    pub_id=None,
    title=None,
    year=None,
    kind=None,
    author_fullnames=None,
    author_roles=None,
):
    assert pub_id is not None
    assert isinstance(pub_id, str), pub_id
    ##
    assert title is not None
    assert isinstance(title, str), title
    ##
    assert year is not None
    assert isinstance(year, int), year
    assert 2015 <= year, year
    ##
    assert kind is not None
    assert isinstance(kind, str), kind
    assert kind in kinds_values, kind
    ##
    assert author_fullnames is not None
    assert isinstance(author_fullnames, list)
    for fullname in author_fullnames:
        assert isinstance(fullname, str), fullname
    ##
    assert author_roles is not None
    assert isinstance(author_roles, list)
    assert len(author_fullnames) == len(author_roles)
    for role in author_roles:
        assert role in roles_values, role
    ##
    collapsed_fullnames = collapse_list(
        pub_id, author_fullnames, kind="author", size=max_number_authors
    )
    collapsed_roles = collapse_list(
        pub_id, author_roles, kind="role", size=max_number_authors
    )
    assert len(collapsed_fullnames) == len(collapsed_roles)
    ##
    pub_data = {
        "pub_id": pub_id,
        "title": title,
        "year": year,
        "kind": kind,
        "author_fullnames": collapsed_fullnames,
        "author_roles": collapsed_roles,
    }
    return pub_data


def collapse_list(pub_id, l, kind=None, size=None):
    assert kind is not None
    assert size is not None
    assert isinstance(size, int) and size > 10, size
    assert isinstance(l, list)
    if len(l) <= 2 * size:
        return l
    nb = len(l)
    left = 0 + size
    right = 0 - size  # Trick to please the linter
    nn = len(l[left:right])
    if kind != "role":
        eprint(
            f"\tWarning: {pub_id} has {kind} list of size {nb}. "
            f"Skipping the {nn} middle ones."
        )
    dummy = f"(skipping {nn} elements)"
    l[left:right] = [dummy]
    assert len(l) == 2 * size + 1, len(l)
    return l
