#!/usr/bin/python
# -*- coding: UTF-8 -*-
# created: 27.02.2018
# author:  TOS

import logging
import inspect
import importlib as imp
import pkgutil

log = logging.getLogger(__name__)


def collect_from_module(path, collect, exclude_module=[]):
    """
    recursively iterates through packages in path, imports all modules and calls 'collect' on modules.
    Args:
        path: (str, pathlib.Path) path to be iterated
        collect: (function) called with module as argument
        exclude_module: (list of str) skips modules with names matching any of passed names.
    """

    # import path
    pkg = imp.import_module(path)

    if not hasattr(pkg, '__path__'):
        collect(pkg)
    else:
        # iterate through all modules in the package
        for _, name, ispkg in pkgutil.iter_modules(pkg.__path__):

            if name in exclude_module: continue

            if not ispkg:
                mod = imp.import_module("{}.{}".format(path, name))
                collect(mod)


def collect_functions(path, exclude_module=[], exclude_functions=[]):
    """
    collects and returns all functions in the modules in this package.
    Args:
        path: (str) module or package to look for function e.g. src.data
        exclude_module: (list of str) modules to exclude
        exclude_functions: (list of str) functions to exclude
    Returns:
        list of functions as 3-tuple (function, name, source file path)
    """

    functions = []

    def _collect(mod):

        # collect all functions of module except '_xxx'
        for name, func in inspect.getmembers(mod, inspect.isfunction):

            if name in exclude_functions: continue

            if inspect.getmodule(func) == mod and not name.startswith('_'):
                functions.append((name, func, mod.__file__))

    collect_from_module(path, _collect, exclude_module)

    return functions

