#!/usr/bin/env python

import repgit
import getopt
import sys

def list_repos(args):
    """list repositories
    
    Arguments:
    - `args`:
    """
    pass

def create_repo(args):
    """create repository
    
    Arguments:
    - `args`:
    """
    pass

def gc_repo(args):
    """run gc in repository
    
    Arguments:
    - `args`:
    """
    pass

def show_help(args):
    """show help message
    
    Arguments:
    - `args`:
    """
    pass


def main():
    """
    """
    cmnds = { 'help' : show_help,
              'create' : create_repo,
              'list' : list_repos,
              'gc' : gc_repo
              }
    args = sys.argv[1:]

    if len(args) == 0 or \
            args[1] not in cmnds:
        show_help(args)
        raise SystemExit(1)
    
    cmnds[args[0]](args)

if __name__ == '__main__':
    main()

    

