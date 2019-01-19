import sys
from typing import Optional


def _query_yes_no(question: str, default: Optional[str]=None) -> bool:
    '''Ask a yes/no question via raw_input() and return their answer.

    See: https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input

    Args:
        questions: the question presented to the user.
        default: the presumed answer if the user just hits <Enter>.  It must be "yes" (the
                 default), "no" or None (meaning an answer is required of the user).

    Returns:
        True for "yes" or False for "no".
    '''
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
