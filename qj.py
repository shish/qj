#!/usr/bin/env python3

from typing import List, Tuple
import argparse
import json
import sys
import os

from .lib import find


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern")
    parser.add_argument("filenames", nargs="*")
    parser.add_argument(
        "-k",
        dest="show_values",
        action="store_false",
        default=True,
        help="only show keys",
    )
    parser.add_argument(
        "-v",
        dest="show_keys",
        action="store_false",
        default=True,
        help="only show values",
    )
    parser.add_argument(
        "-K",
        dest="search_values",
        action="store_false",
        default=True,
        help="only search keys",
    )
    parser.add_argument(
        "-V",
        dest="search_keys",
        action="store_false",
        default=True,
        help="only search values",
    )
    parser.add_argument(
        "-p",
        dest="show_path",
        action="store_true",
        default=None,
        help="always show file path",
    )
    parser.add_argument(
        "-P",
        dest="show_path",
        action="store_false",
        default=None,
        help="always hide file path",
    )
    args = parser.parse_args()

    if args.show_path is None:
        args.show_path = len(args.filenames) > 1

    return args


def get_results(args: argparse.Namespace) -> List[Tuple[str, str]]:
    """
    Kick off a search for each file (or stdin if there are no files)
    """
    if not args.filenames:
        path = "-:" if args.show_path else ""
        obj = json.load(sys.stdin)
        results = find(args.pattern, obj, path, args.search_keys, args.search_values)
    else:
        results = []
        for filename in args.filenames:
            if not args.show_path:
                path = ""
            else:
                path = filename + ":"
            with open(filename) as fp:
                obj = json.load(fp)
            results.extend(
                find(args.pattern, obj, path, args.search_keys, args.search_values)
            )
    return results


def display(args: argparse.Namespace, results: List[Tuple[str, str]]) -> None:
    """
    Print results according to the display rules given on the CLI
    """
    for k, v in results:
        if args.show_keys and args.show_values:
            print("%s = %s" % (k, json.dumps(v)))
        elif args.show_keys:
            print(k)
        elif args.show_values:
            print(v)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    results = get_results(args)
    display(args, results)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
