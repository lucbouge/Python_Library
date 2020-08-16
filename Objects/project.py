from ..System.print import eprint, epprint
from .person import Person


class Project:
    def __init__(
        self, acronym=None, coordinator=None, partners=None, reviewers=None,
    ):
        assert acronym is not None
        assert coordinator is not None
        assert partners is not None
        assert reviewers is not None
        ##
        assert isinstance(acronym, str)
        assert isinstance(coordinator, str), coordinator
        ##
        assert isinstance(partners, list) or isinstance(partners, tuple), acronym
        for partner_id in partners:
            assert isinstance(partner_id, str), partner_id
        ##
        assert isinstance(reviewers, list) or isinstance(reviewers, tuple), acronym
        for reviewer_id in reviewers:
            assert isinstance(reviewer_id, str), reviewer_id
        ##
        self.data = {
            "project_id": acronym,
            "acronym": acronym,
            "partners": tuple(partners),
            "reviewers": tuple(reviewers),
            "coordinator": coordinator,
        }

    ##################################################################

    def __getitem__(self, field):
        return self.data[field]

    def __repr__(self):
        return "Project::" + repr(self.data)

    def __eq__(self, p):
        return self.data["project_id"] == p.data["project_id"]
