from ..System.print import eprint, epprint
from .person import Person
import re


class Project:
    def __init__(
        self,
        *,
        project_id=None,
        acronym=None,
        coordinator=None,  # Optional, may be None
        partners=None,
        reviewers=None,
        CES=None,  # Optional, may be None
    ):
        assert project_id is not None
        assert acronym is not None
        assert partners is not None
        assert reviewers is not None
        ##
        ##
        assert isinstance(project_id, str), project_id
        ##
        assert isinstance(acronym, str), acronym
        ##
        if coordinator is not None:
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
        if CES is not None:
            CES_pattern = r"CE(\d{2})"
            assert re.fullmatch(CES_pattern, CES), CES
        ##

        ##
        self.data = {
            "project_id": project_id,
            "acronym": acronym,
            "partners": tuple(partners),
            "reviewers": tuple(reviewers),
            "coordinator": coordinator,  # Optional, may be None
            "CES": CES,  # Optional, may be None
        }

    ##################################################################

    def __getitem__(self, field):
        return self.data[field]

    def __repr__(self):
        return "Project::" + repr(self.data)

    def __eq__(self, p):
        return self.data["project_id"] == p.data["project_id"]
