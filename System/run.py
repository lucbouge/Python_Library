import os
import argparse
import glob

from .print import eprint

MAX = 100


def phase_to_function(i):
    # eprint("phase_to_function", i)
    basename = "Phases"
    path_pattern = os.path.join(basename, f"phase_{i:02d}_*.py")
    paths = glob.glob(path_pattern)
    if len(paths) == 0:
        return (None, "No_such_module")
    assert len(paths) == 1, paths
    path = paths[0]
    # eprint(f"Loading module: {path}")
    (dirname, filename) = os.path.split(path)
    assert dirname == basename, path
    (modulename, ext) = os.path.splitext(filename)
    assert ext == ".py", filename
    fullmodulename = basename + "." + modulename
    new_module = __import__(fullmodulename, fromlist=("main"))
    function = new_module.main
    return (function, fullmodulename)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--from",
        metavar="phase id",
        help="phase to start with",
        type=str,
        default="0",
        dest="from_phase",
    )
    parser.add_argument(
        "--to",
        metavar="phase id",
        help="phase to end with",
        type=str,
        default=str(MAX - 1),
        dest="to_phase",
    )
    parser.add_argument(
        "--phase",
        metavar="phase id",
        help="phases to run",
        type=str,
        default=None,
        action="extend",
        nargs="+",
        dest="phase",
    )

    args = parser.parse_args()
    return args


def run_phase(phase):
    (function, modulename) = phase_to_function(phase)
    if function is None:
        return
    eprint("\n" * 4)
    eprint("=" * 100)
    eprint(f"Phase: {phase}, module: {modulename}")
    eprint("\n" * 2)
    function()


def run_phases(phases):
    for i in phases:
        run_phase(int(i))


def run():
    args = parse()
    # eprint(args)
    if args.phase is not None:
        run_phases(args.phase)
        return
    i1 = int(args.from_phase)
    i2 = int(args.to_phase)
    run_phases(range(i1, i2 + 1))
