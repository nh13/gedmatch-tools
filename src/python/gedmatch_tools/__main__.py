import logging

import defopt

from gedmatch_tools.tools.add import add, add_all
from gedmatch_tools.tools.ls import ls
from gedmatch_tools.tools.one_to_one import one_to_one, \
    one_to_one_tuples
from gedmatch_tools.tools.rm import rm, rm_r


def main() -> None:
    '''The main entry point for all tools'''
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    defopt.run([
        add,
        add_all,
        ls,
        rm,
        rm_r,
        one_to_one,
        one_to_one_tuples
    ])


if __name__ == '__main__':
    main()
