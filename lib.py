#!/usr/bin/env python3

import json
import re
from typing import List, Tuple, Any


identifier = re.compile("^[a-zA-Z_][a-zA-Z0-9_]*$")


def _jskey(s: str) -> str:
    """
    figure out if we can use object.attr or if we need
    to fall back to object["attr"]
    """
    if identifier.match(s):
        return ".%s" % s
    else:
        return "[%s]" % json.dumps(s)


def find(
    search: str,
    obj: Any,
    path: str = "",
    search_keys: bool = True,
    search_values: bool = True,
) -> List[Tuple[str, Any]]:
    """
    Recursively look through the JSON data structure $obj
    looking for things which match $search
    """
    results = []

    if isinstance(obj, list):
        for ik, v in enumerate(obj):
            results.extend(
                find(search, v, path + "[%d]" % ik, search_keys, search_values)
            )
    if isinstance(obj, dict):
        for sk, v in obj.items():
            if search_keys and search in sk:
                results.append((path + _jskey(sk), v))
            else:
                results.extend(
                    find(search, v, path + _jskey(sk), search_keys, search_values)
                )
    if isinstance(obj, str):
        if search_values and search in obj:
            results.append((path, obj))
    if search.isdigit() and isinstance(obj, int):
        if search_values and int(search) == obj:
            results.append((path, obj))

    return results
