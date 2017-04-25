import os
import sys
import pkgutil


def import_settings_module(name):
    """
    Smart and magic importing function
    """
    name = 'apimocker.settings.{}'.format(name)
    loader = pkgutil.find_loader(name)
    if loader:
        execfile(loader.filename, globals())


IS_TEST = len(sys.argv) > 1 and sys.argv[1] == 'test'
# used to distinguish web app from celery app, in logging for example
ENVIRONMENT = os.environ.get('ENVIRONMENT') or ('test' if IS_TEST else 'dev')

import_settings_module('vars.pull')
import_settings_module('vars.%s' % ENVIRONMENT)
# you can add your envs here, like API_BASE_URL
# in most cases it is the best place to adjust your development environment
import_settings_module('vars.local')

import_settings_module('base')
import_settings_module('base_m')
import_settings_module('envs.%s' % ENVIRONMENT)

import_settings_module('components.db')
import_settings_module('components.cache')
import_settings_module('components.celery')
import_settings_module('components.logging')

# here you can override everything we bundled so far
if IS_TEST:
    import_settings_module('local_tests')
else:
    import_settings_module('local')
