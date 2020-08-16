from Packages.local.conflict import Conflict
from Packages.lib.print import eprint

# from Packages.local.person import Person
from .identify import identify


def get_conflicts_list(
    publication=None,
    reviewers_ids=None,
    partners_ids=None,
    person_id_to_data_dict=None,
    author_fullname_to_person_dict=None,
    project_id=None,
):
    conflicts_list = list()
    ##
    publication_persons = tuple(
        author_fullname_to_person_dict[author_fullname]
        for author_fullname in publication["author_fullnames"]
        if "skipping" not in author_fullname.lower()
    )
    ##
    reviewers_persons = tuple(
        person_id_to_data_dict[reviewer_id]["person"] for reviewer_id in reviewers_ids
    )
    ##
    partners_persons = tuple(
        person_id_to_data_dict[partner_id]["person"] for partner_id in partners_ids
    )
    ##
    for reviewer_person in reviewers_persons:
        for partner_person in partners_persons:
            data = check_conflict(
                publication=publication,
                publication_persons=publication_persons,
                reviewer_person=reviewer_person,
                partner_person=partner_person,
            )
            if data is None:
                continue
            conflict = Conflict(
                project_id=project_id,
                pub_id=publication["pub_id"],
                ##
                reviewer=data["reviewer"],
                reviewer_id=data["reviewer_id"],
                reviewer_found=data["reviewer_found"],
                reviewer_roles=data["reviewer_roles"],
                ##
                partner=data["partner"],
                partner_id=data["partner_id"],
                partner_found=data["partner_found"],
                partner_roles=data["partner_roles"],
            )
            conflicts_list.append(conflict)
    return conflicts_list


########################################################


def check_conflict(
    publication=None,
    publication_persons=None,
    reviewer_person=None,
    partner_person=None,
):
    reviewer_fullname_found = check_person_authors(
        project_person=reviewer_person, publication_persons=publication_persons
    )
    if reviewer_fullname_found is None:
        return None
    ##
    partner_fullname_found = check_person_authors(
        project_person=partner_person, publication_persons=publication_persons
    )
    if partner_fullname_found is None:
        return None
    ##
    reviewer_roles = None
    partner_roles = None
    if publication["kind"] == "these":
        roles_found = check_person_roles(
            author_fullnames=publication["author_fullnames"],
            author_roles=publication["author_roles"],
            reviewer_fullname_found=reviewer_fullname_found,
            partner_fullname_found=partner_fullname_found,
        )
        if roles_found is None:
            return None
        reviewer_roles = roles_found["reviewer"]
        partner_roles = roles_found["partner"]
    ##
    reviewer_id = reviewer_person["person_id"]
    partner_id = partner_person["person_id"]
    assert reviewer_id != partner_id
    data = {
        "reviewer": reviewer_person,
        "reviewer_id": reviewer_id,
        "reviewer_found": reviewer_fullname_found,
        "partner": partner_person,
        "partner_id": partner_id,
        "partner_found": partner_fullname_found,
        "reviewer_roles": reviewer_roles,
        "partner_roles": partner_roles,
    }
    return data


##################################################################


def check_person_authors(project_person=None, publication_persons=None):
    assert project_person is not None
    assert publication_persons is not None
    for publication_person in publication_persons:
        if identify(project_person, publication_person):
            return publication_person["fullname"]
    return None


##################################################################


def check_person_roles(
    author_fullnames=None,
    author_roles=None,
    reviewer_fullname_found=None,
    partner_fullname_found=None,
):
    assert author_fullnames is not None
    assert author_roles is not None
    assert reviewer_fullname_found is not None
    assert partner_fullname_found is not None
    reviewer_indices = find_indices(author_fullnames, reviewer_fullname_found)
    reviewer_roles = set(author_roles[i] for i in reviewer_indices)
    partner_indices = find_indices(author_fullnames, reviewer_fullname_found)
    partner_roles = set(author_roles[i] for i in partner_indices)
    roles = reviewer_roles | partner_roles
    if not ("directeur" in roles or "author" in roles):
        return None
    data = {
        "reviewer": reviewer_roles,
        "partner": partner_roles,
    }
    return data


def find_indices(l, a):
    indices = list()
    for i in range(0, len(l)):
        if a == l[i]:
            indices.append(i)
    return indices
