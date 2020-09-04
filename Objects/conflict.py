from ..System.print import eprint, epprint


class Conflict:
    def __init__(
        self,
        *,
        ##
        project_id=None,
        pub_id=None,
        ##
        reviewer=None,
        reviewer_id=None,
        reviewer_found=None,
        reviewer_roles=None,
        ##
        partner=None,
        partner_id=None,
        partner_found=None,
        partner_roles=None,
    ):
        assert project_id is not None
        assert pub_id is not None
        assert reviewer is not None
        assert reviewer_id is not None
        assert partner is not None
        assert partner_id is not None
        assert partner_id != reviewer_id, project_id
        ##
        self.data = {
            "project_id": project_id,
            "pub_id": pub_id,
            ##
            "reviewer": reviewer,
            "reviewer_id": reviewer_id,
            "reviewer_found": reviewer_found,
            "reviewer_roles": reviewer_roles,
            ##
            "partner": partner,
            "partner_id": partner_id,
            "partner_found": partner_found,
            "partner_roles": partner_roles,
        }

    def __getitem__(self, field):
        return self.data[field]

    def __repr__(self):
        return repr(self.data)

    def __eq__(self, t):
        assert isinstance(t, Conflict)
        return self.data == t.data
