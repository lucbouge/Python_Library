
def extract_unique_elements(l):
    ll = list()
    for e in l:
        if l in ll:
            continue
        ll.append(e)
    return ll
