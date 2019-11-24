import logging
import pathlib

DOIT_CONFIG = {'default_tasks': []}

log = logging.getLogger()


def task_data():
    """ runs python functions in src.data creating data files """

    from doitutils.collect import collect_functions
    from doitutils.utils import target_filenames

    functions = collect_functions('src.data')

    input_path = pathlib.Path("data/raw")
    out_path = pathlib.Path("data/processed")
    for func_name, func, src_file in functions:
        out_files = target_filenames(out_path, func, suffix='_')

        yield {'name': func_name,
               'doc': func.__doc__,
               'actions': [(func, [input_path])],
               'targets': out_files,
               'file_dep': [src_file],
               'clean': True}


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from doit.cmd_base import ModuleTaskLoader
    from doit.doit_cmd import DoitMain

    d = DoitMain(ModuleTaskLoader(globals()))
    d.run(['list', '--all'])
