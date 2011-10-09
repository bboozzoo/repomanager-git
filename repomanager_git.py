#!/usr/bin/env python

import logging
import repgit
import sys
import os.path
from utils import run_cmd, run_parts

# root directory for all repositories
REPO_ROOT = 'repositories'
HOOKS_DIR = 'hooks'

class InvalidParameters(Exception):
    """
    """
    pass

def __extract_repo_name_path(args):
    """
    extract repository name and path from args
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('manager')

    if len(args) < 2:
        raise InvalidParameters("repository name not provided")
    name = args[1]
    if not name.endswith('.git'):
        l.warning('rename repository from %s to %s' % (name, name + '.git'))
        name += '.git'

    path = os.path.join(REPO_ROOT, name)
    return name, path
    
def list_repos(args):
    """list repositories
    
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('manager')
    l.info('list repositories')
    pass

def create_repo(args):
    """create repository
    
    Arguments:
    - `args`:
    """
    l = logging.getLogger('manager')
    l.info('create repository')

    name, path = __extract_repo_name_path(args)

    repo = repgit.create_bare_repo(path)
    # run hooks
    l.info('running user hooks for repot at %s' % (path))
    run_parts(HOOKS_DIR, env={'REPO_PATH' : os.path.abspath(path)})

def gc_repo(args):
    """run gc in repository
    
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('manager')
    l.info('run gc on repository')

    name, path = __extract_repo_name_path(args)
    
    repo = repgit.open_repo(path)
    repo.run_gc()

def show_help(args):
    """show help message
    
    Arguments:
    - `args`:
    """
    pass

def set_config(args):
    """
    set config option
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('manager')
    l.info('set config')

    name, path = __extract_repo_name_path(args)
    
    repo = repgit.open_repo(path)
    # skip args 0 and 1
    if len(args) < 3:
        raise Exception('not enough arguments')

    args = args[2:]
    # the format of key value key value..
    # even number of arguments is needed
    if not args or len(args) % 2 != 0:
        raise Exception('incorrect arguments format')
    
    # pack everythong into a dict
    setc = dict(zip(args[0::2], args[1::2]))
    
    repo.set_config(setc)

def get_config(args):
    """
    get config option
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('manager')
    l.info('get config')

    name, path = __extract_repo_name_path(args)
    
    repo = repgit.open_repo(path)
    conf = repo.get_config()
    for k, v in conf.iteritems():
        print '%s -> %s' % (k, v)
    

def repomanager_main():
    """
    """
    logging.basicConfig(level=logging.DEBUG)
    cmnds = { 'help' : show_help,
              'create' : create_repo,
              'list' : list_repos,
              'gc' : gc_repo,
              'setc' : set_config,
              'getc' : get_config
              }
    args = sys.argv[1:]

    if len(args) == 0 or \
            args[0] not in cmnds:
        show_help(args)
        raise SystemExit(1)
    
    cmnds[args[0]](args)

if __name__ == '__main__':
    repomanager_main()

    

