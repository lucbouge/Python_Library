import sys
import pprint


def eprint(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print("--> ", *args, **kwargs)


# def epprint(*args, **kwargs):
#     def f(a):
#         pprint.pprint(a, stream=sys.stderr, **kwargs)

#     if len(args) == 1:
#         f(*args)
#     else:
#         f(args)


def epprint(*args, **kwargs):
    kwargs["stream"] = sys.stderr
    if len(args) > 1:  # Trick!
        args = (args,)
    pprint.pprint(*args, **kwargs)
