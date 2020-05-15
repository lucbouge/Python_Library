import sys
import pprint



def eprint(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print('--> ', *args, **kwargs)


def epprint(*args, **kwargs):
    pprint.pprint(*args, stream=sys.stderr, **kwargs)
