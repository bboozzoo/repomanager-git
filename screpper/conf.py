from screpper.utils import singleton
import logging
import os

# default paths to configuration files
# loading will be attempted in this order
DEFAULT_CONFIG_PATHS = ['/etc/screpper/screpper.conf',
                        'screpper.conf']

def load_config():
    """load configuration file
    """
    return Config()
    

@singleton
class Config(object):
    """configuration wrapper
    """
    
    def __init__(self, ):
        """
        """
        l = logging.getLogger('screpper.conf')
        self._settings = {}
        try:
            for conff in DEFAULT_CONFIG_PATHS:
                # try to load config files in order as in list
                l.debug('try config at: ' + conff)
                if os.path.exists(conff):
                    l.debug('loading configuration: ' + conff)
                    execfile(conff, self._settings)
                    break
        except:
            l.error('failed to load configuration')
            raise

        # dump certain keys such as __doc__, __builtins__ etc.
        dump_keys = ['__builtins__', '__doc__']
        for key in dump_keys:
            if key in self._settings:
                del self._settings[key]

    def __getattr__(self, attr):
        """
        
        Arguments:
        - `attr`:
        """
        return self._settings[attr]

        
