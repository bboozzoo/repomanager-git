import subprocess
import shlex
import logging
import os
import os.path

__all__ = ('run_cmd', 'run_parts')

def run_cmd(cmd, chdir=None, env=None):
    """
    run a command and return a tuple retcode, stdout, stderr
    Arguments:
    - `cmd`: command string
    - `chdir`: directory to chdir into before runing a command
    - `env`: environment variables to append
    """
    l = logging.getLogger('screpper.util')
    cmd_l = shlex.split(cmd)
    l.debug('exec command %s' % (cmd))
    l.debug('as list %s' % (cmd_l))

    # set directory to current if not defined
    if not chdir:
        chdir = os.getcwd()

    # prepare environemtn
    if env:
        new_env = dict(os.environ.items() + env.items())
    else:
        new_env = os.environ
    p = subprocess.Popen(cmd_l, cwd=chdir, stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, env=new_env)
    
    try:
        out, err = p.communicate()
        l.debug('stdout: ' + str(out))
        l.debug('stderr: ' + str(err))
    except Exception, e:
        l.error('failed to run process: %s' % (str(e)))
        pass

    l.debug('process finished, retcode %d' % (p.returncode))
    return p.returncode, out, err


def run_parts(sdir, env=None):
    """run scripts from given directory
    
    Arguments:
    - `sdir`: scripts directory
    - `env`: additional env variables to set
    """
    l = logging.getLogger('screpper.util')

    flist = filter(lambda x: os.path.isfile(os.path.join(sdir, x)), os.listdir(sdir))
    flist = filter(lambda x: not x.endswith('~'), flist)
    flist.sort()
    l.debug('hooks: %s' % (str(flist)))

    for f in flist:
        l.info('running script %s' % (f))
        ret, out, err = run_cmd(os.path.join('.', f), sdir, env)
        if ret != 0:
            l.error('script %s failed, exit status %d' % (f, ret))
    

def singleton(cls):
    """
    signleton decorator function
    """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
