import logging
from screpper.git.gitcmd import open_repo, create_bare_repo
import sys
import os.path
from screpper.utils import run_cmd, run_parts
from screpper.conf import load_config

# root directory for all repositories
REPO_ROOT = 'repositories'
HOOKS_DIR = 'hooks'

class InvalidParameters(Exception):
    """
    """
    def __init__(self, what, cmd=None):
        """constructor
        
        Arguments:
        - `what`:
        - `cmd`:
        """
        super(Exception, self).__init__(what)
        self.failed_cmd = cmd

def __extract_repo_name_path(args):
    """
    extract repository name and path from args
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('screpper.cli')
    c = load_config()

    # command for which this function is called comes first
    cmd = args[0]
    if len(args) < 2:
        raise InvalidParameters("repository name not provided", cmd)
    name = args[1]
    if not name.endswith('.git'):
        l.warning('rename repository from %s to %s' % (name, name + '.git'))
        name += '.git'

    path = os.path.join(c.repository_root, name)
    return name, path
    
def list_repos(args):
    """list repositories
    
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('screpper.cli')
    l.info('list repositories')
    pass

def create_repo(args):
    """create repository
    
    Arguments:
    - `args`:
    """
    l = logging.getLogger('screpper.cli')
    
    c = load_config()

    l.info('create repository')

    name, path = __extract_repo_name_path(args)

    repo = create_bare_repo(path)
    # run hooks
    l.info('running user hooks for repot at %s' % (path))
    run_parts(c.hooks_root, env={'REPO_PATH' : os.path.abspath(path)})

def gc_repo(args):
    """run gc in repository
    
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('screpper.cli')
    l.info('run gc on repository')

    name, path = __extract_repo_name_path(args)
    
    repo = open_repo(path)
    repo.run_gc()

def show_help(args, cmnds, cmd=None):
    """show help message
    
    Arguments:
    - `args`: list of arguments
    - `cmnds`: commands map
    - `cmd`: specific command to show help entry for
    """
    if cmd and cmd in cmnds:
        print '\t' + cmnds[cmd][1]
    else:
        for single_cmd in cmnds.values():
            print '\t' + single_cmd[1]

def set_config(args):
    """
    set config option
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('screpper.cli')
    l.info('set config')

    cmd = args[0]

    name, path = __extract_repo_name_path(args)
    
    repo = open_repo(path)
    # skip args 0 and 1
    if len(args) < 3:
        raise InvalidParameters('not enough arguments', cmd)

    args = args[2:]
    # the format of key value key value..
    # even number of arguments is needed
    if not args or len(args) % 2 != 0:
        raise InvalidParameters('incorrect arguments format', cmd)
    
    # pack everythong into a dict
    setc = dict(zip(args[0::2], args[1::2]))
    
    repo.set_config(setc)

def get_config(args):
    """
    get config option
    Arguments:
    - `args`: list of arguments, 0 is always command name
    """
    l = logging.getLogger('screpper.cli')
    l.info('get config')

    name, path = __extract_repo_name_path(args)
    
    repo = open_repo(path)
    conf = repo.get_config()
    for k, v in conf.iteritems():
        print '%s -> %s' % (k, v)

def main():
    """CLI interface main
    """
    # setup logging
    logging.basicConfig(lvl=logging.DEBUG)

    c = load_config()

    l = logging.getLogger('screpper')
    if c.logging_level == 'DEBUG':
        l.setLevel(logging.DEBUG)

    cmnds = { 'help' : (lambda x: show_help(x, cmnds), 
                        """help - show help information"""),
              'create' : (create_repo, 
                          """create <repository name> - create a repository"""),
              'list' : (list_repos, 
                        """list - list repositories"""),
              'gc' : (gc_repo, 
                      """gc <repository name> - run git gc in repository"""),
              'setc' : (set_config, 
                        """setc <key> <value> [<key> <value>] - set config keys"""),
              'getc' : (get_config, 
                        """getc [<key> ...] - get keys from configuration (or all if no keys are provided""")
              }
    args = sys.argv[1:]

    if len(args) == 0 or \
            args[0] not in cmnds:
        print 'No or unknown command'
        show_help(args, cmnds)
        raise SystemExit(1)
    
    try:
        cmnds[args[0]][0](args)
    except InvalidParameters, e:
        print str(e)
        show_help(args, cmnds, e.failed_cmd)
    except:
        raise
