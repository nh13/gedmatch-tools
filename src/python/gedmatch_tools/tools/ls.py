from gedmatch_tools.api import ls as ls_api


def ls() -> None:
    '''Lists the kits available on GEDMatch.com'''
    print('kit_one\tkit_two')
    for kit in ls_api():
        print(f'{kit.name}\t{kit.number}')
