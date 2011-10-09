import logging
import os
from utils import run_cmd

class GitException(Exception):
    """exception wrapper
    """
    pass

def is_git_repo(path):
    """
    check if a repository is present under given path
    Arguments:
    - `path`:
    """
    ret, out, err = run_cmd('git rev-parse --git-dir', path)
    if ret == 0:
        return True
    return False

class Repo(object):
    """repository wrapper
    """
    
    def __init__(self, path, bare=False):
        """initialize Repo object, bound to given path
        NOTE: there are no changes done to repository yet
        
        Arguments:
        - `path`:
        - `bare`:
        """
        l = logging.getLogger('git')
        l.debug('initializing repository object at %s' % (path))
        self._path = path
        self._bare = bare
        if self._bare:
            l.debug('repository is bare')

    def bind(self, ):
        """
        perform verfication and create repository (if bare)
        """
        if self._bare:
            if os.path.exists(self._path):
                raise GitException('path %s already present' % (self._path))

            run_cmd('git init --bare %s' % (self._path))
        else:
            if not is_git_repo(self._path):
                raise GitException('%s is not a git repository' % (self._path))

    @classmethod
    def init_bare(cls, path):
        """
        
        Arguments:
        - `path`:
        """
        
        r = Repo(path, bare=True)
        r.bind()
        return r

    @classmethod
    def init_existing(cls, path):
        """
        
        Arguments:
        - `path`:
        """
        r = Repo(path)
        r.bind()
        return r

    def set_config(self, keys):
        """set a list of config options
        
        Arguments:
        - `keys`: a map of config options
        """
        l = logging.getLogger('git')
        for (k, v) in keys.iteritems():
            l.debug('setting %s = %s' % (k, v))
            run_cmd('git config --local --replace-all %s %s' % (k, v), self._path)

    def get_config(self, keys=None):
        """get a config option for key
        
        Arguments:
        - `keys`: list of keys to get, empty list or None means all keys
        """
        l = logging.getLogger('git')
        d = {}
        # get all keys first
        ret, out, err = run_cmd('git config --local -l', self._path)
        if ret != 0:
            raise GitException('failed to obtain configuration')
        
        l.debug('wanted keys: %s' % (keys))

        # then filter only ones we are interested in
        lines = out.strip().split('\n')
        for l in lines:
            k, v = l.split('=')
            if not keys or k in keys:
                d[k] = v

        return d

    def run_gc(self, ):
        """run gc on repository
        """
        run_cmd('git gc', self._path)


def open_repo(path):
    """create a Repo object bound to given path
    
    Arguments:
    - `path`:
    """
    l = logging.getLogger('git')
    l.info('open a repository at %s' % (path))
    r = Repo.init_existing(path)
    return r

def create_bare_repo(path):
    """create a Repo object for a bare repository. Initialization of a
    bare repository is performed, hence it should not exist
    beforehand.
    
    Arguments:
    - `path`:
    """
    l = logging.getLogger('git')
    l.info('create a repository at %s' % (path))
    r = Repo.init_bare(path)
    return r
    


    
