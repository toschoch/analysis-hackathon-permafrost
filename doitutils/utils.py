#!/usr/bin/python
# -*- coding: UTF-8 -*-
# created: 22.01.2018
# author:  TOS

import logging
import mmap
import os

log = logging.getLogger(__name__)


class DuplicateFilter(object):
    def __init__(self):
        self.msgs = set()

    def filter(self, record):
        rv = record.msg not in self.msgs
        self.msgs.add(record.msg)
        return rv


def target_filenames(path, func, suffix=None):
    """
    returns the target file names derived from the function. If the function was created with the
    crates_files decorator, this otherwise the function name is used.
    Args:
        path: (str) path for the target file
        func: (function) function deriving targets for
        suffix: (str) requested file suffix, '_' uses last _ separated part of function name

    Returns:
        (str) target file path
    """
    function_name = func.__name__
    if hasattr(func, 'creates_files'):  # if specified monkey patched
        files = func.creates_files
        return [os.path.join(path, f) for f in files]

    else:  # use the function name for deriving the target filename
        if suffix != '_':
            return [os.path.join(path, "{}.{}".format(function_name, suffix))]
        elif suffix is not None:
            if function_name.find('_') > 0:
                splits = function_name.split('_')
                return [os.path.join(path, "{}.{}".format('_'.join(splits[:-1]), splits[-1]))]
        # default and best for compatibility is pickle
        return [os.path.join(path, "{}.{}".format(function_name, "pkl"))]


def tail(fname, n=5):
    """
    Reads the last n lines of a file without loading the whole file into memory.
    Args:
        fname: (path-like) path to file
        n: (int) optional, number of lines to load

    Returns:
        (list of str) tail lines
    """
    with open(fname) as source:
        mapping = mmap.mmap(source.fileno(), 0, access=mmap.ACCESS_READ)
    last = []
    old_i = -1
    for _ in range(n):
        i = mapping.rfind(b'\n', 0, old_i - 1) + 1
        last.append(mapping[i:old_i])
        old_i = i
    mapping.close()
    last = list(map(lambda s: s.decode(), last))
    return last


def head(fname, n=5):
    """
    Reads the first n lines of a file without loading the whole file into memory.
    Args:
        fname: (path-like) path to file
        n: (int) optional, number of lines to load

    Returns:
        (list of str) head lines
    """
    with open(fname) as source:
        mapping = mmap.mmap(source.fileno(), 0, access=mmap.ACCESS_READ)
    first = []
    old_i = 0
    for _ in range(n):
        i = mapping.find(b'\n', old_i, -1) + 1
        first.append(mapping[old_i:i])
        old_i = i
    mapping.close()
    first = list(map(lambda s: s.decode(), first))
    return first


def dict_to_string(meta, keys, fmt_dict={}):
    return "_".join([fmt_dict.get(k, "{}").format(meta.get(k)) for k in keys if k in meta])
