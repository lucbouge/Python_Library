import sys
import pprint
from pprint import pformat


def eprint(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print("--> ", *args, **kwargs)


def epprint(*args, **kwargs):
    def f(a):
        pprint.pprint(a, stream=sys.stderr, **kwargs)

    if len(args) == 1:
        f(args[0])
    else:
        f(args)

